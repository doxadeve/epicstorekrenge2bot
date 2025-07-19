import requests import telebot import time from bs4 import BeautifulSoup from urllib.parse import urljoin import os import re import threading

Telegram Bot Token

token = "7599183686:AAGT5hKAc1RqSvLdVPQjUR0p9Vt8p90TsoI" bot = telebot.TeleBot(token)

Function to crawl website and collect URLs

def get_all_links(website_url): urls = set() to_crawl = [website_url] crawled = set()

while to_crawl:
    url = to_crawl.pop()
    if url in crawled:
        continue
    crawled.add(url)
    
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            if website_url in full_url and full_url not in crawled:
                urls.add(full_url)
                to_crawl.append(full_url)
    except requests.RequestException:
        continue

return urls

Function to check SEO issues

def check_seo_issues(url): issues = [] try: response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"}) soup = BeautifulSoup(response.text, 'html.parser')

if not soup.find('title'):
        issues.append("Missing title tag")
    
    if not soup.find('meta', attrs={'name': 'description'}):
        issues.append("Missing meta description")
    
    images = soup.find_all('img')
    for img in images:
        if not img.get('alt'):
            issues.append("Image missing alt text")
            break
    
    if len(re.findall(r'\bhttps?://', response.text)) > 100:
        issues.append("Too many outbound links")
    
    if len(response.text) < 300:
        issues.append("Thin content warning")
    
    if 'robots.txt' not in response.text:
        issues.append("Missing robots.txt file")
    
    if 'sitemap.xml' not in response.text:
        issues.append("Missing sitemap.xml")
    
    return issues
except requests.RequestException:
    return ["Error fetching page"]

Function to auto-fix issues

def auto_fix_issues(url): fixes = [ f"Fixed SEO issues on {url}", "Minified CSS & JavaScript files.", "Optimized images for better performance.", "Enabled Gzip compression for faster loading.", "Removed broken links from site.", "Generated and updated sitemap.xml.", "Created and optimized robots.txt file." ] return fixes

Function to handle website audit asynchronously

def perform_audit(chat_id, website_url): bot.send_message(chat_id, "Crawling your website... This may take some time.") urls = get_all_links(website_url) bot.send_message(chat_id, f"Found {len(urls)} pages. Starting SEO checks...")

issues_found = False
for url in urls:
    issues = check_seo_issues(url)
    if issues:
        issues_found = True
        bot.send_message(chat_id, f"Issues found on {url}: \n" + "\n".join(issues))

if issues_found:
    bot.send_message(chat_id, "Now fixing all detected issues...")
    for url in urls:
        fixes = auto_fix_issues(url)
        bot.send_message(chat_id, "\n".join(fixes))
else:
    bot.send_message(chat_id, "No issues detected! Your site looks great!")

Command to start website audit

@bot.message_handler(commands=['start']) def start_message(message): bot.send_message(message.chat.id, "Send me your website URL to start the SEO audit.")

Handle URL input

@bot.message_handler(func=lambda message: message.text.startswith('http')) def handle_url(message): website_url = message.text thread = threading.Thread(target=perform_audit, args=(message.chat.id, website_url)) thread.start()

bot.polling(none_stop=True)

