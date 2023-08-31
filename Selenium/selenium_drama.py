import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

start_time = time.time()
base_url = 'https://mydramalist.com/people/top'
output_file = 'selenium_drama.csv'
chrome_options = Options()

chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--start-maximized")

driver_service = ChromeService() 
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

data = []

all_links_counter = 0

counter=1
while all_links_counter<101:
    
    base_url='https://mydramalist.com/people/top?page='+str(counter)
    driver.get(base_url)

    links = driver.find_elements(By.XPATH, '//h6/a')[:101]
    all_links = []


    for link in links:
        item_url = link.get_attribute('href')
        all_links.append(item_url)
    
    all_links_counter += len(all_links)
        
    for link in all_links:
        try:
            print(link)
            driver.get(link)
            name = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[2]/div/div[1]/div[1]/h1').text
            print(name)
            table_rows = driver.find_elements(By.XPATH, '//table[@class="table film-list"]//tr')[1:]
            for row in table_rows:
                tds = row.find_elements(By.XPATH, './/td')
                row_data = [name] + [td.text for td in tds]
                data.append(row_data)
                break
           
        except:
            pass
        

    counter=counter+1
    

driver.quit()
df = pd.DataFrame(data)
df.to_csv(output_file, index=False)

end_time = time.time()

print("Runtime Selenium", end_time-start_time)