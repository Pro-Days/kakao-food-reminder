########################################
# 배포 시 19, 20줄에 있는 ID, 비밀번호 수정 후 배포
########################################


import time
from selenium import webdriver
import re
from bs4 import BeautifulSoup
import subprocess
import platform
import pyperclip
import pyautogui
import os
import requests
import json

#############
kakao_id = "joohjdays@kakao.com"
kakao_password = "tj2538123"
#############

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1000,1000')

global driver

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

driver.get('https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=bd64ff1830b58542a2c2be786ab2bab1&redirect_uri=https://example.com/oauth')


rest_api_key = 'bd64ff1830b58542a2c2be786ab2bab1'
redirect_uri = 'https://example.com/oauth'
url_token = 'https://kauth.kakao.com/oauth/token'

driver.find_element_by_id(
    'id_email_2').send_keys(kakao_id)
driver.find_element_by_id(
    'id_password_3').send_keys(kakao_password)


print("\n\n로그인을 진행해주세요\n\n")


loading = True
while loading:
    try:
        current_url = driver.current_url
        authorize_code = current_url.split("code=")[1]
    except:
        time.sleep(1)
    else:
        loading = False

# 신규 발급
param = {
    'grant_type': 'authorization_code',
    'client_id': rest_api_key,
    'redirect_uri': redirect_uri,
    'code': authorize_code,  # 한번 발급되면 authorize_code는 무효화됩니다.
}

response = requests.post('https://kauth.kakao.com/oauth/token', data=param)
# token 발급 api로 발급된 정보들을 kakao_token.json 파일에 저장합니다.
tokens = response.json()


def msg_to_me(data, tokens):
    template = generate_json(data)
    print(template)
    # with open("temp.txt", "w", encoding="UTF-8") as f:
    #     f.write(f"lunch: {str(lunch)}\n\ndinner: {str(dinner)}")

    # with open("kakao_token.json", "r") as fp:
    #     tokens = json.load(fp)
    #     print(tokens["access_token"])

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": "Bearer " + tokens["access_token"]
    }

    # with open("contents.json", "r") as template:
    data = {
        "template_object": json.dumps(template)
    }

    # 메시지 전송
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


def generate_json(data):
    menu, energy, date, type = data[0], data[1], data[2], data[3]

    data = {}
    data["object_type"] = "text"
    data['title'] = f"{date}일 {type}메뉴"
    data['description'] = f"설명asd"
    data['text'] = f"메뉴"
    data['link'] = {
        "web_url": "www.naver.com",
        "mobile_web_url": "www.naver.com"
    }
    data["buttons"] = [
        {
            "title": "웹으로 이동",
            "link": {
                "web_url": "www.naver.com",
                "mobile_web_url": "www.naver.com"
            }
        }
    ]

    # 리스트는 최대 3개까지

    # data = {}
    # data["object_type"] = "list"
    # data["header_title"] = f"{date}일 {type}메뉴"
    # data["header_link"] = {
    #     "web_url": "www.naver.com",
    #     "mobile_web_url": "www.naver.com"
    # }

    # data['contents'] = []

    # for i in range(len(menu)):
    #     data['contents'].append({
    #         "title": f"{i+1}. {menu[i]}",
    #         "description": f"설명{i+1}",
    #         "image_url": "",
    #         "image_width": 50, "image_height": 50,
    #         "link": {
    #             "web_url": "www.naver.com",
    #             "mobile_web_url": "www.naver.com"
    #         }
    #     })

    # data["buttons"] = [
    #     {
    #         "title": "웹으로 이동",
    #         "link": {
    #             "web_url": "www.naver.com",
    #             "mobile_web_url": "www.naver.com"
    #         }
    #     }
    # ]
    return data


###################
###################
###################
###################
###################
###################
###################
###################
###################
###################
###################


def initialize():
    print(pyautogui.size())
    pyautogui.PAUSE = 0.5
    python_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(python_path)


# KakaoTalk path is set only to default install path
def get_kakao_cmd():
    user_os = platform.system()
    kakao_path = ['C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe']
    if user_os == 'Darwin':
        kakao_path = ['open', '-a', 'KakaoTalk']
    return kakao_path


def run_kakao():
    kakao_path = get_kakao_cmd()
    print(f'Run KakaoTalk : {kakao_path}')
    try:
        subprocess.run(kakao_path)
    except Exception:
        print('[ERROR] Execute Kakaotalk')
        raise


def enter_chatroom(chat_name):
    # enter_chat_category()
    click_img('search_button.png')
    pyperclip.copy(chat_name)
    pyautogui.hotkey(cmd_key, 'v')
    pyautogui.press('enter')


# Return response to sending msg (Need Cursor check)
def send_msg(msg):
    pyperclip.copy(msg)
    pyautogui.hotkey(cmd_key, 'v')
    pyautogui.press('enter')


def click_img(png_name):
    img_path = os.path.join('img', png_name)
    time.sleep(1)
    location = pyautogui.locateCenterOnScreen(img_path, confidence=0.7)
    x, y = location
    # if is_retina:
    #     x = x / 2
    #     y = y / 2
    pyautogui.moveTo(x, y)
    pyautogui.click()


def talk_check(my_msg):
    initialize()
    """Set chatroom index and message below
        Example like this
        chatroom_idx = 1
        my_msg = 'test'
    """
    # chat_name = "2-3 쌤없는 반톡"
    # chat_name = "ICPA 2-3"
    chat_name = "주현재"
    # chat_name = "이재원"

    run_kakao()
    enter_chatroom(chat_name)
    send_msg(my_msg)
    return True
    # try:
    #     run_kakao()
    #     enter_chatroom(chat_name)
    #     send_msg(my_msg)
    #     return True
    # except Exception as e:
    #     print(f'Error: {e}')
    #     return False


def cmd():

    message = str(input("명령어: "))
    message = message.split()
    if message[0] == "급식":
        if message[1] == "중식":
            date = int(input("날짜: "))+3
            return lunch(date)
        elif message[1] == "석식":
            date = int(input("날짜: "))+3
            return dinner(date)
        # elif message[1] == "모두":
        #     date = int(input("날짜: "))+3
        #     return lunch_and_dinner(date)
        else:
            wrong(10)

    elif message[0] == "도움말":
        print(f"[ 도움말 ]\n\n급식 <중식 or 석식>\n-> 날짜: 1~31")

# [ 도움말 ]
#
# 급식
# -> 날짜: 1~31

    else:
        wrong(3)


def lunch(date):
    if 31 >= date >= 1:
        url = 'http://icpa.icehs.kr/foodlist.do?m=070306&s=icpa'

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return meal(soup, date, "중식")
    else:
        wrong(5)


def dinner(date):
    # print("dinner")
    if 31 >= date >= 1:
        # print("date")
        global driver

        driver.get('http://icpa.icehs.kr/foodlist.do?m=070306&s=icpa')

        dinner_button = driver.find_element_by_xpath('//*[@id="D"]')
        dinner_button.click()

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        return meal(soup, date, "석식")
    else:
        wrong(6)


def lunch_and_dinner(date):
    lunch_menu = lunch(date)
    dinner_menu = dinner(date)
    # print(lunch_menu)
    # print("\n\n\n")
    # print(dinner_menu)
    # print("\n\n\n")
    # msg = lunch_menu + "\n\n" + "-"*20 + "\n\n" + dinner_menu
    # print(msg)
    return lunch_menu, dinner_menu


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


def meal(soup, date, meal_type):
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

        energy = ul[-1]
        print(energy)
        ul = ul[:-2]

        meal = ul

        if meal == []:
            no_meal(date, meal_type)
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

            # -> str

            # meal_str = ""

            # for i in range(len(meal)):
            #     meal_str += meal[i]
            #     meal_str += "\n"

            # for i in range(len(meal)):
            #     meal_str += meal[i] + "  |  알레르기: "
            #     # print(numbers[i])
            #     if numbers[i] != []:
            #         for j in range(len(numbers[i])):
            #             meal_str += str(numbers[i][j]) + ", "
            #     else:
            #         # print("else")
            #         meal_str += "없음, "
            #     meal_str = meal_str[:-2]
            #     meal_str += "\n\n"
            # meal_str += "\n" + energy
            # menu = f"{date-3}일 {meal_type}메뉴\n\n\n{meal_str}"
            # return menu

            # -> list
            return_list = [meal, energy, date-3, meal_type]
            return return_list


def no_meal(date, meal_type):
    print(f"\n{date}일 {meal_type}메뉴\n\n정보 없음\n")


# Config changed by OS
cmd_key = 'ctrl'
home_key = ('home', '')

if __name__ == "__main__":
    menu = cmd()
    # print(msg)
    msg_to_me(menu, tokens)
    # talk_result = talk_check(msg)
    # if talk_result:
    #     exit(0)
    # else:
    #     exit(1)
