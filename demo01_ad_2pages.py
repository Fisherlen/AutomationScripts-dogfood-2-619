"""
20250907 Sunday
扩展任务：返回前2页中所有包含广告的信息
基于 demo01_20250907.py 扩展
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import urllib.parse


def get_page_ads(driver, page_num):
    """
    获取当前页面的所有广告信息
    """
    ads_info = []
    
    try:
        # 查找带有广告标记的结果 - 多种可能的广告标记
        # 方式1: 通过"广告"文本查找
        ad_indicators = driver.find_elements(By.XPATH, "//span[contains(text(), '广告') or contains(text(), '商业推广')]")
        
        for indicator in ad_indicators:
            try:
                # 向上查找广告容器 - 尝试多种可能的父容器
                ad_container = None
                
                # 尝试不同的父级选择器
                for parent_level in range(1, 6):
                    try:
                        parent_xpath = "./ancestor::div[" + str(parent_level) + "]"
                        potential_container = indicator.find_element(By.XPATH, parent_xpath)
                        
                        # 检查是否包含标题链接
                        title_links = potential_container.find_elements(By.XPATH, ".//h3//a | .//a[@data-click] | .//a[contains(@class, 'title')] | .//a[contains(@class, 't')]")
                        if title_links:
                            ad_container = potential_container
                            break
                    except:
                        continue
                
                if not ad_container:
                    ad_container = indicator.find_element(By.XPATH, "./ancestor::div[contains(@class, 'c-container') or contains(@class, 'result')]")
                
                ad_data = {
                    "page": page_num,
                    "ad_number": len(ads_info) + 1,
                    "title": "",
                    "url": "",
                    "description": "",
                    "is_ad": True
                }
                
                # 获取标题
                try:
                    title_elem = ad_container.find_element(By.XPATH, ".//h3//a | .//a[@data-click] | .//a[contains(@class, 'title')] | .//a[contains(@class, 't')]")
                    ad_data["title"] = title_elem.text.strip()
                    ad_data["url"] = title_elem.get_attribute("href")
                except:
                    pass
                
                # 获取描述/内容
                try:
                    desc_elem = ad_container.find_element(By.XPATH, ".//span[contains(@class, 'content-right')] | .//div[contains(@class, 'content')] | .//span[contains(@class, 'abstract')] | .//div[contains(@class, 'c-span9')]")
                    ad_data["description"] = desc_elem.text.strip()
                except:
                    pass
                
                # 如果标题为空，尝试获取整个广告的文本
                if not ad_data["title"]:
                    ad_text = ad_container.text.strip()
                    ad_data["title"] = ad_text[:100] if ad_text else "未获取到标题"
                    ad_data["description"] = ad_text
                
                ads_info.append(ad_data)
                
            except Exception as e:
                print(f"  处理单个广告时出错: {str(e)}")
                continue
        
        # 方式2: 查找带有广告属性的容器
        try:
            ad_containers = driver.find_elements(By.CSS_SELECTOR, "div[tpl='ad'], div[data-tpl='ad'], .ecom_ad, div[mu*='ad']")
            for container in ad_containers:
                # 检查是否已经被添加
                container_text = container.text[:50]
                already_added = any(ad.get("title", "")[:50] == container_text for ad in ads_info)
                
                if not already_added and container_text:
                    ad_data = {
                        "page": page_num,
                        "ad_number": len(ads_info) + 1,
                        "title": container_text[:100],
                        "url": "",
                        "description": container.text,
                        "is_ad": True
                    }
                    
                    # 尝试获取链接
                    try:
                        link = container.find_element(By.TAG_NAME, "a")
                        ad_data["url"] = link.get_attribute("href")
                        if not ad_data["title"] or ad_data["title"] == container_text[:100]:
                            ad_data["title"] = link.text.strip()[:100]
                    except:
                        pass
                    
                    ads_info.append(ad_data)
        except Exception as e:
            print(f"  通过属性查找广告时出错: {str(e)}")
                
    except Exception as e:
        print(f"获取第{page_num}页广告时出错: {str(e)}")
    
    return ads_info


def go_to_page(driver, keyword, page_num):
    """
    通过URL直接跳转到指定页码
    """
    try:
        # 构建百度搜索URL
        encoded_keyword = urllib.parse.quote(keyword)
        # pn参数: 0=第1页, 10=第2页, 20=第3页...
        pn = (page_num - 1) * 10
        url = f"https://www.baidu.com/s?wd={encoded_keyword}&pn={pn}"
        
        print(f"跳转到第{page_num}页: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(5)
        
        return True
        
    except Exception as e:
        print(f"跳转到第{page_num}页失败: {str(e)}")
        return False


def test_baidu_2pages():
    """
    测试百度搜索"手机"前2页的广告信息
    """
    # 初始化浏览器驱动
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # 使用以下代码自动管理 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)
    wait = WebDriverWait(driver, 30)
    
    all_ads = []
    keyword = "手机"
    
    try:
        # 1. 获取第1页广告
        print("=== 正在获取第1页广告 ===")
        if go_to_page(driver, keyword, 1):
            page1_ads = get_page_ads(driver, 1)
            all_ads.extend(page1_ads)
            print(f"第1页找到 {len(page1_ads)} 条广告")
            
            for ad in page1_ads:
                print(f"  [{ad['ad_number']}] {ad['title'][:60]}...")
        
        # 2. 获取第2页广告
        print("\n=== 正在获取第2页广告 ===")
        if go_to_page(driver, keyword, 2):
            page2_ads = get_page_ads(driver, 2)
            all_ads.extend(page2_ads)
            print(f"第2页找到 {len(page2_ads)} 条广告")
            
            for ad in page2_ads:
                print(f"  [{ad['ad_number']}] {ad['title'][:60]}...")
        
        # 3. 输出汇总结果
        print("\n" + "="*50)
        print(f"总计找到 {len(all_ads)} 条广告")
        print("="*50)
        
        # 打印详细广告信息
        if all_ads:
            print("\n详细广告信息:")
            for ad in all_ads:
                print(f"\n[第{ad['page']}页 - 广告{ad['ad_number']}]")
                print(f"  标题: {ad['title']}")
                print(f"  URL: {ad['url'][:80]}..." if len(ad['url']) > 80 else f"  URL: {ad['url']}")
                print(f"  描述: {ad['description'][:100]}..." if len(ad['description']) > 100 else f"  描述: {ad['description']}")
        
        # 4. 保存结果到JSON文件
        output_file = "baidu_ads_2pages.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_ads, f, ensure_ascii=False, indent=2)
        print(f"\n广告信息已保存到: {output_file}")
        
        # 5. 检查结果
        if all_ads:
            print("\n--》测试通过：成功获取到广告信息")
            return True
        else:
            print("\n--》测试完成：未获取到任何广告信息（可能当前没有广告展示）")
            return True
            
    except TimeoutException:
        print("测试失败：页面加载超时")
        return False
    except Exception as e:
        print(f"测试执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 等待查看结果
        time.sleep(5)
        
        # 关闭浏览器
        driver.quit()
        print("\n浏览器已关闭")


if __name__ == "__main__":
    test_baidu_2pages()
