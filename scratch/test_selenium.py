import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
try:
    path = os.path.abspath('d:/dbmss/templates/delivery_dashboard.html')
    driver.get('file://' + path)
    time.sleep(1)
    print('Initial Tabs Active:', len(driver.find_elements(By.CSS_SELECTOR, '.tab-content.active')))
    
    # Click tracking tab
    link = driver.find_element(By.XPATH, "//a[contains(text(), 'Live Tracking')]")
    link.click()
    time.sleep(1)
    
    # Read JS errors
    logs = driver.get_log('browser')
    for log in logs:
        print('BROWSER LOG:', log)
        
    print('Tabs Active After Click:', len(driver.find_elements(By.CSS_SELECTOR, '.tab-content.active')))
except Exception as e:
    print('Python Error:', e)
finally:
    driver.quit()
