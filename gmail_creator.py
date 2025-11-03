#!/usr/bin/env python3
"""
Gmail Account Creator - Educational Project
Optimized for GitHub Actions
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
        logging.FileHandler('gmail_creator.log'),
        logging.StreamHandler()
    ]
)

class GmailCreator:
    def __init__(self):
        self.driver = None
        self.accounts_created = []
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver for GitHub Actions"""
        chrome_options = Options()
        
        # Options for headless environment
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set user agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
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
    
    def simulate_human_delay(self):
        """Simulate human-like delay"""
        delay = random.uniform(2.0, 5.0)
        time.sleep(delay)
    
    def save_progress(self, index):
        """Save progress to file"""
        progress = {
            'last_index': index,
            'total_created': len(self.accounts_created),
            'timestamp': time.time()
        }
        with open('progress.json', 'w') as f:
            json.dump(progress, f)
    
    def load_progress(self):
        """Load progress from file"""
        try:
            with open('progress.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def create_single_account(self, index):
        """Attempt to create a single Gmail account"""
        username = self.generate_username(index)
        password = "kaaamoooshi"
        
        logging.info(f"🔄 Attempting to create account {index}/100: {username}")
        
        try:
            # Navigate to signup page
            self.driver.get("https://accounts.google.com/signup")
            self.simulate_human_delay()
            
            # Fill personal information
            first_name_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "firstName"))
            )
            first_name_field.send_keys("A")
            
            last_name_field = self.driver.find_element(By.NAME, "lastName")
            last_name_field.send_keys("A")
            
            # Click next
            next_buttons = self.driver.find_elements(By.XPATH, "//button/span[text()='Next']")
            if next_buttons:
                next_buttons[0].click()
                self.simulate_human_delay()
            
            # Check if we hit a CAPTCHA or verification
            if "challenge" in self.driver.current_url.lower() or "verify" in self.driver.current_url.lower():
                logging.warning(f"⚠️ Verification required for account {username}")
                return False
            
            # Save account info even if not fully completed
            account_info = {
                'index': index,
                'name': 'A A',
                'username': username,
                'email': f'{username}@gmail.com',
                'password': password,
                'status': 'requires_manual_verification'
            }
            
            self.accounts_created.append(account_info)
            logging.info(f"✅ Account {username} processed (requires manual verification)")
            
            return True
            
        except TimeoutException:
            logging.warning(f"⏰ Timeout occurred for account {username}")
            return False
        except Exception as e:
            logging.error(f"❌ Error creating account {username}: {str(e)}")
            return False
    
    def save_results(self):
        """Save results to CSV and JSON files"""
        # Save to CSV
        with open('gmail_accounts.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Index', 'Name', 'Username', 'Email', 'Password', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for account in self.accounts_created:
                writer.writerow({
                    'Index': account['index'],
                    'Name': account['name'],
                    'Username': account['username'],
                    'Email': account['email'],
                    'Password': account['password'],
                    'Status': account['status']
                })
        
        # Save to JSON
        with open('gmail_accounts.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.accounts_created, jsonfile, ensure_ascii=False, indent=2)
        
        logging.info(f"💾 Results saved: {len(self.accounts_created)} accounts")
    
    def run_creation_process(self, start_index=1, end_index=100):
        """Run the account creation process"""
        logging.info("🚀 Starting Gmail account creation process...")
        
        # Load previous progress
        progress = self.load_progress()
        if progress and os.getenv('RESUME_PROGRESS', 'true').lower() == 'true':
            start_index = progress['last_index'] + 1
            logging.info(f"📚 Resuming from index {start_index}")
        
        successful_creations = 0
        
        for i in range(start_index, end_index + 1):
            try:
                if self.create_single_account(i):
                    successful_creations += 1
                
                # Save progress periodically
                if i % 5 == 0:
                    self.save_progress(i)
                    self.save_results()
                
                # Random delay between attempts
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
        self.save_progress(end_index)
        
        logging.info(f"🎉 Process completed! Successfully processed {successful_creations} out of {end_index - start_index + 1} accounts")
        
        return successful_creations
    
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
        end_index = int(os.getenv('END_INDEX', '100'))
        
        creator = GmailCreator()
        success_count = creator.run_creation_process(start_index, end_index)
        
        # Set output for GitHub Actions
        if os.getenv('GITHUB_ACTIONS'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
                print(f'accounts_created={success_count}', file=fh)
        
        exit(0 if success_count > 0 else 1)
        
    except Exception as e:
        logging.error(f"💥 Critical error: {e}")
        exit(1)
    finally:
        if creator:
            creator.cleanup()

if __name__ == "__main__":
    main()
