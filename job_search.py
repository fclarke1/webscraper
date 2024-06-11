import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import argparse


def main(args):
    # Define Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    # Add more options here if needed

    # Define paths
    user_home_dir = os.path.expanduser("~")
    chrome_binary_path = os.path.join(user_home_dir, "chrome-linux64", "chrome")
    chromedriver_path = os.path.join(user_home_dir, "chromedriver-linux64", "chromedriver")

    # Set binary location and service
    chrome_options.binary_location = chrome_binary_path
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the website
        driver.get('https://cord.co/search/')

        # Locate the search box
        search_box = driver.find_element(By.ID, 'keyword_input')

        # Enter text into the search box
        search_text = args.job_search
        search_box.send_keys(search_text)

        # Submit the search query (Option 1)
        search_box.send_keys(Keys.RETURN)
        
        # Wait until the company_block_list div is loaded
        wait = WebDriverWait(driver, 10)
        company_block = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'position_block_list')))

        # Find all job ad elements within the company_block_list
        job_ads = company_block.find_elements(By.CLASS_NAME, 'card_info')

        job_list = []

        for job in job_ads:
            # Extract job title and subtitle
            title = job.find_element(By.CLASS_NAME, 'card_title').text
            location = job.find_element(By.CLASS_NAME, 'position_details').text

            # Append the job details to the list
            job_list.append({'title': title, 'location': location})

        # Print the job list or process it as needed
        for job in job_list:
            print(f"{job['title']}\n  {job['location']}\n")

    except TimeoutException:
        print("Loading took too much time!")

    # Close the driver
    driver.quit()


if __name__=="__main__":
    # get user input for the search term
    parser = argparse.ArgumentParser(description='Search on Cord.co for jobs')
    parser.add_argument('--job_search', type=str, default='data analyst', help='enter job search text, default=data analyst')
    args = parser.parse_args()
    main(args)