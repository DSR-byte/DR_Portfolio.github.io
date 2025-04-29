import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse, time, random

class TruePeopleSearchScraper:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")


        self.driver = uc.Chrome(use_subprocess=False,options=options)
        self.driver.set_page_load_timeout(random.uniform(10, 20))
        self.SC_OFF_Flag = False

    def build_url(self, name, city_state):
        name_param = urllib.parse.quote(name)
        location_param = urllib.parse.quote(city_state)
        return f"https://www.truepeoplesearch.com/results?name={name_param}&citystatezip={location_param}"

    def load_search_page(self, url):
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"⏱️ Timeout or load error — {e}. Retrying with JS...")
            try:
                self.driver.execute_script("location.reload()")
                time.sleep(random.uniform(10, 20))
            except:
                pass
        time.sleep(random.uniform(10, 20))

    def get_detail_links(self):
        try:
            return WebDriverWait(self.driver, random.uniform(10, 20)).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/find/person/')]"))
            )
        except:
            print("🧼 Killing overlays and retrying...")
            try:
                self.driver.execute_script("""
                    let ads = document.querySelectorAll('[id*="ad"], [class*="ad"], .overlay, .popup, .modal');
                    ads.forEach(ad => ad.remove());
                """)
            except:
                pass
            time.sleep(random.uniform(10, 20))
            return self.driver.find_elements(By.XPATH, "//a[contains(@href, '/find/person/')]")

    def find_phone_number(self, detail_links):
        
        links = [
            btn.get_attribute("href") if btn.get_attribute("href").startswith("http")
            else "https://www.truepeoplesearch.com" + btn.get_attribute("href")
            for btn in detail_links
        ]
    
        for url in links:
            if self.SC_OFF_Flag:
                self.driver.quit()
                break
            
            try:
                print("🔗 Trying:", url)
                self.driver.get(url)
                self.driver.refresh()
                time.sleep(random.uniform(10, 20))
                phone = WebDriverWait(self.driver, random.uniform(10, 20)).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span[itemprop="telephone"]'))
                ).text.strip()
                print("✅ Phone number found:", phone)
                return phone
            except Exception as e:
                print(f"❌ No number on this page: {type(e).__name__}")
        print("❌ No phone number found in any results.")
        return "N/A"


    def search(self, name, city_state):
        try:
            url = self.build_url(name, city_state)
            print(f"\n🔍 Searching: {name} | {city_state}")
            self.load_search_page(url)
            links = self.get_detail_links()
            print(f"🔗 Found {len(links)} detail links")
            return self.find_phone_number(links)
        except Exception as e:
            print(f"❌ Error during search for {name}: {e}")
            return "ERROR"

    def close(self):
        self.SC_OFF_Flag = True



