# File: application_bot.py
from selenium.webdriver.common.keys import Keys

def auto_apply(driver, job_url, resume_path, cover_letter):
    driver.get(job_url)
    time.sleep(2)
    
    # Click Easy Apply
    driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button").click()
    time.sleep(1)
    
    # Fill form (simplified example)
    driver.find_element(By.NAME, "resume").send_keys(resume_path)
    driver.find_element(By.CSS_SELECTOR, "[aria-label='Cover letter']").send_keys(cover_letter)
    
    # Submit (disabled for safety - uncomment to use)
    # driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
    print("Application simulated - remove comments to enable real submission")

# Usage in main scraper:
# auto_apply(driver, job_url, "path/to/resume.pdf", cover_letter_text)