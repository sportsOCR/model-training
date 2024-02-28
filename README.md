# model-training
Clovaai [deep-text-recognition-benchmark](https://github.com/clovaai/deep-text-recognition-benchmark)를 참고하여 프로젝트 진행
## About The Project
본 프로젝트는 한국 방송사의 스포츠 중계 화면에 특화된 OCR(Optical Character Recognition) 모델 개발을 목표로 하고 있습니다.
- 프로젝트 개요

OCR 기술은 이미지나 영상 속의 문자를 인식하는 기술로, 문자 영역 검출과 문자 인식, 크게 두 단계의 프로세스로 구성됩니다. 전통적인 OCR(문서의 글자 인식)과 달리, 동적이고 복잡한 배경의 문자 인식 정확도 저하가 주요 문제점으로 대두되고 있습니다. 이러한 문제를 해결하기 위해, 영역 속의 글자를 인식하는 데 특화된 STR(Scene Text Recognition) 모델을 활용하였습니다.

- 모델 선정

OCR 모델 구조는 네이버 Clova AI가 제안한 STR 모델 중 가장 우수한 성능을 보여준 TPS-ResNet-BiLSTM-Attn 구조를 기반으로 하였습니다. 이 구조는 TPS(Thin Plate Spline) 기반의 변환, ResNet 기반의 특징 추출, BiLSTM 기반의 시퀀스 모델링, Attention 기반의 예측을 결합한 형태로, 복잡하거나 변형된 텍스트를 정확하게 인식하는 데 뛰어난 성능을 보여줍니다. 또한, `스포츠 중계 영상 내 문자 인식 모델의 성능 분석 연구 `논문의 실험을 통해 한국어 인식에 효과적임을 입증했습니다.

- 데이터셋 및 학습

기존에 영어 데이터셋(MJ, ST)으로 학습된 모델을 한국어 글자체 데이터셋을 활용하여 새롭게 학습하였습니다. 이를 통해 한글 텍스트에 대한 인식 능력을 향상 시키고, 스포츠 중계 화면에서 한글 정보를 더욱 정확하게 인실할 수 있게 되었습니다.

## Project Files Description
1. `dataset_preprocess.py`
    - 한글 데이터셋 저장 (from [AIHub](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=81))
    - Create Dataset Annotation File
2. `dataset_preprocess_2.py`
    - 1에서 생성한 Annotation File 통해 단어 단위로 crop후 save
    - Create gt.txt
  
      
    - 해당 블로그의 코드 참고함. [링크](https://cvml.tistory.com/21?category=854254)
3. `create_lmdb_dataset.py`
   - Create lmdb dataset
   - 폴더의 구조는 아래와 같아야 함.
   ```
   data
    ├── gt.txt
    └── test
      ├── word_1.png
      ├── word_2.png
      ├── word_3.png
      └── ...
   ```
   -  gt.txt의 구조는 아래와 같아야 함.
   ```
   test/word_1.png Tiredness
   test/word_2.png kills
   test/word_3.png A
   ...
   ```
   - 실행
    ```
    python create_lmdb_dataset.py --inputPath data/ --gtFile data/gt.txt --outputPath result/
    ```   
4. `train.py`
   - train start
   - 본 프로젝트에서는 TPS-ResNet-BiLSTM-Attn 구조 사용
     - 해당 내용은 논문 `스포츠 중계 영상 내 문자 인식 모델의 성능 분석 연구 ` 참고
    
    
   ```
   python train.py \
    --train_data data_lmdb_release/training --valid_data data_lmdb_release/validation \
    --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn
   ```


Please refer to the [link](https://github.com/clovaai/deep-text-recognition-benchmark) for more detailed information.
