import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

import time

from concurrent.futures import ThreadPoolExecutor





numberOfThreads = 1





def initDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver

def visitSite(url, driver):
    urlsFoundInPage = 0
    try:
        driver.get(url)
        time.sleep(3)
        urlsFoundInPage = driver.find_elements(By.TAG_NAME, "a")
        print("found: " + str(len(urlsFoundInPage)) + " in " + url)
    except Exception as e:
        print("Exception " + str(e))
    finally:
        driver.quit()  

def main():

    # Init the web driver
    driver = initDriver()



    # This is the filePath to the file that contains all the url of the sites to visit 
    filePath = "../data/sitesList.csv"
    with open(filePath, mode='r', encoding="utf-8") as file:
        reader = csv.reader(file)

        # Read the content of the file line for line
        urls = []
        for row in reader:
            print(row)

            url = row[1] # WARNING we supposed to have in the second position of the csv the url to visit
            urls.append(url)



        with ThreadPoolExecutor(max_workers=numberOfThreads) as executor:
            futures = [executor.submit(visitSite, url, driver) for url in urls]

            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print("Exception: " + str(e))


  


if __name__ == "__main__":
    main()