# XSS-atack-base
<div align="center">

# 🛡️ XSS Vulnerability Scanner 🛡️

<img src="./logo.svg" alt="XSS Scanner Logo" width="250" height="250">

*A powerful tool for detecting Cross-Site Scripting (XSS) vulnerabilities in web applications*

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0-red.svg)](https://github.com/yourusername/xss-scanner/)

</div>

## ✨ Features

- 🔍 Tests for XSS vulnerabilities using both GET and POST methods
- 🔄 Tests multiple common parameters automatically
- 🔒 Checks for security headers such as Content Security Policy (CSP)
- ⚡ Concurrent testing with multiple threads for efficiency
- 🕵️ Uses random user agents to avoid detection
- 📚 Support for extensive XSS payloads

## 📋 Requirements

- Python 3.6+
- Required packages listed in `requirements.txt`

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/mrVXBoT/XSS-atack-base.git
cd XSS-atack-base

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

```bash
python XSS.py
```

You will be prompted to enter the target URL. The tool will then automatically:

1. Check for security headers like CSP
2. Test the target with various XSS payloads using GET requests
3. Test the target with various XSS payloads using POST requests
4. Test multiple common parameters (search, q, query, etc.)

## 📊 Results

The tool provides detailed output for each test, including:

- HTTP status code
- Whether the payload was reflected in the response
- The actual payload used
- The HTTP method used
- A preview of the response content

## 📝 Example

```
Enter the target URL (e.g., https://example.com): https://vulnerable-site.com

[+] No CSP detected.
==================================================
Status Code: 200
Is Reflected: Yes
Payload: <script>alert(1)</script>
Method: GET
Response Content: <html>...<script>alert(1)</script>...</html>
==================================================
```

## ⚠️ Disclaimer

This tool is for **educational purposes and ethical security testing only**. Always obtain proper authorization before testing any website for vulnerabilities. Unauthorized security testing is illegal and unethical.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### Made with ❤️ for the security research community

</div>


