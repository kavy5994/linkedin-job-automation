from selenium import webdriver
from dotenv import load_dotenv
from scrapper import linkedin_login, scrape_jobs
from airtable_manager import AirtableManager
from ai_helper import generate_cover_letter
import time

load_dotenv()

def main():
    # Initialize components
    driver = webdriver.Chrome()
    at_manager = AirtableManager()
    
    # Step 1: Scrape LinkedIn
    linkedin_login(driver, os.getenv("LINKEDIN_EMAIL"), os.getenv("LINKEDIN_PASSWORD"))
    jobs = scrape_jobs(driver, keyword="Python Developer")
    
    # Step 2: Process jobs
    for job in jobs:
        # Step 3: Generate cover letter (mock resume)
        resume_text = "Experienced Python developer with 3+ years..."
        job["CoverLetter"] = generate_cover_letter(job["JobTitle"], resume_text)
        
        # Step 4: Save to Airtable
        at_manager.add_job(job)
        print(f"Added: {job['JobTitle']} at {job['Company']}")
    
    driver.quit()

if __name__ == "__main__":
    main()