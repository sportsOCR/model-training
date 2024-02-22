# model-training
Clovaai [deep-text-recognition-benchmark](https://github.com/clovaai/deep-text-recognition-benchmark)를 참고하여 프로젝트 진행
## About The Project

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
```
python create_lmdb_dataset.py --inputPath data/ --gtFile data/gt.txt --outputPath result/
```   
4. `train.py`
## Training
