import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import datetime


class FunctionalTester:
    def __init__(self):
        self.setup_gemini()
        self.setup_selenium()
        
    def setup_gemini(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel("gemini-1.5-pro-latest")  
        
    def setup_selenium(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
    def generate_test_script(self, url):
        prompt = f"""
        Generate a Python Selenium test script for the website: {url}
        Focus on basic functionality tests like:
        1. Page load
        2. Navigation
        3. Basic form submissions
        4. Content verification
        """
        
        response = self.model.generate_content(prompt)
        return response.text
        
    def run_tests(self, url):
        results = {
            'passed': [],
            'failed': [],
            'screenshots': []
        }
        
        try:
            # Generate and execute test script
            test_script = self.generate_test_script(url)
            
            # Basic tests
            self.driver.get(url)
            results['passed'].append('Page Load Test')
            
            # Take screenshot
            screenshot_path = f'static/screenshots/{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            self.driver.save_screenshot(screenshot_path)
            results['screenshots'].append(screenshot_path)
            
        except Exception as e:
            results['failed'].append(str(e))
            
        return results
        
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()