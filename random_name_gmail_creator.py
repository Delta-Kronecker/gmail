#!/usr/bin/env python3
"""
Random Name Gmail Account Creator - With realistic random names
"""

import os
import time
import random
import csv
import json
import logging
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('random_gmail_creator.log'),
        logging.StreamHandler()
    ]
)

class RandomNameGmailCreator:
    def __init__(self):
        self.driver = None
        self.accounts_created = []
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver"""
        chrome_options = Options()
        
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logging.info("✅ Chrome driver initialized successfully")
        except Exception as e:
            logging.error(f"❌ Failed to initialize Chrome driver: {e}")
            raise
    
    def generate_username(self, index):
        """Generate username according to pattern"""
        return f"kaaamoooshi{str(index).zfill(3)}"
    
    def generate_random_name(self, length=5):
        """Generate random English name with reasonable length"""
        # Common English name patterns (consonant-vowel combinations)
        consonants = 'bcdfghjklmnpqrstvwxyz'
        vowels = 'aeiou'
        
        name = ''
        for i in range(length):
            if i % 2 == 0:
                name += random.choice(consonants)
            else:
                name += random.choice(vowels)
        
        return name.capitalize()
    
    def generate_random_lastname(self, length=6):
        """Generate random English lastname"""
        # Common lastname endings
        endings = ['son', 'man', 'ton', 'wood', 'field', 'worth', 'stein', 'berg', 'ford', 'ville']
        
        base_length = length - 3
        if base_length < 2:
            base_length = 2
            
        base = self.generate_random_name(base_length).lower()
        ending = random.choice(endings)
        
        return (base + ending).capitalize()
    
    def smart_wait(self, min_time=1, max_time=3):
        """Smart random delay"""
        delay = random.uniform(min_time, max_time)
        time.sleep(delay)
    
    def find_element_safe(self, by, value, timeout=10):
        """Safely find element"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logging.warning(f"⏰ Timeout finding element: {by}={value}")
            return None
    
    def fill_account_info(self, username, password, first_name, last_name):
        """Fill account information with random names"""
        try:
            logging.info("🌐 Navigating to Google signup...")
            self.driver.get("https://accounts.google.com/signup")
            self.smart_wait(2, 4)
            
            # Take screenshot for debugging
            self.driver.save_screenshot('debug_page1.png')
            
            # Find first name field - try multiple selectors
            first_name_field = None
            selectors = [
                (By.NAME, "firstName"),
                (By.CSS_SELECTOR, "input[aria-label*='First name']"),
                (By.CSS_SELECTOR, "input[placeholder*='First']"),
                (By.ID, "firstName"),
                (By.CSS_SELECTOR, "input[type='text']")
            ]
            
            for by, value in selectors:
                first_name_field = self.find_element_safe(by, value)
                if first_name_field:
                    break
            
            if not first_name_field:
                logging.error("❌ Could not find first name field")
                return "field_not_found"
            
            # Fill first name
            first_name_field.clear()
            first_name_field.send_keys(first_name)
            self.smart_wait(0.5, 1.5)
            
            # Find last name field
            last_name_field = None
            selectors = [
                (By.NAME, "lastName"),
                (By.CSS_SELECTOR, "input[aria-label*='Last name']"),
                (By.CSS_SELECTOR, "input[placeholder*='Last']"),
                (By.ID, "lastName")
            ]
            
            for by, value in selectors:
                last_name_field = self.find_element_safe(by, value)
                if last_name_field:
                    break
            
            if not last_name_field:
                logging.error("❌ Could not find last name field")
                return "field_not_found"
            
            # Fill last name
            last_name_field.clear()
            last_name_field.send_keys(last_name)
            self.smart_wait(0.5, 1.5)
            
            # Find and click next button
            next_button = None
            selectors = [
                (By.XPATH, "//span[contains(text(), 'Next')]"),
                (By.XPATH, "//button[contains(., 'Next')]"),
                (By.CSS_SELECTOR, "button[type='button']"),
                (By.CSS_SELECTOR, ".VfPpkd-vQzf8d")
            ]
            
            for by, value in selectors:
                next_button = self.find_element_safe(by, value)
                if next_button:
                    break
            
            if next_button:
                try:
                    next_button.click()
                    self.smart_wait(2, 4)
                    self.driver.save_screenshot('debug_page2.png')
                except:
                    # Try JavaScript click as fallback
                    self.driver.execute_script("arguments[0].click();", next_button)
                    self.smart_wait(2, 4)
            else:
                logging.warning("⚠️ Could not find next button")
                return "next_button_not_found"
            
            # Check current page status
            current_url = self.driver.current_url
            page_source = self.driver.page_source
            
            logging.info(f"📄 Current URL: {current_url}")
            
            if "challenge" in current_url.lower():
                return "verification_required"
            elif "myaccount" in current_url.lower() or "welcome" in current_url.lower():
                return "success"
            elif "username" in current_url.lower():
                return self.fill_username_password(username, password)
            else:
                return f"unknown_page"
                
        except Exception as e:
            logging.error(f"❌ Error in form filling: {e}")
            return f"error"
    
    def fill_username_password(self, username, password):
        """Fill username and password fields"""
        try:
            # Find username field
            username_field = None
            selectors = [
                (By.NAME, "Username"),
                (By.ID, "username"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[aria-label*='username']")
            ]
            
            for by, value in selectors:
                username_field = self.find_element_safe(by, value)
                if username_field:
                    break
            
            if username_field:
                username_field.clear()
                username_field.send_keys(username)
                self.smart_wait(1, 2)
            
            # Find password field
            password_field = None
            selectors = [
                (By.NAME, "Passwd"),
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.ID, "passwd"),
                (By.CSS_SELECTOR, "input[aria-label*='password']")
            ]
            
            for by, value in selectors:
                password_field = self.find_element_safe(by, value)
                if password_field:
                    break
            
            if password_field:
                password_field.clear()
                password_field.send_keys(password)
                self.smart_wait(1, 2)
            
            # Find confirm password field
            confirm_field = None
            selectors = [
                (By.NAME, "ConfirmPasswd"),
                (By.CSS_SELECTOR, "input[aria-label*='Confirm']")
            ]
            
            for by, value in selectors:
                confirm_field = self.find_element_safe(by, value)
                if confirm_field:
                    break
            
            if confirm_field:
                confirm_field.clear()
                confirm_field.send_keys(password)
                self.smart_wait(1, 2)
            
            # Try to submit
            next_button = None
            selectors = [
                (By.XPATH, "//span[contains(text(), 'Next')]"),
                (By.XPATH, "//button[contains(., 'Next')]"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]
            
            for by, value in selectors:
                next_button = self.find_element_safe(by, value)
                if next_button:
                    break
            
            if next_button:
                try:
                    next_button.click()
                    self.smart_wait(3, 5)
                except:
                    self.driver.execute_script("arguments[0].click();", next_button)
                    self.smart_wait(3, 5)
            
            # Final status check
            final_url = self.driver.current_url
            if "challenge" in final_url:
                return "phone_verification_required"
            elif "myaccount" in final_url:
                return "success"
            else:
                return f"submitted"
                
        except Exception as e:
            return f"username_password_error"
    
    def attempt_account_creation(self, index):
        """Attempt to create a single Gmail account with random names"""
        username = self.generate_username(index)
        password = "kaaamoooshi"
        
        # Generate random names
        first_name = self.generate_random_name(random.randint(4, 6))
        last_name = self.generate_random_lastname(random.randint(5, 8))
        
        logging.info(f"🔄 Attempting to create account {index}: {username}")
        logging.info(f"👤 Using names: {first_name} {last_name}")
        
        try:
            status = self.fill_account_info(username, password, first_name, last_name)
            
            account_info = {
                'index': index,
                'first_name': first_name,
                'last_name': last_name,
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
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': f'{username}@gmail.com',
                'password': password,
                'status': f'critical_error',
                'timestamp': time.time()
            }
            self.accounts_created.append(account_info)
            return False
    
    def save_results(self):
        """Save results to files"""
        # CSV file
        with open('random_gmail_accounts.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Index', 'First Name', 'Last Name', 'Username', 'Email', 'Password', 'Status', 'Timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account in self.accounts_created:
                writer.writerow({
                    'Index': account['index'],
                    'First Name': account['first_name'],
                    'Last Name': account['last_name'],
                    'Username': account['username'],
                    'Email': account['email'],
                    'Password': account['password'],
                    'Status': account['status'],
                    'Timestamp': account.get('timestamp', '')
                })
        
        # JSON file
        with open('random_gmail_accounts.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.accounts_created, jsonfile, ensure_ascii=False, indent=2)
        
        logging.info(f"💾 Results saved: {len(self.accounts_created)} accounts")
    
    def run_creation_process(self, start_index=1, end_index=5):
        """Run the account creation process"""
        logging.info("🚀 Starting Random Name Gmail account creation process...")
        
        for i in range(start_index, end_index + 1):
            try:
                self.attempt_account_creation(i)
                
                # Save progress
                if i % 2 == 0:
                    self.save_results()
                    logging.info(f"💾 Progress saved at index {i}")
                
                # Delay between attempts
                if i < end_index:
                    delay = random.uniform(10.0, 20.0)
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
        end_index = int(os.getenv('END_INDEX', '5'))
        
        creator = RandomNameGmailCreator()
        creator.run_creation_process(start_index, end_index)
        
    except Exception as e:
        logging.error(f"💥 Critical error: {e}")
    finally:
        if creator:
            creator.cleanup()

if __name__ == "__main__":
    main()
