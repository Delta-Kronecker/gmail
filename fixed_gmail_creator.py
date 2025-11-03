#!/usr/bin/env python3
"""
Fixed Gmail Account Creator - With better error handling and element detection
"""

import os
import time
import random
import csv
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fixed_gmail_creator.log'),
        logging.StreamHandler()
    ]
)

class FixedGmailCreator:
    def __init__(self):
        self.driver = None
        self.accounts_created = []
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver with better options"""
        chrome_options = Options()
        
        # Essential options for GitHub Actions
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        
        # Bypass automation detection
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Real user agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            # Remove webdriver properties
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            })
            logging.info("✅ Chrome driver initialized successfully")
        except Exception as e:
            logging.error(f"❌ Failed to initialize Chrome driver: {e}")
            raise
    
    def generate_username(self, index):
        """Generate username according to pattern"""
        return f"kaaamoooshi{str(index).zfill(3)}"
    
    def smart_wait(self, min_time=1, max_time=3):
        """Smart random delay"""
        delay = random.uniform(min_time, max_time)
        time.sleep(delay)
    
    def find_element_safe(self, by, value, timeout=10):
        """Safely find element with multiple strategies"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logging.warning(f"⏰ Timeout finding element: {by}={value}")
            return None
    
    def click_element(self, element):
        """Safe click with JavaScript fallback"""
        try:
            element.click()
            return True
        except:
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                return False
    
    def fill_account_info_smart(self, username, password):
        """Smart form filling with multiple element detection strategies"""
        try:
            logging.info("🌐 Navigating to Google signup...")
            self.driver.get("https://accounts.google.com/signup")
            self.smart_wait(2, 4)
            
            # Take screenshot for debugging
            self.driver.save_screenshot('debug_page1.png')
            
            # Strategy 1: Try multiple possible selectors for first name
            first_name_selectors = [
                "input[name='firstName']",
                "input[aria-label='First name']",
                "#firstName",
                "input[type='text']",
                "input[placeholder*='First']"
            ]
            
            first_name_field = None
            for selector in first_name_selectors:
                try:
                    if 'name=' in selector:
                        first_name_field = self.find_element_safe(By.NAME, selector.split('=')[1].strip("'"))
                    elif '#' in selector:
                        first_name_field = self.find_element_safe(By.ID, selector.split('#')[1])
                    else:
                        first_name_field = self.find_element_safe(By.CSS_SELECTOR, selector)
                    
                    if first_name_field:
                        break
                except:
                    continue
            
            if not first_name_field:
                logging.error("❌ Could not find first name field")
                return "field_not_found"
            
            # Fill first name
            first_name_field.clear()
            first_name_field.send_keys("A")
            self.smart_wait(0.5, 1.5)
            
            # Find last name field
            last_name_selectors = [
                "input[name='lastName']",
                "input[aria-label='Last name']",
                "#lastName",
                "input[placeholder*='Last']"
            ]
            
            last_name_field = None
            for selector in last_name_selectors:
                try:
                    if 'name=' in selector:
                        last_name_field = self.find_element_safe(By.NAME, selector.split('=')[1].strip("'"))
                    elif '#' in selector:
                        last_name_field = self.find_element_safe(By.ID, selector.split('#')[1])
                    else:
                        last_name_field = self.find_element_safe(By.CSS_SELECTOR, selector)
                    
                    if last_name_field:
                        break
                except:
                    continue
            
            if not last_name_field:
                logging.error("❌ Could not find last name field")
                return "field_not_found"
            
            # Fill last name
            last_name_field.clear()
            last_name_field.send_keys("A")
            self.smart_wait(0.5, 1.5)
            
            # Find and click next button
            next_button_selectors = [
                "button[type='button'] span",
                "div[role='button'] span",
                "button:contains('Next')",
                "span:contains('Next')",
                ".VfPpkd-vQzf8d"
            ]
            
            next_button = None
            for selector in next_button_selectors:
                try:
                    if 'contains' in selector:
                        next_button = self.find_element_safe(By.XPATH, f"//*[contains(text(), 'Next')]")
                    else:
                        next_button = self.find_element_safe(By.CSS_SELECTOR, selector)
                    
                    if next_button:
                        break
                except:
                    continue
            
            if next_button:
                self.click_element(next_button)
                self.smart_wait(2, 4)
                
                # Take screenshot after clicking next
                self.driver.save_screenshot('debug_page2.png')
            else:
                logging.warning("⚠️ Could not find next button, trying to proceed")
            
            # Check current page status
            current_url = self.driver.current_url
            page_title = self.driver.title
            page_source = self.driver.page_source
            
            logging.info(f"📄 Current URL: {current_url}")
            logging.info(f"📄 Page title: {page_title}")
            
            # Analyze page content
            if "challenge" in current_url.lower():
                return "verification_required"
            elif "myaccount" in current_url.lower() or "welcome" in current_url.lower():
                return "success"
            elif "username" in current_url.lower() or "signup" in current_url.lower():
                # Continue with username/password filling
                return self.fill_username_password(username, password)
            else:
                return f"unknown_page_{current_url.split('/')[-1]}"
                
        except Exception as e:
            logging.error(f"❌ Error in form filling: {e}")
            return f"error_{str(e)[:50]}"
    
    def fill_username_password(self, username, password):
        """Fill username and password fields"""
        try:
            # Find username field
            username_selectors = [
                "input[name='Username']",
                "input[aria-label*='username']",
                "#username",
                "input[type='email']"
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    if 'name=' in selector:
                        username_field = self.find_element_safe(By.NAME, selector.split('=')[1].strip("'"))
                    elif '#' in selector:
                        username_field = self.find_element_safe(By.ID, selector.split('#')[1])
                    else:
                        username_field = self.find_element_safe(By.CSS_SELECTOR, selector)
                    
                    if username_field:
                        break
                except:
                    continue
            
            if username_field:
                username_field.clear()
                username_field.send_keys(username)
                self.smart_wait(1, 2)
            
            # Find password field
            password_selectors = [
                "input[name='Passwd']",
                "input[type='password']",
                "#passwd",
                "input[aria-label*='password']"
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    if 'name=' in selector:
                        password_field = self.find_element_safe(By.NAME, selector.split('=')[1].strip("'"))
                    elif '#' in selector:
                        password_field = self.find_element_safe(By.ID, selector.split('#')[1])
                    else:
                        password_field = self.find_element_safe(By.CSS_SELECTOR, selector)
                    
                    if password_field:
                        break
                except:
                    continue
            
            if password_field:
                password_field.clear()
                password_field.send_keys(password)
                self.smart_wait(1, 2)
            
            # Try to submit
            submit_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Next')",
                "span:contains('Next')"
            ]
            
            for selector in submit_selectors:
                try:
                    if 'contains' in selector:
                        submit_btn = self.find_element_safe(By.XPATH, f"//*[contains(text(), 'Next')]")
                    else:
                        submit_btn = self.find_element_safe(By.CSS_SELECTOR, selector)
                    
                    if submit_btn:
                        self.click_element(submit_btn)
                        self.smart_wait(3, 5)
                        break
                except:
                    continue
            
            # Final status check
            final_url = self.driver.current_url
            if "challenge" in final_url:
                return "phone_verification_required"
            elif "myaccount" in final_url:
                return "success"
            else:
                return f"submitted_{final_url.split('/')[-1]}"
                
        except Exception as e:
            return f"username_password_error_{str(e)[:30]}"
    
    def attempt_account_creation(self, index):
        """Attempt to create a single Gmail account"""
        username = self.generate_username(index)
        password = "kaaamoooshi"
        
        logging.info(f"🔄 Attempting to create account {index}: {username}")
        
        try:
            status = self.fill_account_info_smart(username, password)
            
            account_info = {
                'index': index,
                'name': 'A A',
                'username': username,
                'email': f'{username}@gmail.com',
                'password': password,
                'status': status,
                'timestamp': time.time()
            }
            
            self.accounts_created.append(account_info)
            logging.info(f"📝 Account {username} - Status: {status}")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to create account {username}: {e}")
            
            account_info = {
                'index': index,
                'name': 'A A',
                'username': username,
                'email': f'{username}@gmail.com',
                'password': password,
                'status': f'critical_error_{str(e)[:30]}',
                'timestamp': time.time()
            }
            self.accounts_created.append(account_info)
            return False
    
    def save_results(self):
        """Save results to files"""
        # CSV file
        with open('fixed_gmail_accounts.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Index', 'Name', 'Username', 'Email', 'Password', 'Status', 'Timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account in self.accounts_created:
                writer.writerow({
                    'Index': account['index'],
                    'Name': account['name'],
                    'Username': account['username'],
                    'Email': account['email'],
                    'Password': account['password'],
                    'Status': account['status'],
                    'Timestamp': account.get('timestamp', '')
                })
        
        # JSON file
        with open('fixed_gmail_accounts.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.accounts_created, jsonfile, ensure_ascii=False, indent=2)
        
        logging.info(f"💾 Results saved: {len(self.accounts_created)} accounts")
    
    def run_creation_process(self, start_index=1, end_index=3):
        """Run the account creation process"""
        logging.info("🚀 Starting FIXED Gmail account creation process...")
        
        for i in range(start_index, end_index + 1):
            try:
                self.attempt_account_creation(i)
                
                # Save progress
                if i % 2 == 0:
                    self.save_results()
                    logging.info(f"💾 Progress saved at index {i}")
                
                # Delay between attempts
                if i < end_index:
                    delay = random.uniform(15.0, 25.0)
                    logging.info(f"⏳ Waiting {delay:.1f} seconds...")
                    time.sleep(delay)
                    
            except Exception as e:
                logging.error(f"❌ Unexpected error at index {i}: {e}")
                continue
        
        # Final save
        self.save_results()
        
        # Summary
        status_count = {}
        for account in self.accounts_created:
            status = account['status']
            status_count[status] = status_count.get(status, 0) + 1
        
        logging.info("📊 Final Summary:")
        for status, count in status_count.items():
            logging.info(f"   {status}: {count} accounts")
        
        return len(self.accounts_created)
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()
            logging.info("✅ Chrome driver closed")

def main():
    """Main execution function"""
    creator = None
    try:
        start_index = int(os.getenv('START_INDEX', '1'))
        end_index = int(os.getenv('END_INDEX', '3'))
        
        creator = FixedGmailCreator()
        creator.run_creation_process(start_index, end_index)
        
    except Exception as e:
        logging.error(f"💥 Critical error: {e}")
    finally:
        if creator:
            creator.cleanup()

if __name__ == "__main__":
    main()
