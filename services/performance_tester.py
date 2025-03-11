import requests
from bs4 import BeautifulSoup
import time

class PerformanceTester:
    def run_tests(self, url):
        results = {
            'load_time': 0,
            'page_size': 0,
            'resource_count': 0
        }
        
        try:
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            
            # Calculate load time
            results['load_time'] = round(end_time - start_time, 2)
            
            # Calculate page size
            results['page_size'] = len(response.content) / 1024  # Size in KB
            
            # Count resources
            soup = BeautifulSoup(response.text, 'html.parser')
            resources = soup.find_all(['img', 'script', 'link'])
            results['resource_count'] = len(resources)
            
        except Exception as e:
            results['error'] = str(e)
            
        return results