from collections import Counter
import math
import numpy as np


### 후처리

def cosine_similarity(str1, str2):
    words1 = Counter(str1)
    words2 = Counter(str2)

    common = set(words1.keys()) & set(words2.keys())

    dot_product = sum(words1[word] * words2[word] for word in common)
    magnitude1 = math.sqrt(sum(count ** 2 for count in words1.values()))
    magnitude2 = math.sqrt(sum(count ** 2 for count in words2.values()))

    if magnitude1 * magnitude2 == 0:
        return 0  # 방지: 제로 나누기

    return dot_product / (magnitude1 * magnitude2)

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = np.arange(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = distances.copy()
        distances[1:] = np.minimum(distances[1:], distances[:-1] + 1)
        distances[1:] = np.minimum(distances[1:], distances_[:-1] + (s1 != c2))
        distances[0] = i2 + 1
    return distances[-1]

def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) if union else 0


def read_domain_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def is_word_in_domain(word, domain_words):
    return word in domain_words


def correct_ocr_errors(ocr_word, domain_words):
    lev_closest_word = None
    cos_closest_word = None
    min_lev_distance = float('inf')
    max_cos_distance = float('-inf')

    for domain_word in domain_words:
        # 레벤슈타인 거리 계산
        lev_distance = levenshtein_distance(ocr_word, domain_word)
        if lev_distance < min_lev_distance:
            min_lev_distance = lev_distance
            lev_closest_word = domain_word

        # 코사인 유사도 계산
        cos_distance = cosine_similarity(ocr_word, domain_word)
        if cos_distance > max_cos_distance:
            max_cos_distance = cos_distance
            cos_closest_word = domain_word

    return cos_closest_word

def find_closest_domain_word(ocr_word, domain_words):

    best_match = None
    highest_cosine_similarity = float('-inf')  # 가장 높은 코사인 유사도를 저장하기 위한 변수
    highest_combined_similarity = float('-inf')

    for domain_word in domain_words:
        # 코사인 유사도 계산
        cosine_sim = cosine_similarity(ocr_word, domain_word)
        jaccard_sim = jaccard_similarity(ocr_word, domain_word)
        # Debugging: 각 단어와 그에 대한 코사인 유사도를 출력합니다.
        # print(f"Domain word: {domain_word}, Cosine Similarity: {cosine_sim}")
        # print(f"Domain word: {domain_word}, Jaccard Similarity: {jaccard_sim}")

        # # 코사인 유사도가 현재까지 찾은 가장 높은 유사도보다 높은 경우 업데이트
        # if cosine_sim > highest_cosine_similarity:
        #     highest_cosine_similarity = cosine_sim
        #     best_match = domain_word

        combined_similarity = cosine_sim + jaccard_sim
        if combined_similarity > highest_combined_similarity:
            highest_combined_similarity = combined_similarity
            best_match = domain_word
            # print(f"Best match : {best_match}_voting")

    # Debugging: 최종 선택된 단어와 그의 코사인 유사도를 출력합니다.
    print(f"Error word: {ocr_word}, Highest Cosine Similarity: {highest_cosine_similarity}")

    return best_match if best_match else ocr_word