# File: main.py
from linkedin_scraper import scrape_linkedin_jobs
from notion_integration import sync_to_notion
from ai_generator import generate_cover_letter
import time
import random

def full_automation():
    # 1. Scrape
    scrape_linkedin_jobs(...)
    
    # 2. Sync to Notion
    sync_to_notion(...)
    
    # 3. Generate materials
    jobs = pd.read_csv("linkedin_jobs.csv")
    for _, job in jobs.iterrows():
        cover_letter = generate_cover_letter(...)
        
        # 4. Auto-apply (optional)
        # auto_apply(driver, job['link'], "resume.pdf", cover_letter)
        
        # Anti-bot delay
        time.sleep(random.randint(5, 15))

if __name__ == "__main__":
    full_automation()