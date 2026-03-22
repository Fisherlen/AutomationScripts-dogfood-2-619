"""
20250908 Monday
执行记录：已跑通。
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

def test_baidu():
    """
    更精确地测试百度搜索"手机"页面中的广告是否包含"京东"
    """
    # 初始化浏览器驱动
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # 1. 打开百度网页
        print("打开百度网页...")
        driver.get("https://www.baidu.com/")

        # 2. 在搜索框中输入"手机"
        print("输入搜索关键词'手机'...")
        search_box = driver.find_element(By.ID, "chat-textarea")
        search_box.clear()
        search_box.send_keys("手机")
        search_box.send_keys(Keys.RETURN)

        # 4. 等待广告加载（广告通常加载较慢）
        print("等待广告加载...")
        time.sleep(5)

        # 5. 查找百度广告元素
        # 百度广告通常有特定的标记
        ad_contents = []

        # 查找带有广告标记的元素
        ad_indicators = driver.find_elements(By.XPATH, "//*[contains(text(), '广告') or contains(text(), '广告')]")

        for indicator in ad_indicators:
            # 获取广告容器
            try:
                # 向上查找广告容器
                ad_container = indicator.find_element(By.XPATH, "./ancestor::*[contains(@class, 'c-container') or contains(@class, 'result') or contains(@class, 'ad')]")
                ad_contents.append(ad_container.text)
            except:
                # 如果找不到容器，就取指示器附近的文本
                ad_contents.append(indicator.text)

        # 查找明确标记为广告的容器
        explicit_ads = driver.find_elements(By.CSS_SELECTOR, "[data-tpl='ad'], .c-container[tpl='ad'], .ecom_ad")
        for ad in explicit_ads:
            ad_contents.append(ad.text)

        # 合并所有广告内容
        all_ad_text = " ".join(ad_contents)
        print(f"收集到的广告内容: {all_ad_text[:300]}...")

        # 6. 检查是否包含"京东"
        if "京东" in all_ad_text:
            print("测试通过：广告中包含'京东'")
            return True
        else:
            print("测试失败：广告中不包含'京东'")
            return False

    except TimeoutException:
        print("测试失败：页面加载超时")
        return False
    except Exception as e:
        print(f"测试执行出错: {str(e)}")
        return False
    finally:
        # 关闭浏览器
        driver.quit()
        print("浏览器已关闭")

if __name__ == "__main__":
    # 运行简化版本
    test_baidu()
