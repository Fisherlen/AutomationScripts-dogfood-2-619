"""
百度广告信息采集器
功能：采集百度搜索结果前N页中的广告信息
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class BaiduAdCollector:
    """百度广告信息采集类"""
    
    def __init__(self, headless=False):
        """初始化采集器"""
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        if headless:
            self.options.add_argument('--headless')
        
        self.service = Service(ChromeDriverManager().install())
        self.driver = None
        self.wait = None
        
    def start(self):
        """启动浏览器"""
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 15)
        
    def stop(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("\n浏览器已关闭")
            
    def search_keyword(self, keyword):
        """搜索指定关键词"""
        search_url = f"https://www.baidu.com/s?wd={keyword}"
        print(f"访问搜索结果页面: {search_url}")
        self.driver.get(search_url)
        time.sleep(2)
        
        # 等待搜索结果加载
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "content_left")))
            print("搜索结果页面加载完成")
        except TimeoutException:
            print("搜索结果加载超时，继续执行...")
            
    def get_page_ads(self, page_num):
        """获取当前页面的所有广告信息"""
        ad_contents = []
        print(f"\n=== 正在获取第 {page_num} 页的广告信息 ===")
        
        # 等待页面主要内容加载
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "content_left")))
        except TimeoutException:
            print("页面内容加载超时，继续尝试获取广告")
        
        time.sleep(2)
        
        # 定义过滤关键词列表，排除无关内容
        filter_keywords = ['精', '回复', '百度一下', '查看详情', '展开', '文心助手']
        
        # 查找带有广告标记的元素
        ad_indicators = self.driver.find_elements(
            By.XPATH, "//*[contains(text(), '广告') and not(contains(@class, 'c-icon'))]"
        )
        
        for indicator in ad_indicators:
            try:
                ad_container = indicator.find_element(
                    By.XPATH, 
                    "./ancestor::*[contains(@class, 'c-container') or contains(@class, 'result') or contains(@class, 'ad')][1]"
                )
                ad_text = ad_container.text.strip()
                
                # 过滤掉太短或包含过滤关键词的内容
                if (ad_text and ad_text not in ad_contents 
                    and len(ad_text) > 10 
                    and not any(keyword in ad_text for keyword in filter_keywords)
                    and '广告' in ad_text):
                    ad_contents.append(ad_text)
            except:
                continue

        # 查找明确标记为广告的容器
        explicit_ads = self.driver.find_elements(
            By.CSS_SELECTOR, 
            "[data-tpl='ad'], .c-container[tpl='ad'], .ecom_ad, [class*='ad-'], .ec-pl-container"
        )
        for ad in explicit_ads:
            try:
                ad_text = ad.text.strip()
                if (ad_text and ad_text not in ad_contents 
                    and len(ad_text) > 10 
                    and not any(keyword in ad_text for keyword in filter_keywords)):
                    ad_contents.append(ad_text)
            except:
                continue
        
        return ad_contents
            
    def go_to_next_page(self):
        """跳转到下一页"""
        try:
            # 等待页面底部加载
            self.wait.until(EC.presence_of_element_located((By.ID, "page")))
            
            # 查找下一页按钮
            next_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(text(), '下一页') or contains(@class, 'n')]")
                )
            )
            
            # 滚动到按钮位置
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            
            next_button.click()
            time.sleep(3)
            return True
        except NoSuchElementException:
            print("找不到下一页按钮")
            return False
        except Exception as e:
            print(f"翻页失败: {e}")
            return False
            
    def collect_ads(self, keyword, pages=2):
        """采集指定关键词的广告信息"""
        all_ads = []
        
        try:
            # 搜索关键词
            self.search_keyword(keyword)
            
            # 获取前N页的广告信息
            for page in range(1, pages + 1):
                page_ads = self.get_page_ads(page)
                all_ads.extend(page_ads)
                
                # 打印当前页广告
                print(f"\n第 {page} 页广告信息:")
                for i, ad in enumerate(page_ads, 1):
                    print(f"  广告 {i}: {ad[:100]}...")
                
                # 如果不是最后一页，点击下一页
                if page < pages:
                    print("\n跳转到下一页...")
                    if not self.go_to_next_page():
                        print("无法继续翻页，结束采集")
                        break
                        
            return all_ads
            
        except Exception as e:
            print(f"采集过程出错: {e}")
            import traceback
            traceback.print_exc()
            return all_ads

def print_ad_summary(ads):
    """打印广告汇总信息"""
    print("\n" + "="*60)
    print("=== 广告信息汇总 ===")
    print("="*60)
    
    for i, ad in enumerate(ads, 1):
        print(f"\n【广告 {i}】")
        print(ad)
        print("-"*40)
    
    print(f"\n总共获取到 {len(ads)} 条广告信息")
    
    # 检查是否包含京东
    all_ad_text = " ".join(ads)
    if "京东" in all_ad_text:
        print("\n--》检查结果：广告中包含'京东'，测试通过")
        return True
    else:
        print("\n--》检查结果：广告中不包含'京东'")
        return False

if __name__ == "__main__":
    # 使用示例
    collector = BaiduAdCollector(headless=False)
    
    try:
        collector.start()
        ads = collector.collect_ads("手机", pages=2)
        print_ad_summary(ads)
    finally:
        collector.stop()
