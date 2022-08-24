from selenium import webdriver
import re


options = webdriver.ChromeOptions()
options.add_argument('--window-size=1024,768')

global driver

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

driver.get('http://icpa.icehs.kr/main.do')

print('ready')


def loop():

    message = input("명령어: ")

    if message == '!급식':

        global driver

        meal_list = driver.find_element_by_class_name('meal_list')

        meal = meal_list.text.split("\n")

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

        print("\n" + meal_str)


while True:
    loop()
