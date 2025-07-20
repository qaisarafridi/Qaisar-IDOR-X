
### 👤 Author: [Qaisar Afridi](https://github.com/yourusername)  
**Qaisar-IDOR-X** is a smart Python3 tool for automated testing of **Insecure Direct Object Reference (IDOR)** vulnerabilities.  
It crawls target websites, identifies URL parameters, and fuzzes them with different values to detect potential IDOR issues while filtering false positives intelligently.

<img width="629" height="296" alt="image" src="https://github.com/user-attachments/assets/74b52f65-87ab-45be-959b-5d2e83e1152d" />

## ⚙️ Features

- ✅ Crawls target URL and extracts real parameterized links
- ✅ Automatically detects common sensitive parameters like `id`, `user_id`, `account_id`, etc.
- ✅ Fuzzes real parameters (not just `id`) with numerical values
- ✅ Filters false positives using semantic response comparison
- ✅ Detects sensitive data leaks (emails, tokens, profiles, etc.)
- ✅ Beautiful figlet banner with author branding
- ✅ Works on unauthenticated pages (future support for login coming soon)

---

## 📦 Requirements

Install the dependencies with:

```bash
pip install -r requirements.txt
