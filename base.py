import cv2

def where_base(tmp_img_path, channel):
    # 이미지를 그레이스케일로 로드
    img_original = cv2.imread(tmp_img_path, cv2.IMREAD_GRAYSCALE)  # 실제 경로로 수정 필요
    bases_status = []

    if channel == 'mbc':
        # 베이스 중심 좌표
        base_centers = [(263, 245), (242, 225), (220, 245)]
        gray_threshold = 225

        for idx, (x, y) in enumerate(base_centers, start=1):
            pixel_val = img_original[y, x]
            if pixel_val < gray_threshold:
                bases_status.append(f"{idx}루")

    elif channel == 'kbsn':
        base_centers = [(1784, 904), (1760, 809), (1738, 904)]
        gray_threshold = 100

         # 각 베이스의 중심에 대한 그레이스케일 값을 검사
        for idx, (x, y) in enumerate(base_centers, start=1):
            pixel_val = img_original[y, x]
            if pixel_val > gray_threshold:
                bases_status.append(f"{idx}루")

    # 결과 출력
    status = ' '.join(bases_status) if bases_status else "베이스 없음"
    return status