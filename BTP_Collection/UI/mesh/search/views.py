from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
import whoosh as wh
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import FileStorage
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
cache = TTLCache(maxsize=100, ttl=300)
# Create your views here.
per_page = 10

def parse(results, **kwargs):
    new_results = []
    analyzer = wh.analysis.RegexTokenizer()
    fragmenter = wh.highlight.ContextFragmenter(maxchars=300, surround=50)
    formatter = wh.highlight.UppercaseFormatter()
    for result in results:
        parsed_dict = {}
        text = result['body']
        # parsed_dict['title'] = result['title']
        parsed_dict['body'] = wh.highlight.highlight(text, kwargs.get('query', None), analyzer, fragmenter, formatter, top=3)
        parsed_dict['url'] = result['url']
        similar = result.more_like_this('body')
        parsed_dict['similar'] = [str(similar[i]['url']) for i in range(min(len(similar.top_n), 1))]
        new_results.append(parsed_dict)
    return new_results

def index(request):
    template = loader.get_template('search/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

@cached(cache)
def results(request):
    template = loader.get_template('search/results.html')
    query = request.GET.get('q', '')
    page = int(request.GET.get('p', 1))
    if query != '':
        storage = FileStorage("/home/gagandeep/Academics/BTP/Index/crawl/crawl/mesh_index")
        ix = storage.open_index()
        qp = QueryParser("body", schema=ix.schema, termclass=wh.query.Variations)
        q = qp.parse(query)
        searcher = ix.searcher()
        with searcher as s:
            results = s.search_page(q, page, pagelen = per_page)
            total, time = results.total, results.results.runtime
            if results.pagecount >= page:
                results = parse(results, query=set(query.split(" ")))
                context = {'results':results, 'query':query, 'total':total, 'time':time}
                return HttpResponse(template.render(context, request))
    template = loader.get_template('search/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
