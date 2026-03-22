"""
20250907 Sunday
传统自动化测试方法 -- 传统方法没使用大模型=传统方法没使用大模型=传统方法没使用大模型
执行记录：这段代码是根据通义的指引修改完成，有一部分代码已经做了修改
需要登梯子
"""
# --------------------------------------------------------------------------------
"""
案例:百度推广测试
1.打开网页 https://ww.baidu.com/
2.在输入框中输入手机，然后点击搜索按钮
3.返回第一页中所有包含广告的信息
结果:如果包含京东返回通过，否则返回失败安装:

预装：
1.执行命令 pip install selenium
2.下载浏览器驱动
        https://googlechromelabs.github.io/chrome-for-testing/#stable
        详细下载地址：
        https://storage.googleapis.com/chrome-for-testing-public/140.0.7339.80/win64/chromedriver-win64.zip
        留意：需要和我电脑WINDOWS匹配和64BIT才可 --> chromedriver.exe
3.拷贝chromedriver.exe到此项目所在的Python解释器目录中下：L:\Python\Python311
"""
# --------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time


def test_baidu():
    """
    更精确地测试百度搜索"手机"页面中的广告是否包含"百度"
    """
    # 初始化浏览器驱动
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # 使用以下代码自动管理 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 5)

    try:
        # 1. 打开百度网页
        print("打开百度网页...")
        driver.get("https://www.baidu.com/")

        # 2. 在搜索框中输入"手机"
        print("输入搜索关键词'手机'...")
        search_box = driver.find_element(By.ID, "kw")
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
        ad_indicators = driver.find_elements(By.XPATH, "//*[contains(text(), '广告')]")

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

        # 6. 检查是否包含"百度"
        if "百度" in all_ad_text:
            print("\n--》测试通过：广告中包含'百度'")
            return True
        else:
            print("\n--》测试失败：广告中不包含'百度'")
            return False


    except TimeoutException:
        print("测试失败：页面加载超时")
        return False
    except Exception as e:
        print(f"测试执行出错: {str(e)}")
        return False
    finally:
        # 等待30秒再关闭浏览器
        # print("等待30秒...")
        time.sleep(15)

        # 关闭浏览器
        driver.quit()
        print("\n\n浏览器已关闭")

if __name__ == "__main__":
    # 运行简化版本
    test_baidu()
