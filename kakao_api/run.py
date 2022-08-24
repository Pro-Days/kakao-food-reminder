import json
from collections import OrderedDict

file_data = OrderedDict()

data = [['장조림버터볶음밥', '친환경쌀밥', '팽이버섯된장국', '삼색과일컵', '배추김치', '이-오',
         '아이돌인기샌드위치(/)'], ' * 에너지 : 889/단백질 : 41.6/칼슘 : 304.5/철 : 6.3', 15, '중식']
# dinner = [['쌀밥-자율', '돈코츠라멘(탕)', '장각탄두리치킨이력번호', '배추김치', '단무지-우동날'],
#   ' * 에너지 : 907.4/단백질 : 59.6/칼슘 : 157.7/철 : 3.2', 15, '석식']

menu, energy, date, type = data[0], data[1], data[2], data[3]


data = {}
data["object_type"] = "list"
data["header_type"] = f"{date}일 {type}메뉴"
data["header_link"] = {
    "web_url": "www.naver.com",
    "mobile_web_url": "www.naver.com"
}


data['contents'] = []

for i in range(len(menu)):
    data['contents'].append({
        "title": f"{i+1}. {menu[i]}",
        "description": f"설명{i+1}",
        "image_url": "",
        "image_width": 50, "image_height": 50,
        "link": {
            "web_url": "www.naver.com",
            "mobile_web_url": "www.naver.com"
        }
    })

data["buttons"] = [
    {
        "title": "웹으로 이동",
        "link": {
            "web_url": "www.naver.com",
            "mobile_web_url": "www.naver.com"
        }
    }
]
print(data)

with open("temp.json", 'w', encoding="UTF-8") as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
