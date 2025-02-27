# 西南交通大学教务网抢课脚本
# 仅适用于优选班抢课
# 尚未完成(见115行代码)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# 配置信息
USERNAME = "************"
PASSWORD = "************"
LOGIN_URL = "http://jwc.swjtu.edu.cn/service/login.html"
TARGET_COURSE = "互联网搜索引擎"


def main():
    # 初始化浏览器
    driver = webdriver.Chrome()
    # driver.maximize_window()
    print("浏览器已启动")

    try:
        # 打开登录页面
        driver.get(LOGIN_URL)

        # 点击统一账号登录
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'学校统一账号登录')]"))
        ).click()

        # 输入用户名密码
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='交大ID/手机/邮箱']"))
        )
        password_input = driver.find_element(By.XPATH, "//input[@placeholder='请输入密码']")

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        # 点击登录
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='登录']"))
        ).click()
        print('成功登录')

        time.sleep(10)

        # 进入选课菜单
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(),'网上选课')]"))
        ).click()
        print('网上选课')

        # 切换到iframe
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//iframe')))
        driver.switch_to.frame(iframe)
        print('成功切换到iframe')

        # time.sleep(5)

        # 进入优选班选课
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'按优选班选课')]"))
        ).click()
        print('按优选班选课')

        # 开始监控
        while True:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 开始检查课程名额...")

            # 查找目标课程行
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//tr[.//span[contains(@id,'courseName')]]"))
            )

            target_row = None
            for row in rows:
                if TARGET_COURSE in row.text:
                    target_row = row
                    break

            if target_row:
                # 检查名额
                quota_cell = target_row.find_elements(By.XPATH, "./td")[10]  # 第11个td
                current, total = map(int, quota_cell.text.strip().split("/"))

                if current < total:
                    print(f"检测到有空位: {current}/{total}，尝试选课")

                    # 点击选课按钮
                    select_btn = target_row.find_element(By.XPATH, ".//input[@value='选课']")
                    select_btn.click()

                    # 处理确认弹窗
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@value='确认选课']"))
                    ).click()

                    print("选课成功！")
                    return
                else:
                    print(f"当前名额已满: {current}/{total}")
            else:
                print("未找到目标课程")

            # 等待1分钟
            print("等待下一次检查...")
            time.sleep(60)

            # 刷新页面
            # ---------------------------------------------------------------- 
            driver.refresh()
            # ---------------------------------------------------------------- 应改为点击刷新按钮

    finally:
        print('waiting')
        time.sleep(1000)
        driver.quit()


if __name__ == "__main__":
    main()
