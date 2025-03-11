from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import os
import json
from datetime import datetime
from services.url_validator import validate_url
from services.functional_tester import FunctionalTester
from services.performance_tester import PerformanceTester
from services.security_tester import SecurityTester
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# Store results in memory
test_results = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', results=test_results)

@app.route('/test', methods=['POST'])
def run_test():
    url = request.form.get('url')
    
    if not validate_url(url):
        flash('Invalid URL provided', 'error')
        return redirect(url_for('index'))
    
    try:
        # Initialize testers
        functional_tester = FunctionalTester()
        performance_tester = PerformanceTester()
        security_tester = SecurityTester()
        
        # Run tests
        functional_results = functional_tester.run_tests(url)
        performance_results = performance_tester.run_tests(url)
        security_results = security_tester.run_tests(url)
        
        # Compile results
        test_result = {
            'url': url,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'functional': functional_results,
            'performance': performance_results,
            'security': security_results
        }
        
        # Store results
        test_results.insert(0, test_result)
        
        flash('Testing completed successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash(f'Error during testing: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)