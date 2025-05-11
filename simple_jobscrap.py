import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def linkedin_to_excel(job_title, location, max_results=10):
    """
    Super simple LinkedIn scraper that saves results to Excel
    """
    # Setup
    jobs = []
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"
    
    try:
        # Get page
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find jobs
        for job in soup.find_all('div', class_='base-card', limit=max_results):
            jobs.append({
                'Title': job.find('h3').get_text().strip(),
                'Company': job.find('h4').get_text().strip(),
                'Location': job.find('span', class_='job-search-card__location').get_text().strip(),
                'Link': job.find('a')['href'].split('?')[0]
            })
            time.sleep(1)  # Small delay
        
        # Save to Excel
        if jobs:
            pd.DataFrame(jobs).to_excel(f"{job_title}_jobs.xlsx", index=False)
            print(f"✅ Saved {len(jobs)} jobs to {job_title}_jobs.xlsx")
        else:
            print("❌ No jobs found")
            
    except Exception as e:
        print(f"Error: {e}")

# How to use
linkedin_to_excel("Data Analyst", "Canada")