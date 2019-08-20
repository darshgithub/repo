import sys
import os

page_count = int(sys.argv[1])

while page_count > 0:
    os.system('scrapy crawl mesh')
    page_count = page_count - 32
