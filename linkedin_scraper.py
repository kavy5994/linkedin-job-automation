# File: linkedin_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_linkedin_jobs(email, password, keywords, location, max_jobs=10):
    # Setup browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.linkedin.com/login")
    
    # Login
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    # Job Search
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}"
    driver.get(search_url)
    time.sleep(3)
    
    # Scroll to load jobs
    jobs = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")[:max_jobs]
    
    for job in job_elements:
        job.click()
        time.sleep(1)
        title = driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__job-title").text
        company = driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__company-name").text
        jobs.append({"Title": title, "Company": company})
    
    # Save to CSV
    pd.DataFrame(jobs).to_csv("linkedin_jobs.csv", index=False)
    driver.quit()

# Usage
scrape_linkedin_jobs(
    email="your_email@example.com",
    password="your_password",
    keywords="Data Scientist",
    location="United States"
)