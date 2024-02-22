# -*- coding: utf-8 -*-

import time
import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F

from utils import CTCLabelConverter, AttnLabelConverter
from dataset import RawDataset, AlignCollate
from model import Model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


import helper
import postprocess as pp


def demo(opt, former_score_list, base_status, former_base_status, frame_count):
    start = time.time()
    """ model configuration """
    if 'CTC' in opt.Prediction:
        converter = CTCLabelConverter(opt.character)
    else:
        converter = AttnLabelConverter(opt.character)
    opt.num_class = len(converter.character)

    if opt.rgb:
        opt.input_channel = 3

    model = Model(opt)
    model = torch.nn.DataParallel(model).to(device)

    # load model
    model.load_state_dict(torch.load(opt.saved_model, map_location=device))

    # prepare data. two demo images from https://github.com/bgshih/crnn#run-demo
    AlignCollate_demo = AlignCollate(imgH=opt.imgH, imgW=opt.imgW, keep_ratio_with_pad=opt.PAD)
    demo_data = RawDataset(root=opt.cropimg_folder, opt=opt)  # use RawDataset
    demo_loader = torch.utils.data.DataLoader(
        demo_data, batch_size=opt.batch_size,
        shuffle=False,
        num_workers=int(opt.workers),
        collate_fn=AlignCollate_demo, pin_memory=True)

    # predict
    scoreboard_list = []
    total_confidence_score = 0
    # start = time.time()
    model.eval()
    with torch.no_grad():
        for image_tensors, image_path_list in demo_loader:
            batch_size = image_tensors.size(0)
            image = image_tensors.to(device)
            # For max length prediction
            length_for_pred = torch.IntTensor([opt.batch_max_length] * batch_size).to(device)
            text_for_pred = torch.LongTensor(batch_size, opt.batch_max_length + 1).fill_(0).to(device)

            if 'CTC' in opt.Prediction:
                preds = model(image, text_for_pred)

                # Select max probabilty (greedy decoding) then decode index to character
                preds_size = torch.IntTensor([preds.size(1)] * batch_size)
                _, preds_index = preds.max(2)
                # preds_index = preds_index.view(-1)
                preds_str = converter.decode(preds_index, preds_size)

            else:
                preds = model(image, text_for_pred, is_train=False)

                # select max probabilty (greedy decoding) then decode index to character
                _, preds_index = preds.max(2)
                preds_str = converter.decode(preds_index, length_for_pred)


            log = open(f'./log_demo_score.txt', 'a')
            # dashed_line = '-' * 60
            # head = f'{"team1":10s}\t{"score":10s}\t{"team2":10s}\t{"score":10s}\tPitcher'

            # print(f'{dashed_line}\n{head}\n{dashed_line}')
            # log.write(f'{dashed_line}\n{head}\n{dashed_line}\n')

            preds_prob = F.softmax(preds, dim=2)
            preds_max_prob, _ = preds_prob.max(dim=2)

            # 후처리 단어 모음
            team_list_path = opt.input_folder_postprocess + 'team.txt'
            team_words = pp.read_domain_words(team_list_path)
            number_list_path = opt.input_folder_postprocess + 'number.txt'
            number_words = pp.read_domain_words(number_list_path)
            player_list_path = opt.input_folder_postprocess + 'player_kbsn0707.txt'
            player_words = pp.read_domain_words(player_list_path)


            # pred 모음 여기서 for로 출력함
            for idx, (img_name, pred, pred_max_prob) in enumerate(zip(image_path_list, preds_str, preds_max_prob)):
                if 'Attn' in opt.Prediction:
                    pred_EOS = pred.find('[s]')
                    pred = pred[:pred_EOS]  # prune after "end of sentence" token ([s])
                    pred_max_prob = pred_max_prob[:pred_EOS]
  
                confidence_score = pred_max_prob.cumprod(dim=0)[-1]

                if (idx == 0 or idx == 2):
                    if not pp.is_word_in_domain(pred, team_words):
                        final_word = pp.find_closest_domain_word(pred, team_words)
                        pred = final_word
                elif (idx == 1 or idx == 3):
                    if not helper.is_number(pred):
                        final_word = pp.find_closest_domain_word(pred, number_words)
                        pred = final_word
                else :
                    if not pp.is_word_in_domain(pred, player_words):
                        final_word = pp.find_closest_domain_word(pred, player_words)
                        pred = final_word

                print(f'{img_name:25s}\t{pred:25s}\t{confidence_score:0.4f}')
                scoreboard_list.append(pred)
                total_confidence_score+=confidence_score
            
            # 정확도 낮은 경우는 스코어보드 없는 것이라 판단
            img_len = len(scoreboard_list)
            avg_confidence_score = total_confidence_score/img_len
            if(avg_confidence_score<=0.8):
                scoreboard_list = []
                return scoreboard_list
            elif former_score_list == scoreboard_list and base_status == former_base_status: # 이전과 경기 결과 같으면 추가 안함
                return scoreboard_list

            else:
                if img_len == 5:
                    log.write(f'{scoreboard_list[0]:10s}\t{scoreboard_list[1]:10s}\t{scoreboard_list[2]:10s}\t{scoreboard_list[3]:10s}\t{scoreboard_list[4]}\t\t{base_status}\n')
                    helper.text2json(scoreboard_list,base_status,opt.json_path, frame_count,pitcher=True)
                else:
                    log.write(
                        f'{scoreboard_list[0]:10s}\t{scoreboard_list[1]:10s}\t{scoreboard_list[2]:10s}\t{scoreboard_list[3]:10s}\t\t{base_status}\n')
                    helper.text2json(scoreboard_list, base_status, opt.json_path,frame_count)
                log.close()


    end = time.time()
    print("time", end - start)
    return scoreboard_list



