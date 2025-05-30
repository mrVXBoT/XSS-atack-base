import requests
from urllib.parse import quote_plus, quote
import concurrent.futures
import random
import string
import base64
import re
import argparse
import os
import json
import time
import sys
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

# ASCII Art Logo
def print_banner():
    banner = f"""
    {Fore.RED}██╗   ██╗{Fore.WHITE}██╗  ██╗    {Fore.RED}██╗  ██╗{Fore.WHITE}███████╗███████╗    {Fore.RED}███████╗{Fore.WHITE}██╗   ██╗{Fore.RED}███████╗
    {Fore.RED}██║   ██║{Fore.WHITE}╚██╗██╔╝    {Fore.RED}╚██╗██╔╝{Fore.WHITE}██╔════╝██╔════╝    {Fore.RED}██╔════╝{Fore.WHITE}██║   ██║{Fore.RED}██╔════╝
    {Fore.RED}██║   ██║{Fore.WHITE} ╚███╔╝      {Fore.RED}╚███╔╝ {Fore.WHITE}███████╗███████╗    {Fore.RED}█████╗  {Fore.WHITE}██║   ██║{Fore.RED}█████╗  
    {Fore.RED}╚██╗ ██╔╝{Fore.WHITE} ██╔██╗      {Fore.RED}██╔██╗ {Fore.WHITE}╚════██║╚════██║    {Fore.RED}██╔══╝  {Fore.WHITE}██║   ██║{Fore.RED}██╔══╝  
    {Fore.RED} ╚████╔╝ {Fore.WHITE}██╔╝ ██╗     {Fore.RED}██╔╝ ██╗{Fore.WHITE}███████║███████║    {Fore.RED}███████╗{Fore.WHITE}╚██████╔╝{Fore.RED}███████╗
    {Fore.RED}  ╚═══╝  {Fore.WHITE}╚═╝  ╚═╝     {Fore.RED}╚═╝  ╚═╝{Fore.WHITE}╚══════╝╚══════╝    {Fore.RED}╚══════╝{Fore.WHITE} ╚═════╝ {Fore.RED}╚══════╝
    {Fore.YELLOW}              XSS VULNERABILITY SCANNER v1.0
    {Style.BRIGHT}{Fore.WHITE}              Developed by: {Fore.RED}VX{Fore.WHITE} Security Team
    """
    print(banner)
    print(f"{Fore.CYAN}{'=' * 80}")

# Table formatting function
def print_table_header(headers):
    header_row = ""
    for header in headers:
        header_row += f"{Fore.CYAN}{Style.BRIGHT}{header:<20}{Style.RESET_ALL}"
    
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(header_row)
    print(f"{Fore.CYAN}{'=' * 80}")

def print_table_row(values, status=None):
    row = ""
    for i, value in enumerate(values):
        # Color-code based on status for the first column
        if i == 0 and status:
            if status >= 400:
                color = Fore.RED
            elif status >= 300:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
        elif i == 2:  # Is Reflected column
            color = Fore.GREEN if value == "Yes" else Fore.RED
        else:
            color = Fore.WHITE
            
        row += f"{color}{str(value):<20}{Style.RESET_ALL}"
    
    print(row)

def animate_loading(text, duration=3):
    chars = "-\|/"
    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        sys.stdout.write(f"\r{Fore.YELLOW}{text} {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print()


def generate_random_string(length=20):
    """Generates a random alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_user_agent():
    """Generates a random User-Agent string."""
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.40",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    ]
    return random.choice(agents)

def encode_payload(payload, encoding_type='standard'):
    """
    Encodes the payload using various encoding techniques.
    
    :param payload: The payload to encode
    :param encoding_type: The type of encoding to use (standard, double, base64, js)
    :return: The encoded payload
    """
    if encoding_type == 'standard':
        return quote_plus(payload)
    elif encoding_type == 'double':
        return quote_plus(quote_plus(payload))
    elif encoding_type == 'base64':
        return base64.b64encode(payload.encode()).decode()
    elif encoding_type == 'js':
        # JavaScript escape
        result = ''
        for char in payload:
            if char.isalnum():
                result += char
            else:
                result += '\\x{:02x}'.format(ord(char))
        return result
    else:
        return quote_plus(payload)

def load_payloads_from_file(file_path):
    """Loads XSS payloads from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        payloads = file.read().splitlines()
    return payloads

def launch_xss_attack(url, payload, method="GET", param_name="xss", encoding_type="standard"):
    """
    Launches an XSS attack against the specified URL.
    
    :param url: The target URL
    :param payload: The XSS payload to inject
    :param method: HTTP method (GET or POST)
    :param param_name: The name of the parameter to inject the payload into
    :param encoding_type: The type of encoding to use for the payload
    :return: A dictionary containing the attack result
    """
    # Encode the payload with the specified encoding type
    encoded_payload = encode_payload(payload, encoding_type)
    
    # Prepare headers with random user agent
    headers = {
        'User-Agent': generate_random_user_agent(),
        'Referer': 'https://google.com',
        'Origin': url.split('/')[2] if '/' in url else url,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        if method.upper() == "POST":
            data = {param_name: encoded_payload}
            response = requests.post(url, headers=headers, data=data, timeout=15)
        else:
            # Make sure URL has correct format
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            # Add payload to URL
            attack_url = f"{url}?{param_name}={encoded_payload}"
            response = requests.get(attack_url, headers=headers, timeout=15)
        
        # Get response content and limit size to avoid memory issues
        response_content = response.text[:1000] if len(response.text) > 1000 else response.text
        
        # Check for different forms of reflection (more comprehensive check)
        is_reflected = check_reflection(payload, encoded_payload, response_content)
        
        return {
            'status': response.status_code,
            'content': response_content,
            'is_reflected': is_reflected,
            'payload': payload,
            'encoded_payload': encoded_payload,
            'method': method,
            'param_name': param_name,
            'encoding_type': encoding_type
        }
    except requests.exceptions.RequestException as e:
        return {'error': str(e), 'payload': payload, 'method': method, 'param_name': param_name}

def test_multiple_parameters(url, payload, method="GET"):
    parameters = ["xss", "search", "q", "query", "input", "data", "id", "page", "p", "s", "term"]
    results = []
    
    # Make sure URL has correct format
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    # Test with different encoding types for more comprehensive coverage
    encoding_type = "standard"  # Can be changed to 'double', 'base64', 'js'
    
    for param in parameters:
        try:
            if method.upper() == "POST":
                encoded_payload = encode_payload(payload, encoding_type)
                data = {param: encoded_payload}
                headers = {
                    'User-Agent': generate_random_user_agent(),
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                response = requests.post(url, headers=headers, data=data, timeout=10)
            else:
                encoded_payload = encode_payload(payload, encoding_type)
                attack_url = f"{url}?{param}={encoded_payload}"
                headers = {'User-Agent': generate_random_user_agent()}
                response = requests.get(attack_url, headers=headers, timeout=10)
            
            response_content = response.text[:1000] if len(response.text) > 1000 else response.text
            is_reflected = check_reflection(payload, encoded_payload, response_content)
            
            results.append({
                'param_name': param,
                'status': response.status_code,
                'content': response_content,
                'is_reflected': is_reflected,
                'payload': payload,
                'encoded_payload': encoded_payload,
                'method': method,
                'encoding_type': encoding_type
            })
        except requests.exceptions.RequestException:
            # Skip failed requests for parameters without interrupting the scan
            continue
    
    return results

def check_security_headers(url):
    """Checks for security headers such as CSP."""
    try:
        response = requests.get(url, timeout=15)
        headers = response.headers
        if 'Content-Security-Policy' in headers:
            print(f"{Fore.YELLOW}[+] CSP detected: {Fore.RED}{headers['Content-Security-Policy']}")
        else:
            print(f"{Fore.GREEN}[+] No CSP detected. {Fore.YELLOW}(Site may be vulnerable to XSS)")
        
        # Check for other security headers
        security_headers = {
            'X-XSS-Protection': 'XSS Protection',
            'X-Frame-Options': 'Frame Options',
            'X-Content-Type-Options': 'Content Type Options',
            'Strict-Transport-Security': 'HSTS'
        }
        
        print(f"{Fore.CYAN}\nSecurity Headers:\n{'-' * 50}")
        for header, name in security_headers.items():
            if header in headers:
                print(f"{Fore.GREEN}[+] {name}: {headers[header]}")
            else:
                print(f"{Fore.RED}[-] {name}: Not found")
    except Exception as e:
        print(f"{Fore.RED}[-] Error checking headers: {str(e)}")

def check_reflection(payload, encoded_payload, response_content):
    """More comprehensive check for payload reflection"""
    # Check for direct reflection
    if payload in response_content:
        return True
    
    # Check for URL-encoded reflection
    if encoded_payload in response_content:
        return True
    
    # Check for HTML-encoded reflection
    html_encoded = payload.replace('<', '&lt;').replace('>', '&gt;')
    if html_encoded in response_content:
        return True
    
    # Check for partial reflections (useful for longer payloads)
    key_elements = ['script', 'alert', 'onerror', 'onclick', 'onload', 'javascript']
    for element in key_elements:
        if element in payload.lower() and element in response_content.lower():
            return True
    
    return False

def print_summary(successful_payloads):
    if not successful_payloads:
        print(f"\n{Fore.RED}No successful XSS payloads found!")
        return
        
    print(f"\n{Fore.GREEN}{Style.BRIGHT}XSS Scan Summary{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * 80}")
    print(f"{Fore.GREEN}Found {len(successful_payloads)} successful XSS payloads!")
    
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Top 5 Most Effective Payloads:{Style.RESET_ALL}")
    for i, result in enumerate(successful_payloads[:5], 1):
        print(f"{Fore.WHITE}{i}. {Fore.CYAN}{result['payload']} {Fore.WHITE}(via {Fore.GREEN}{result['method']}{Fore.WHITE} to parameter {Fore.GREEN}{result.get('param_name', 'xss')})")

def main():
    # Display banner and welcome message
    print_banner()
    print(f"{Fore.WHITE}This tool scans websites for {Fore.RED}Cross-Site Scripting (XSS){Fore.WHITE} vulnerabilities")
    print(f"{Fore.YELLOW}WARNING: Only use on websites you have permission to test!\n")
    
    # Get target URL
    target_url = input(f"{Fore.CYAN}Enter the target URL {Fore.WHITE}(e.g., https://example.com): ").strip()
    payload_file = "payload.txt"
    
    # Initialize successful payloads list for summary
    log_result.successful_payloads = []
    
    # Load payloads
    try:
        payloads = load_payloads_from_file(payload_file)
        print(f"{Fore.GREEN}[+] Loaded {len(payloads)} payloads from {payload_file}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error loading payloads: {str(e)}")
        return
    
    # Limit number of payloads for faster testing if needed
    # payloads = payloads[:50]  # Uncomment to limit payloads
    
    # Display table headers for results
    headers = ['Status', 'Method', 'Reflected', 'Parameter', 'Payload']
    print_table_header(headers)
    
    # Check security headers
    animate_loading("Checking security headers", 1)
    check_security_headers(target_url)
    
    # Run tests with different methods and parameters
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        print(f"\n{Fore.YELLOW}[*] Testing GET requests with {len(payloads)} payloads...")
        animate_loading("Scanning", 2)
        
        # GET requests
        futures = [executor.submit(launch_xss_attack, target_url, payload, "GET") for payload in payloads]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            log_result(result)
        
        print(f"\n{Fore.YELLOW}[*] Testing POST requests with {len(payloads)} payloads...")
        animate_loading("Scanning", 2)
        
        # POST requests
        futures = [executor.submit(launch_xss_attack, target_url, payload, "POST") for payload in payloads]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            log_result(result)
        
        print(f"\n{Fore.YELLOW}[*] Testing multiple parameters...")
        animate_loading("Scanning additional parameters", 2)
        
        # Test multiple parameters (using a subset of payloads for speed)
        param_test_payloads = payloads[:min(25, len(payloads))]
        futures = [executor.submit(test_multiple_parameters, target_url, payload, "GET") for payload in param_test_payloads]
        for future in concurrent.futures.as_completed(futures):
            results = future.result()
            for result in results:
                log_result(result)
    
    # Print summary of findings
    print_summary(log_result.successful_payloads)
    
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(f"{Fore.WHITE}Scan completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Style.BRIGHT}{Fore.RED}VX{Fore.WHITE} Security Team | XSS Scanner v1.0")
    print(f"{Fore.CYAN}{'=' * 80}")

def log_result(result):
    if 'error' in result:
        print(f"{Fore.RED}Error: {result['error']}")
        return
        
    # Format for table output
    status = result['status']
    is_reflected = 'Yes' if result['is_reflected'] else 'No'
    method = result['method']
    payload = result['payload']
    param = result.get('param_name', 'xss')
    
    # Truncate payload if too long
    if len(payload) > 17:
        payload = payload[:15] + '...'
    
    # Print as table row
    values = [status, method, is_reflected, param, payload]
    print_table_row(values, status)
    
    # Store successful payloads for summary
    if result['is_reflected']:
        if not hasattr(log_result, 'successful_payloads'):
            log_result.successful_payloads = []
        log_result.successful_payloads.append(result)

if __name__ == "__main__":
    try:
        # Check if colorama is installed, if not, install it
        try:
            import colorama
        except ImportError:
            print("Installing required package: colorama")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
            print("Package installed successfully!\n")
            # Restart the script to use the newly installed package
            os.execv(sys.executable, ['python'] + sys.argv)
        
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Scan interrupted by user.\n")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}\n")