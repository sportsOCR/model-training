import json

file = json.load(open('./korean_dataset/Textinwild/textinthewild_data_info.json', 'rt', encoding='UTF8'))

# print(file.keys())#dict_keys(['info', 'images', 'annotations', 'licenses'])
# print(file['info']) #{'name': 'Text in the wild Dataset', 'date_created': '2019-10-14 04:31:48'}
# print(type(file['images'])) #list
#
# print(file['images'][:3])

import random
import os

ocr_good_files = os.listdir('./korean_dataset/Textinwild/Signboard')
print(len(ocr_good_files))

random.shuffle(ocr_good_files)

n_train = int(len(ocr_good_files) * 0.7)
n_validation = int(len(ocr_good_files) * 0.15)
n_test = int(len(ocr_good_files) * 0.15)

print(n_train, n_validation, n_test) # 26054 5583 5583

train_files = ocr_good_files[:n_train]
validation_files = ocr_good_files[n_train: n_train+n_validation]
test_files = ocr_good_files[-n_test:]
print("check1")
## train/validation/test 이미지들에 해당하는 id 값을 저장

train_img_ids = {}
validation_img_ids = {}
test_img_ids = {}

for image in file['images']:
    if image['file_name'] in train_files:
        train_img_ids[image['file_name']] = image['id']
    elif image['file_name'] in validation_files:
        validation_img_ids[image['file_name']] = image['id']
    elif image['file_name'] in test_files:
        test_img_ids[image['file_name']] = image['id']

print("check2")
## train/validation/test 이미지들에 해당하는 annotation 들을 저장

train_annotations = {f:[] for f in train_img_ids.keys()}
validation_annotations = {f:[] for f in validation_img_ids.keys()}
test_annotations = {f:[] for f in test_img_ids.keys()}

train_ids_img = {train_img_ids[id_]:id_ for id_ in train_img_ids}
validation_ids_img = {validation_img_ids[id_]:id_ for id_ in validation_img_ids}
test_ids_img = {test_img_ids[id_]:id_ for id_ in test_img_ids}
print("check4")

for idx, annotation in enumerate(file['annotations']):
    if idx % 5000 == 0:
        print(idx,'/',len(file['annotations']),'processed')
    # if annotation['attributes']['type'] != '단어(어절)':
    if annotation['attributes']['class'] != 'word':
        continue
    if annotation['image_id'] in train_ids_img:
        train_annotations[train_ids_img[annotation['image_id']]].append(annotation)
    elif annotation['image_id'] in validation_ids_img:
        validation_annotations[validation_ids_img[annotation['image_id']]].append(annotation)
    elif annotation['image_id'] in test_ids_img:
        test_annotations[test_ids_img[annotation['image_id']]].append(annotation)

print("check5")
with open('train_annotation.json', 'w') as file:
    json.dump(train_annotations, file)
with open('validation_annotation.json', 'w') as file:
    json.dump(validation_annotations, file)
with open('test_annotation.json', 'w') as file:
    json.dump(test_annotations, file)