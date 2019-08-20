from whoosh import index
from scrapy.linkextractors import LinkExtractor
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from bs4 import BeautifulSoup
from mysql.connector import Error
import scrapy
import time
import hashlib
import mysql.connector as mysql

class MeshSpider(scrapy.Spider):
    name = "mesh"

    def __init__(self):
        self.extractor = LinkExtractor()
        self.write = index.open_dir("mesh_index").writer()
        file = open('urls/indexed.txt')
        self.count = int(file.readline().rstrip("\n"))
        self.temp = 0
        self.LIMIT = 32
        self.urls = []
        self.data = self._get_start_data('terms.txt', as_dict=True)
        try:
            self.thread = mysql.connect(host='localhost',
                                        user='mesh_admin',
                                        passwd='i@am@great@no',
                                        database='mesh_visited')
            self.cursor = self.thread.cursor()
        except Error as e:
            raise Exception("Error while connecting to MySQL database ", e)

    def _get_start_urls(self, filename, **kwargs):
        file = open(filename)
        line = file.readline().rstrip("\n")
        if kwargs.get('as_dict', False):
            urls = {}
            while line != "":
                urls[line] = True
                line = file.readline().rstrip("\n")
        else:
            urls = []
            while line != "":
                urls.append(line)
                line = file.readline().rstrip("\n")
            urls = list(set(urls))
        return urls

    _get_start_data = _get_start_urls

    def _insert(self, **kwargs):
        query = "INSERT INTO visited_urls (urls, status) VALUES (%s, %s)"
        values = (kwargs.get('url', ''), kwargs.get('status', True))
        self.cursor.execute(query, values)
        self.thread.commit()

    def _check(self, *args):
        query = "SELECT status FROM visited_urls WHERE urls = %s"
        self.cursor.execute(query, (args[0], ))
        status = self.cursor.fetchall()
        if len(status) > 0:
            return status[0][0]
        return False

    def start_requests(self):
        self.urls = self._get_start_urls('urls/seeds.txt')

        i = 0
        while self.temp < self.LIMIT:
            if self.temp > self.LIMIT:
                break
            yield scrapy.Request(url=self.urls[i], callback=self.parse)
            i += 1

    def parse(self, response):
        if self._check(response.url) is False:
            soup = BeautifulSoup(response.text, features='lxml')
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            text = text.replace('\n', ' ').lower()
            keywords = []
            for term in text.split(" "):
                if self.data.get(term, False):
                    keywords.append(term)
            keywords = list(set(keywords))
            if len(keywords) >= 5:
                hash_text = hashlib.md5(text.encode())
                self.write.add_document(url = response.url, body = text, tags = ','.join(keywords), hash = hash_text.hexdigest(), title = str(soup.title.string))
                self._insert(url=response.url, status=True)
                self.count += 1
                self.temp += 1
        next_page = [x.url for x in self.extractor.extract_links(response)]
        for url in next_page:
            if self._check(url) is False:
                self.urls.append(url)

    def __del__(self):
        self.write.commit()
        self.thread.close()
        file = open('urls/indexed.txt', 'w')
        file.write(str(self.count) + '\n')
