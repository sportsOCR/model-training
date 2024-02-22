import cv2
import os

import base
import cropping
import ocr_recognition

def extract_frames(opt):
    interval = 300
    score_list = []
    former_base_status = 0
    # 동영상 파일 열기
    cap = cv2.VideoCapture(opt.input_video)
    print("open video")

    if not cap.isOpened():
        print("동영상 파일을 열 수 없습니다.")
        return

    # 출력 폴더가 없으면 생성
    if not os.path.exists(opt.input_folder_image):
        os.makedirs(opt.input_folder_image)

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # interval 초마다 프레임 저장
        if frame_count % interval == 0:
            output_path = os.path.join(opt.input_folder_image, f"{frame_count}_img.png")
            cv2.imwrite(output_path, frame)
            base_status = base.where_base(output_path, opt.channel)

            cropping.crop_and_save_image(opt, frame_count)
            score_list = ocr_recognition.demo(opt,score_list, base_status, former_base_status, frame_count)
            if not score_list:
                print("점수판이 존재하지 않습니다.")

        frame_count += 1
        former_base_status = base_status
    cap.release()
    print("프레임 추출이 완료되었습니다.")