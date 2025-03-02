# 西南交通大学教务网抢课脚本
# 仅适用于优选班抢课
# 尚未完成(见115行代码)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from logger import get_logger
from bs4 import *

# 配置信息
USERNAME = "*************"
PASSWORD = "*************"
LOGIN_URL = "http://jwc.swjtu.edu.cn/service/login.html"
TARGET_COURSE = "现代铁路信息技术"

def Grab(driver, logger, target_course=TARGET_COURSE):
    """
    执行抢课操作
    
    参数:
        driver: WebDriver实例,用于浏览器操作
        logger: 日志记录器实例
        target_course: 目标课程名称,默认使用全局配置的TARGET_COURSE
    
    返回:
        bool: 是否成功抢到课程
    """
    # 进入选课菜单
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//p[contains(text(),'网上选课')]"))
    ).click()
    logger.info('网上选课')

    # 切换到iframe
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//iframe')))
    driver.switch_to.frame(iframe)
    logger.info('成功切换到iframe')

    # time.sleep(5)

    # 进入优选班选课
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'按优选班选课')]"))
    ).click()
    logger.info('按优选班选课')

    # 开始监控
    while True:
        logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 开始检查课程名额...")

        # 查找目标课程行
        try:
            # 显式等待元素存在且可见
            row = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, f"//span[text()='{target_course}']/parent::td/parent::tr"))
            )
            
            logger.info(f"成功找到目标课程: {target_course}")
        except Exception as e:
            logger.error(f"查找课程时出错: {str(e)}")
            row = []

        # 打印row的XPath信息
        logger.info(f"目标课程行的XPath: //tr[.//span[@id and contains(text(),'{target_course}')]]")
        
        target_row = row

        if target_row:
            # 检查名额
            quota_cell = target_row.find_elements(By.XPATH, "./td")[11]  # 第12个td
            current, total = map(int, quota_cell.text.strip().split("/"))

            if current < total:
                logger.info(f"检测到有空位: {current}/{total}，尝试选课")

                # 点击选课按钮
                select_btn = target_row.find_element(By.XPATH, ".//input[@value='选课']")
                select_btn.click()

                # 处理确认弹窗
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//input[@value='确定选课'])[2]"))
                ).click()

                logger.critical("选课成功！")
                return True
            else:
                logger.info(f"当前名额已满: {current}/{total}")
        else:
            logger.warning("未找到目标课程")

        # 等待半分钟
        logger.info("等待下一次检查...")
        time.sleep(30)

        # 刷新页面
        # 通过按钮的onclick属性中的reload关键字来定位刷新按钮
        try:
            refresh_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'reload')]"))
            )
            refresh_button.click()
            logger.info("点击刷新按钮成功")
        finally:
            pass
        # except Exception as e:
        #     logger.error(f"尝试点击刷新按钮失败: {e}")
        #     logger.info("回退到使用driver.refresh()方法")
        #     driver.refresh()

        #     Grab(driver, logger)

def main():
    # 初始化日志
    logger = get_logger(log_file='grab_class.log')
    
    # 初始化浏览器
    driver = webdriver.Chrome()
    # driver.maximize_window()
    logger.info("浏览器已启动")

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
        logger.info('成功登录')

        time.sleep(10)

        # 调用抢课函数，传入必要的参数
        success = Grab(driver, logger)
        if success:
            logger.info("抢课流程成功完成")

    finally:
        logger.info('程序等待中')
        time.sleep(1000)
        driver.quit()


if __name__ == "__main__":
    main()
