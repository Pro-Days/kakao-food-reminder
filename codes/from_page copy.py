from selenium import webdriver
# import time
import requests
from bs4 import BeautifulSoup
import re
import datetime


options = webdriver.ChromeOptions()
options.add_argument('--window-size=1024,768')

global driver

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

driver.get('http://icpa.icehs.kr/main.do')

print('ready')


def loop():

    message = input("명령어: ")
    message = message.split()
    # print(message)

    # if message[0] == '!급식_셀레니움':
    #     pass

    #     global driver

    #     driver.get('http://icpa.icehs.kr/foodlist.do?m=070306&s=icpa')

    #     day = time.strftime('%d', time.localtime(time.time()))

    #     print(driver.text)

    #     today_meal = driver.find_element_by_xpath(
    #         '//*[@id="con_body"]/div[3]/table/tbody/tr[19]/td/a')

    if message[0] == "급식":
        try:
            if message[1] == "중식":
                lunch()
            elif message[1] == "석식":
                dinner()
            else:
                wrong(1)
        except:
            wrong(2)

    elif message[0] == "도움말":
        print(f"[ 도움말 ]\n\n급식 <중식 / 석식>\n-> 날짜: (YYYY.MM.DD or MM.DD or DD or 오늘)")

# [ 도움말 ]
#
# 급식 <중식 / 석식>
# -> 날짜: 1~31

    else:
        wrong(3)


def lunch():
    # http://icpa.icehs.kr/foodlist.do?year=2019&month=10&m=070306&s=icpa
    date = str(input("날짜: "))

    if date == "오늘":
        url = 'http://icpa.icehs.kr/foodlist.do?m=070306&s=icpa'

        datetime = datetime.datetime.now()
        year = datetime.year
        month = datetime.month
        date = datetime.day

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        meal(soup, year, month, date)

        loop()
    else:
        date = date.split(".")
        if len(date) == 1:
            try:
                date = int(date)
            except:
                wrong(7)
            finally:
                if 31 >= date >= 1:
                    url = 'http://icpa.icehs.kr/foodlist.do?m=070306&s=icpa'

                    datetime = datetime.datetime.now()
                    year = datetime.year
                    month = datetime.month

                    response = requests.get(url)
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    meal(soup, year, month, date)

                    loop()
                else:
                    wrong(5)
        elif len(date) == 2:
            try:
                date[0] = int(date[0])
                date[1] = int(date[1])
            except:
                wrong(8)
            finally:
                if 1 <= date[0] <= 12 and 31 >= date[1] >= 1:
                    url = 'http://icpa.icehs.kr/foodlist.do?m=070306&s=icpa'

                    datetime = datetime.datetime.now()
                    year = datetime.year
                    month = date[0]
                    date = date[1]

                    response = requests.get(url)
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    meal(soup, year, month, date)

                    loop()
                else:
                    wrong(9)


def dinner():
    # print("dinner")
    date = int(input("날짜: "))
    if 31 >= date >= 1:
        # print("date")
        global driver

        driver.get('http://icpa.icehs.kr/foodlist.do?m=070306&s=icpa')

        dinner_button = driver.find_element_by_xpath('//*[@id="D"]')
        dinner_button.click()

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        meal(soup, date)

        loop()

    else:
        wrong(6)


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
    loop()


def meal(soup, year, month, date):
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
    print(f"\n{date}일 메뉴\n\n정보 없음\n")


loop()

# 199
