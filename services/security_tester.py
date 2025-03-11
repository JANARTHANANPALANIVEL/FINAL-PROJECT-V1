from zapv2 import ZAPv2
import time

class SecurityTester:
    def __init__(self):
        self.zap = ZAPv2(
            apikey='c9sqolnd0e46dkqc75o5gd3hhc',
            proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
        )
        
    def run_tests(self, url):
        results = {
            'alerts': [],
            'risk_level': 'Low',
            'scan_time': None
        }
        
        try:
            # Start passive scan
            self.zap.urlopen(url)
            time.sleep(2)  # Wait for passive scan
            
            # Start active scan
            scan_id = self.zap.ascan.scan(url)
            
            # Get results
            alerts = self.zap.core.alerts()
            results['alerts'] = [
                {
                    'risk': alert['risk'],
                    'name': alert['name'],
                    'description': alert['description']
                }
                for alert in alerts
            ]
            
            # Determine risk level
            risk_levels = [alert['risk'] for alert in alerts]
            if 'High' in risk_levels:
                results['risk_level'] = 'High'
            elif 'Medium' in risk_levels:
                results['risk_level'] = 'Medium'
                
        except Exception as e:
            results['error'] = str(e)
            
        return results