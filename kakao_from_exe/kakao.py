import os
import pyautogui
import pyperclip
import platform
import subprocess
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time


options = webdriver.ChromeOptions()
options.add_argument('--window-size=1024,768')

global driver

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)


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
        elif message[1] == "모두":
            date = int(input("날짜: "))+3
            return lunch_and_dinner(date)
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
    msg = lunch_menu + "\n\n" + "-"*20 + "\n\n" + dinner_menu
    # print(msg)
    return msg


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

        info = ul[-1]
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
            print(meal)

            numbers = allergy(numbers)

            # print(numbers)

            meal_str = ""

            for i in range(len(meal)):
                meal_str += meal[i]
                meal_str += "\n"

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
            meal_str += "\n" + info
            menu = f"{date-3}일 {meal_type}메뉴\n\n\n{meal_str}"
            return menu


def no_meal(date, meal_type):
    print(f"\n{date}일 메뉴\n\n정보 없음\n")


# Config changed by OS
cmd_key = 'ctrl'
home_key = ('home', '')

if __name__ == "__main__":
    msg = cmd()
    # print(msg)
    talk_result = talk_check(msg)
    if talk_result:
        exit(0)
    else:
        exit(1)
