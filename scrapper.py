import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LinkedInJobScraper:
    def __init__(self):
        self.driver = self.create_driver()
        self.wait = WebDriverWait(self.driver, 15)
        
    def create_driver(self):
        chrome_options = webdriver.ChromeOptions()
        
        # Optimization and stealth settings
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Headless mode (uncomment when ready)
        # chrome_options.add_argument('--headless=new')
        # chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def login(self, email, password):
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            # Handle cookie consent if present
            try:
                cookie_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@action-type, 'ACCEPT')]"))
                )
                cookie_btn.click()
            except TimeoutException:
                pass
            
            # Fill login form
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(email)
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            submit_button.click()
            
            # Verify login success
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label, 'Search')]"))
            )
            print("Login successful")
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            self.driver.save_screenshot("login_failure.png")
            return False
    
    def scrape_jobs(self, keyword="Business Developer", location="Remote", max_jobs=10):
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
        self.driver.get(url)
        time.sleep(3)
        
        jobs = []
        listings = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".jobs-search__results-list li"))
        )[:max_jobs]  # Only take the first 10 listings
    
        for job in listings:
            try:
                title = job.find_element(By.CSS_SELECTOR, "h3").text.strip()
                company = job.find_element(By.CSS_SELECTOR, "h4").text.strip()
                url = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href").split('?')[0]
                
                jobs.append({
                    "JobTitle": title,
                    "Company": company,
                    "JobURL": url,
                    "Status": "Not Applied"
                })
                
                # Stop if we have 10 jobs
                if len(jobs) >= 10:
                    break
                    
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
        
        return jobs
    
    def _scroll_page(self):
        """Scroll to load all jobs on the page"""
        scroll_pause_time = 1
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def _extract_job_data(self, job_element):
        """Extract detailed job data from a listing"""
        try:
            title = job_element.find_element(By.CSS_SELECTOR, "h3").text.strip()
            company = job_element.find_element(By.CSS_SELECTOR, "h4").text.strip()
            location = job_element.find_element(By.CSS_SELECTOR, "[class*='job-search-card__location']").text.strip()
            url = job_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href").split('?')[0]
            
            # Try to get posting date if available
            try:
                date = job_element.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
            except NoSuchElementException:
                date = "Not specified"
            
            return {
                "JobTitle": title,
                "Company": company,
                "Location": location,
                "DatePosted": date,
                "JobURL": url,
                "Status": "Not Applied"
            }
            
        except Exception as e:
            print(f"Error extracting job details: {str(e)}")
            return None
    
    def _has_next_page(self):
        """Check if there's a next page available"""
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
            return "disabled" not in next_button.get_attribute("class")
        except NoSuchElementException:
            return False
    
    def close(self):
        self.driver.quit()

# Usage example:
if __name__ == "__main__":
    scraper = LinkedInJobScraper()
    if scraper.login("):
        jobs = scraper.scrape_jobs(keyword="Business Developer", location="Remote", max_pages=1)
        
        # Save just the first 10 jobs
        scraper.save_first_10_jobs(jobs)
        
        scraper.close()
    
        