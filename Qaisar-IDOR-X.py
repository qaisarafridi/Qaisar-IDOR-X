#!/usr/bin/env python3
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urljoin
from bs4 import BeautifulSoup
import re, sys, hashlib
from time import sleep

# Fancy Banner
def banner():
    print(r"""
   ____        _                       ________  ____  ____       _  __
  / __ \____ _(_)________ ______      /  _/ __ \/ __ \/ __ \     | |/ /
 / / / / __ `/ / ___/ __ `/ ___/_____ / // / / / / / / /_/ /_____|   / 
/ /_/ / /_/ / (__  ) /_/ / /  /_____// // /_/ / /_/ / _, _/_____/   |  
\___\_\__,_/_/____/\__,_/_/        /___/_____/\____/_/ |_|     /_/|_|  

🔍 Author: Qaisar Afridi | Qaisar-IDOR-X – Smart IDOR Detection Tool
""")

# Extract links from the page
def extract_links(base_url):
    try:
        resp = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        links = set()
        for a in soup.find_all("a", href=True):
            href = urljoin(base_url, a["href"])
            if urlparse(href).netloc == urlparse(base_url).netloc:
                if "=" in href:  # Only keep links with parameters
                    links.add(href)
        return list(links)
    except Exception as e:
        print(f"[!] Error extracting links: {e}")
        return []

# Detect sensitive keywords
def looks_sensitive(text):
    keywords = ["email", "user", "profile", "admin", "account", "token", "address"]
    content = text.lower()
    return any(k in content for k in keywords)

# Diffing logic
def is_different(base, test):
    return hashlib.md5(base.encode()).hexdigest() != hashlib.md5(test.encode()).hexdigest()

# Fuzz parameters
def fuzz_idor(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    for key in query:
        original_value = query[key][0]
        for test_val in range(2, 6):
            query[key] = [str(test_val)]
            new_query = urlencode(query, doseq=True)
            new_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"

            try:
                base_resp = requests.get(url, timeout=10)
                test_resp = requests.get(new_url, timeout=10)

                if is_different(base_resp.text, test_resp.text) and looks_sensitive(test_resp.text):
                    print(f"[⚠️] Potential IDOR on: {new_url}")
            except Exception as e:
                print(f"[!] Request failed for {new_url}: {e}")
            sleep(0.5)

# Main logic
def main(target):
    banner()
    print(f"[+] Crawling target: {target}\n")
    urls = extract_links(target)

    if not urls:
        print("[!] No parameterized links found.")
        return

    for u in urls:
        print(f"[→] Testing: {u}")
        fuzz_idor(u)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 qaisar_idor_x.py <https://target.com>")
        sys.exit(1)
    main(sys.argv[1])
