cd /backend/scrapy_thai_app/thai_spider
# scrapy list
echo "Hello.  This script is used to run scrape Thai website"
python3 multi_run_thai.py
# scrapy crawl dbdcrawler_Thai -o /backend/temp/thaiVersion.json