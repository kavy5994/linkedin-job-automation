from scrapper import linkedin_login, scrape_jobs, create_driver
from airtable_manager import AirtableManager
from selenium import webdriver
import os
from dotenv import load_dotenv


#from ai_helper import generate_cover_letter
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
load_dotenv()



def main():
    # Initialize components
    driver = create_driver() #webdriver.Chrome()
    at_manager = AirtableManager()
    
    # Step 1: Scrape LinkedIn
    linkedin_login(driver, os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"))
    jobs = scrape_jobs(driver, keyword="business Developer")
    
    # Step 2: Process jobs
    for job in jobs:
        # Step 3: Generate cover letter (mock resume)
        resume_text = "Experienced Python developer with 3+ years..."
        #job["CoverLetter"] = generate_cover_letter(job["JobTitle"], resume_text)
        
        # Step 4: Save to Airtable
        at_manager.add_job(job)
        print(f"Added: {job['JobTitle']} at {job['Company']}")
    
    driver.quit()

if __name__ == "__main__":
    main()