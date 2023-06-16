import re
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class LaptopCrawler:
    def __init__(self, chromedriver_path, url):
        self.chromedriver_path = chromedriver_path
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def get_laptops(self):
        laptops = []
        self.driver.get(self.url)
        for i in range(160):
            elements = self.driver.find_elements(By.CLASS_NAME, "more-details")

            # Retrieve the href attribute of each element
            for element in elements:
                href = element.get_attribute("href")
                laptops.append(href)
            self.driver.find_element(by=By.CLASS_NAME, value="page-item.next").click()
        return laptops

    def get_details(self, laptops):
        all_details = []
        for laptop in laptops:
            time.sleep(2)
            print(laptop)
            self.driver.get(laptop)
            crawling_time = datetime.now()
            price_and_stores = self.driver.find_element(By.CLASS_NAME, "prices-txt").text
            price_and_stores = re.findall(r'\b\d+(?:,\d+)?\b', price_and_stores)
            laptop_val = {}
            rows_values = self.driver.find_elements(By.CLASS_NAME, "paramRow")
            for row in rows_values:
                param_and_value = row.text.split('\n')
                if len(param_and_value) == 2:
                    laptop_val[param_and_value[0]] = param_and_value[1]
            if len(price_and_stores) == 3:
                laptop_val['lower_price'] = price_and_stores[0]
                laptop_val['higher_price'] = price_and_stores[1]
                laptop_val['num_of_stores'] = price_and_stores[2]
            elif len(price_and_stores) == 2:
                laptop_val['lower_price'] = price_and_stores[0]
                laptop_val['higher_price'] = price_and_stores[0]
                laptop_val['num_of_stores'] = price_and_stores[1]
            else:
                laptop_val['lower_price'] = price_and_stores[0]
                laptop_val['higher_price'] = price_and_stores[0]
                laptop_val['num_of_stores'] = 1
            laptop_val['crawling_time'] = crawling_time
            all_details.append(laptop_val)
        df = pd.DataFrame(all_details)
        df.to_excel("output.xlsx")


class BenchmarkCrawler:
    def __init__(self, chromedriver_path, url):
        self.chromedriver_path = chromedriver_path
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def crawl_cpu(self):
        # Load the web page
        self.driver.get(self.url)

        # Find the table element by ID
        table = self.driver.find_element(By.ID, "cputable")

        # Find all rows in the table
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Create empty lists to store the column data
        cpu_names = []
        cpu_marks = []
        ranks = []
        prices = []

        # Loop through the rows and extract the data
        for row in rows[1:]:  # Exclude the header row
            # Find columns within each row
            columns = row.find_elements(By.TAG_NAME, "td")

            # Extract the text from each column
            cpu_name = columns[0].text
            cpu_mark = columns[1].text
            rank = columns[2].text
            price = columns[3].text

            # Append the data to the respective lists
            cpu_names.append(cpu_name)
            cpu_marks.append(cpu_mark)
            ranks.append(rank)
            prices.append(price)

        # Close the WebDriver
        self.driver.quit()

        # Create a DataFrame from the data lists
        data = {"CPU_name": cpu_names, "CPU_mark": cpu_marks, "Rank": ranks, "Price": prices}
        df = pd.DataFrame(data)

        df.to_excel("benchmark.xlsx")


def main():
    chromedriver_path = r"../chromedriver.exe"
    url = "https://www.zap.co.il/models.aspx?sog=c-pclaptop"
    cpu_banchmark_crawler = BenchmarkCrawler(chromedriver_path, 'https://www.cpubenchmark.net/cpu_list.php')
    cpu_banchmark_crawler.crawl_cpu()

    laptop_crawler = LaptopCrawler(chromedriver_path, url)
    laptops = laptop_crawler.get_laptops()
    laptop_crawler.get_details(laptops)


if __name__ == '__main__':
    main()
