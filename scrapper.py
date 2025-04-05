from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def linkedin_login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
    time.sleep(3)

def scrape_jobs(driver, keyword="Python Developer", location="Remote"):
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
    driver.get(url)
    time.sleep(3)
    
    jobs = []
    listings = driver.find_elements(By.CSS_SELECTOR, ".jobs-search__results-list li")
    
    for job in listings:
        title = job.find_element(By.CSS_SELECTOR, "h3").text
        company = job.find_element(By.CSS_SELECTOR, "h4").text
        url = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        jobs.append({
            "JobTitle": title,
            "Company": company,
            "JobURL": url,
            "Status": "Not Applied"
        })
    
    return jobs