import json


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

## 인식된 text를 json으로 변경하는 함수
def text2json(list, base,json_path, frame_count,pitcher= False):

    if not pitcher:
        version = {
        "team1" : {
            "name": list[0],
            "score" : list[1]
            },
        "team2" : {
            "name": list[2],
            "score" : list[3]
            },
        "Pitcher" : list[4],
        "base" : base
        }
    else:
        version = {
            "team1": {
                "name": list[0],
                "score": list[1]
            },
            "team2": {
                "name": list[2],
                "score": list[3]
            },
            "base": base
        }
    with open(json_path, 'a', encoding='utf-8') as file:
        if file.tell() == 0:  # 파일이 비어있으면
            file.write("{" + '"' + str(frame_count)+'" :')  # 맨 앞에 '{' 추가
        else:
            file.write(',' + '"' + str(frame_count)+'" :')  # 파일이 비어있지 않으면 이전 객체와 현재 객체 사이에 쉼표 추가
        json.dump(version, file, ensure_ascii=False, indent=2)
        # file.write('}')  # 맨 뒤에 '}' 추가