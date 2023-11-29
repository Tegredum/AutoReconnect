import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import json
import datetime
from selenium.common.exceptions import ElementNotInteractableException

def check_internet(url: str) -> bool:
    try:
        requests.get(url, timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        return False
    
def connect_wifi(ssid: str) -> None:
    try:
        # 使用 netsh 命令连接 ZJUWLAN
        subprocess.run(f"netsh wlan connect \"{ssid}\"", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"连接 ZJUWLAN 失败，错误信息：{e}")

def login_net_zju(username: str, password: str) -> None:
    # 使用 Selenium 打开浏览器并登录 net.zju.edu.cn
    driver: webdriver.Chrome = webdriver.Chrome()
    driver.get("https://net2.zju.edu.cn/srun_portal_pc?ac_id=69&theme=zju")
    time.sleep(10)

    # 找到用户名与密码输入框并输入
    try:
        driver.find_element(By.ID, "username").send_keys(username)
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(1)

        driver.find_element(By.ID, "login").click()
        time.sleep(5)
    except ElementNotInteractableException as e:
        print(f"找不到元素，错误信息：{e}")

    driver.close()

if __name__ == "__main__":
    while True:
        if not check_internet("https://www.baidu.com"):
            connect_wifi("ZJUWLAN")
            # 从 JSON 文件中读取学号与密码
            with open("credentials.json", "r") as f:
                credentials = json.load(f)
                username: str = credentials["username"]
                password: str = credentials["password"]
                login_net_zju(username, password)
        else:
            print(f"网络正常，当前时间：{datetime.datetime.now()}")
            time.sleep(3600)