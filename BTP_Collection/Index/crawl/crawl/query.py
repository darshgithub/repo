from whoosh import index
from whoosh.qparser import QueryParser
from bs4 import BeautifulSoup
import hashlib
def parse_html(html):
    keys = html.keys()
    if len(keys) == 2:
        soup = BeautifulSoup(html['body'], features='lxml')
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        text = text.replace('\n', ' ').lower()
        hash_text = hashlib.md5(text.encode())
        return (text, hash_text.hexdigest(), ' ', str(soup.title.string), html['url'])
    if len(keys) == 3:
        text = html['body']
        hash_text = hashlib.md5(text.encode())
        return (text, hash_text.hexdigest(),  html['tags'], ' ', html['url'])
    if len(keys) == 4:
        return (html['body'], html['hash'], html['tags'], ' ', html['url'])
    return (html['body'], html['hash'], html['tags'], html['title'], html['url'])


ix = index.open_dir("mesh_index")
# qp = QueryParser("body", schema=ix.schema)
# query = "Cell"
# q = qp.parse(query)
searcher = ix.searcher().documents()
writer = ix.writer()
i = 0
for doc in searcher:
    text, hash, tags, title, url = parse_html(doc)
    writer.update_document(url=url, body = text, tags = tags, hash = hash, title=title)
    print(str(i+1) + ' completed.')
    i += 1
writer.commit()

"""
with searcher as s:
    results = s.search_page(q, 2, pagelen=10)
    print(dir(results.results))
    similar = results[0].more_like_this('body')
    print(similar.top_n)
    # soup = BeautifulSoup(results[0]['body'])
    # print(soup.title.string)
"""
