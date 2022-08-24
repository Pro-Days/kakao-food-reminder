import requests
from bs4 import BeautifulSoup
import re


def cmd():

    message = str(input("명령어: "))
    if message == "급식":
        lunch()

    elif message == "도움말":
        print(f"[ 도움말 ]\n\n급식\n-> 날짜: 1~31")

# [ 도움말 ]
#
# 급식
# -> 날짜: 1~31

    else:
        wrong(3)


def lunch():
    date = int(input("날짜: "))
    if 31 >= date >= 1:
        url = 'http://icpa.icehs.kr/foodlist.do?m=070306&s=icpa'

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        meal(soup, date)

        cmd()
    else:
        wrong(5)


def allergy(numbers):
    for i in range(len(numbers)):
        for j in range(len(numbers[i])):
            if numbers[i][j] == "1":
                numbers[i][j] = "난류"
            if numbers[i][j] == "2":
                numbers[i][j] = "우유"
            if numbers[i][j] == "3":
                numbers[i][j] = "메밀"
            if numbers[i][j] == "4":
                numbers[i][j] = "땅콩"
            if numbers[i][j] == "5":
                numbers[i][j] = "대두"
            if numbers[i][j] == "6":
                numbers[i][j] = "밀"
            if numbers[i][j] == "7":
                numbers[i][j] = "고등어"
            if numbers[i][j] == "8":
                numbers[i][j] = "게"
            if numbers[i][j] == "9":
                numbers[i][j] = "새우"
            if numbers[i][j] == "10":
                numbers[i][j] = "돼지"
            if numbers[i][j] == "11":
                numbers[i][j] = "복숭아"
            if numbers[i][j] == "12":
                numbers[i][j] = "토마토"
            if numbers[i][j] == "13":
                numbers[i][j] = "아황산류"
            if numbers[i][j] == "14":
                numbers[i][j] = "호두"
            if numbers[i][j] == "15":
                numbers[i][j] = "닭고기"
            if numbers[i][j] == "16":
                numbers[i][j] = "쇠고기"
            if numbers[i][j] == "17":
                numbers[i][j] = "오징어"
            if numbers[i][j] == "18":
                numbers[i][j] = "조개류(굴, 전복, 홍합 포함)"
            if numbers[i][j] == "19":
                numbers[i][j] = "잣"
    return numbers


def wrong(n):
    print(f"잘못된 입력입니다. (오류번호: {n})\n")
    cmd()


def meal(soup, date):
    target_table = soup.find("table", "tb_calendar")
    tds = target_table.find_all('td')

    try:
        td = tds[date-1]
    except:
        wrong(4)
    finally:
        ul = str(td.find("ul"))
        ul = ul.replace("<ul>\n", "")
        ul = ul.replace("\t", "")
        ul = ul.replace("</ul>", "")
        ul = ul.split("<br/>")

        info = ul[-1]
        ul = ul[:-2]

        meal = ul

        if meal == []:
            no_meal(date)
        else:
            numbers = []

            for i in range(len(meal)):
                numbers.append(re.findall(r'\d+', meal[i]))
                meal[i] = re.sub(r'\d+', '', meal[i])

            for i in range(len(meal)):
                meal[i] = meal[i].replace(" ", "")
                meal[i] = meal[i].replace("OV", "")
                meal[i] = meal[i].replace(".", "")

            # print(numbers)
            # print(meal)

            numbers = allergy(numbers)

            # print(numbers)

            meal_str = ""

            for i in range(len(meal)):
                meal_str += meal[i] + "  |  알레르기: "
                # print(numbers[i])
                if numbers[i] != []:
                    for j in range(len(numbers[i])):
                        meal_str += str(numbers[i][j]) + ", "
                else:
                    # print("else")
                    meal_str += "없음, "
                meal_str = meal_str[:-2]
                meal_str += "\n"
            meal_str += "\n" + info
            print(f"\n{date}일 중식메뉴\n{meal_str}\n")


def no_meal(date):
    print(f"\n{date}일 중식메뉴\n\n정보 없음\n")


cmd()
