import csv
from time import sleep
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Constants
urllink = 'https://batdongsan.com.vn'
amp = 'https://batdongsan.com.vn/ban-nha-dat-tp-hcm/p'
amp1 = '?cIds=41,325,163,575,283,283,324'
n = 1500
namefile = 'bds_raw_data_new.csv'

# Set up Selenium WebDriver
user_agent = UserAgent().random
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu') 
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_driver_path = '/Users/mac/Downloads/chromedriver'
service = Service(chrome_driver_path)

with open(namefile, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Địa chỉ', 'Mức giá', 'Diện tích', 'Số phòng ngủ', 'Số tầng', 'Số toilet', 'Mô tả', 'Link', "Pháp lý", "Đường vào", "Mặt tiền", "Hướng nhà", "Nội thất"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    start_page = 1082
    for i in range(start_page, n):
        url = amp + str(i) + amp1

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        sleep(0.5)  # Adjusted sleep time for better loading
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for div in soup.findAll('a', class_='js__product-link-for-product-id'):
            link = div.get('href')
            full_link = urllink + link

            drive = webdriver.Chrome(service=service, options=chrome_options)
            drive.get(full_link)
            sleep(0.2)  # Increased sleep for property page loading
            soup = BeautifulSoup(drive.page_source, 'html.parser')

            data = {}
            data['Địa chỉ'] = soup.find('span', class_='re__pr-short-description js__pr-address').get_text().strip()

            container = soup.find('div', class_='re__pr-specs-content js__other-info')
            for title in ["Diện tích", "Mức giá", "Số phòng ngủ", "Số tầng", "Số toilet", "Pháp lý", "Đường vào", "Mặt tiền", "Hướng nhà", "Nội thất"]:  
                item = container.find('span', class_='re__pr-specs-content-item-title', text=title)
                if item:
                    value = item.find_next_sibling('span', class_='re__pr-specs-content-item-value').text.strip()
                    data[title] = value
                else:
                    data[title] = "Not found"
            
            data['Mô tả'] = soup.find('div', class_='re__section-body re__detail-content js__section-body js__pr-description js__tracking').get_text().strip()
            data['Link'] = full_link 

            print(data)
            writer.writerow(data)

            print("Successfully processed data from batdongsan.com.vn")
            drive.quit()
        driver.quit()
print("END")
