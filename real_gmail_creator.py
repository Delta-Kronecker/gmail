#!/usr/bin/env python3
"""
Real Gmail Account Creator - Educational Project
This script attempts to actually create Gmail accounts
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('real_gmail_creator.log'),
        logging.StreamHandler()
    ]
)

class RealGmailCreator:
    def __init__(self):
        self.driver = None
        self.accounts_created = []
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver for real execution"""
        chrome_options = Options()
        
        # Options for GitHub Actions environment
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set user agent
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
    
    def simulate_human_behavior(self):
        """Simulate human-like behavior with random delays"""
        delay = random.uniform(1.0, 3.0)
        time.sleep(delay)
    
    def fill_account_info(self, username, password):
        """Fill account information in Gmail signup form"""
        try:
            # Wait for page to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "firstName"))
            )
            
            # Fill first name
            first_name = self.driver.find_element(By.NAME, "firstName")
            first_name.clear()
            first_name.send_keys("A")
            
            # Fill last name
            last_name = self.driver.find_element(By.NAME, "lastName")
            last_name.clear()
            last_name.send_keys("A")
            
            self.simulate_human_behavior()
            
            # Click next button
            next_btn = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_btn.click()
            
            # Wait for next page
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "month"))
            )
            
            # Fill birthday information
            # Month
            month_select = self.driver.find_element(By.ID, "month")
            month_select.click()
            months = self.driver.find_elements(By.XPATH, "//select[@id='month']/option")
            if len(months) > 1:
                random.choice(months[1:]).click()
            
            # Day
            day_field = self.driver.find_element(By.NAME, "day")
            day_field.clear()
            day_field.send_keys(str(random.randint(1, 28)))
            
            # Year
            year_field = self.driver.find_element(By.NAME, "year")
            year_field.clear()
            year_field.send_keys(str(random.randint(1985, 2000)))
            
            # Gender
            gender_select = self.driver.find_element(By.ID, "gender")
            gender_select.click()
            genders = self.driver.find_elements(By.XPATH, "//select[@id='gender']/option")
            if len(genders) > 1:
                random.choice(genders[1:]).click()
            
            self.simulate_human_behavior()
            
            # Click next
            next_buttons = self.driver.find_elements(By.XPATH, "//span[text()='Next']")
            for btn in next_buttons:
                try:
                    btn.click()
                    break
                except:
                    continue
            
            # Wait for username/password page
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Fill username
            username_field = self.driver.find_element(By.ID, "username")
            username_field.clear()
            username_field.send_keys(username)
            
            # Fill password
            password_field = self.driver.find_element(By.NAME, "Passwd")
            password_field.clear()
            password_field.send_keys(password)
            
            confirm_password_field = self.driver.find_element(By.NAME, "ConfirmPasswd")
            confirm_password_field.clear()
            confirm_password_field.send_keys(password)
            
            self.simulate_human_behavior()
            
            # Click next
            next_buttons = self.driver.find_elements(By.XPATH, "//span[text()='Next']")
            for btn in next_buttons:
                try:
                    btn.click()
                    break
                except:
                    continue
            
            # Check for success or challenges
            time.sleep(5)
            
            current_url = self.driver.current_url
            page_source = self.driver.page_source
            
            if "challenge" in current_url or "verify" in current_url:
                return "verification_required"
            elif "welcome" in current_url or "myaccount" in current_url:
                return "success"
            elif "username" in current_url:
                return "username_taken"
            else:
                return "unknown_status"
                
        except Exception as e:
            logging.error(f"❌ Error filling form: {e}")
            return "error"
    
    def attempt_account_creation(self, index):
        """Attempt to create a single Gmail account"""
        username = self.generate_username(index)
        password = "kaaamoooshi"
        
        logging.info(f"🔄 Attempting to create account {index}: {username}")
        
        try:
            # Navigate to Gmail signup
            self.driver.get("https://accounts.google.com/signup")
            time.sleep(3)
            
            # Fill the form
            status = self.fill_account_info(username, password)
            
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
            
            if status == "success":
                logging.info(f"✅ Account {username} created successfully!")
            elif status == "username_taken":
                logging.warning(f"⚠️ Username {username} is already taken")
            elif status == "verification_required":
                logging.warning(f"🛡️ Verification required for {username}")
            else:
                logging.info(f"ℹ️ Account {username} status: {status}")
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Failed to create account {username}: {e}")
            
            # Save failed attempt
            account_info = {
                'index': index,
                'name': 'A A',
                'username': username,
                'email': f'{username}@gmail.com',
                'password': password,
                'status': f'failed_{str(e)}',
                'timestamp': time.time()
            }
            self.accounts_created.append(account_info)
            return False
    
    def save_results(self):
        """Save results to files"""
        # CSV file
        with open('real_gmail_accounts.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
        with open('real_gmail_accounts.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.accounts_created, jsonfile, ensure_ascii=False, indent=2)
        
        logging.info(f"💾 Results saved: {len(self.accounts_created)} accounts")
    
    def run_creation_process(self, start_index=1, end_index=5):
        """Run the actual account creation process"""
        logging.info("🚀 Starting REAL Gmail account creation process...")
        
        successful_attempts = 0
        
        for i in range(start_index, end_index + 1):
            try:
                if self.attempt_account_creation(i):
                    successful_attempts += 1
                
                # Save progress every 2 accounts
                if i % 2 == 0:
                    self.save_results()
                    logging.info(f"💾 Progress saved at index {i}")
                
                # Longer delay between real attempts
                if i < end_index:
                    delay = random.uniform(10.0, 30.0)
                    logging.info(f"⏳ Waiting {delay:.1f} seconds before next attempt...")
                    time.sleep(delay)
                    
            except KeyboardInterrupt:
                logging.info("⏹️ Process interrupted by user")
                break
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
        
        logging.info("📊 Creation Summary:")
        for status, count in status_count.items():
            logging.info(f"   {status}: {count} accounts")
        
        logging.info(f"🎉 Process completed! Attempted {len(self.accounts_created)} accounts")
        
        return successful_attempts
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()
            logging.info("✅ Chrome driver closed")

def main():
    """Main execution function"""
    creator = None
    try:
        # Get parameters from environment variables
        start_index = int(os.getenv('START_INDEX', '1'))
        end_index = int(os.getenv('END_INDEX', '5'))  # Smaller batch for real attempts
        
        creator = RealGmailCreator()
        success_count = creator.run_creation_process(start_index, end_index)
        
        exit(0 if success_count > 0 else 1)
        
    except Exception as e:
        logging.error(f"💥 Critical error: {e}")
        exit(1)
    finally:
        if creator:
            creator.cleanup()

if __name__ == "__main__":
    main()
