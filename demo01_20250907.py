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
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


def get_ads_from_page(driver):
    """
    从当前页面获取所有广告信息
    """
    ads_info = []
    
    ad_indicators = driver.find_elements(By.XPATH, "//*[contains(text(), '广告')]")
    
    for indicator in ad_indicators:
        try:
            ad_container = indicator.find_element(By.XPATH, "./ancestor::*[contains(@class, 'c-container') or contains(@class, 'result') or contains(@class, 'ad')][1]")
            ad_text = ad_container.text.strip()
            if ad_text and ad_text not in ads_info:
                ads_info.append(ad_text)
        except:
            ad_text = indicator.text.strip()
            if ad_text and ad_text not in ads_info:
                ads_info.append(ad_text)
    
    explicit_ads = driver.find_elements(By.CSS_SELECTOR, "[data-tpl='ad'], .c-container[tpl='ad'], .ecom_ad, [data-click*='ad']")
    for ad in explicit_ads:
        ad_text = ad.text.strip()
        if ad_text and ad_text not in ads_info:
            ads_info.append(ad_text)
    
    return ads_info


def test_baidu_two_pages():
    """
    测试百度搜索"手机"，返回前2页中所有包含广告的信息
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--start-maximized')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)
    
    all_ads = []
    
    try:
        print("打开百度网页...")
        driver.get("https://www.baidu.com/")
        
        time.sleep(3)
        
        try:
            close_btn = driver.find_element(By.CSS_SELECTOR, ".close-btn, .s-close, [class*='close']")
            close_btn.click()
            print("关闭弹窗...")
            time.sleep(1)
        except:
            pass
        
        print("输入搜索关键词'手机'...")
        driver.execute_script("document.getElementById('kw').value = '手机';")
        time.sleep(0.5)
        
        driver.execute_script("document.getElementById('su').click();")
        
        print("等待搜索结果加载...")
        time.sleep(5)
        
        print("\n========== 第1页广告信息 ==========")
        page1_ads = get_ads_from_page(driver)
        for i, ad in enumerate(page1_ads, 1):
            print(f"\n广告 {i}:")
            print(ad[:200] + "..." if len(ad) > 200 else ad)
        all_ads.extend(page1_ads)
        print(f"\n第1页共找到 {len(page1_ads)} 条广告")
        
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, "a.n:last-child")
            print("\n点击下一页...")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_page)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", next_page)
            
            time.sleep(5)
            
            print("\n========== 第2页广告信息 ==========")
            page2_ads = get_ads_from_page(driver)
            for i, ad in enumerate(page2_ads, 1):
                print(f"\n广告 {i}:")
                print(ad[:200] + "..." if len(ad) > 200 else ad)
            all_ads.extend(page2_ads)
            print(f"\n第2页共找到 {len(page2_ads)} 条广告")
        except NoSuchElementException:
            print("\n未找到下一页按钮")
        except Exception as e:
            print(f"\n翻页失败: {str(e)}")
        
        print("\n" + "="*50)
        print(f"前2页共收集到 {len(all_ads)} 条广告信息")
        print("="*50)
        
        return all_ads
        
    except TimeoutException:
        print("测试失败：页面加载超时")
        return all_ads
    except Exception as e:
        print(f"测试执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return all_ads
    finally:
        print("\n等待10秒后关闭浏览器...")
        time.sleep(10)
        driver.quit()
        print("浏览器已关闭")


if __name__ == "__main__":
    test_baidu_two_pages()
