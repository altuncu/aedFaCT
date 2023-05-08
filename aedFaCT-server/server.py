from urllib.parse import urlparse
from flask import Flask, request
from flask_cors import CORS
import requests
import jsonpickle
from util.util import *
from newspaper import Article
from util.m_sifrank.embeddings import sent_emb_sif, word_emb_elmo
from util.m_sifrank.model.method import SIFRank_plus
from stanfordcorenlp import StanfordCoreNLP
from pybliometrics.scopus import ScopusSearch
from model.researcher import Researcher, sort_researchers
from model.news_article import NewsArticle
from model.publication import Publication

# Load SIFRank model
options_file = "./util/m_sifrank/auxiliary_data/elmo_2x4096_512_2048cnn_2xhighway_options.json"
weight_file = "./util/m_sifrank/auxiliary_data/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"
ELMO = word_emb_elmo.WordEmbeddings(options_file, weight_file, cuda_device=-1)
SIF = sent_emb_sif.SentEmbeddings(ELMO, lamda=1.0)
elmo_layers_weight = [0.0, 1.0, 0.0]

# Global variables
article = None
article_title = ""
article_source = ""
researchers = []
terms = []

############ MODIFY THESE VALUES ##############
# Google API keys
google_api_key = "<Enter your Google API key here>"
google_cx_ms = "<Enter cx value for your custom search engine covering mainstream news outlets>"
google_cx_sci = "<Enter cx value for your custom search engine covering scientific news outlets>"
google_cx_cse = "<Enter cx value for your custom search engine for general Google search results>"
################################################

# Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

# Get keywords from input article
@app.route('/extract-keywords/',methods=["GET", "POST"])
def extract_keywords():
    if request.method == 'POST':
        global article, article_title, article_source
        article = Article(request.json['url'])
        article.download()
        article.parse()
        article_title = article.title
        article_source = urlparse(article.url).hostname
        en_model = StanfordCoreNLP(r'./util/m_sifrank/stanford-corenlp-full-2018-02-27')
        keywords = SIFRank_plus(article.text, SIF, en_model, N=10, elmo_layers_weight=elmo_layers_weight)
        en_model.close()
        return {'keywords': jsonpickle.encode(list(dict.keys(keywords)))}
    return '', 200

# Get articles from Scopus
@app.route('/get-pubs/',methods=["GET", "POST"])
def get_pubs():
    if request.method == "POST":
        global terms
        terms = request.json['keywords']
        terms_copy = terms.copy()
        while True:
            query = " AND ".join(["\"" + t + "\"" for t in terms_copy])
            search_results = ScopusSearch('TITLE-ABS-KEY (' + query + ')', integrity_fields=["eid", "title", "author_names"], 
                                            integrity_action="warn", refresh=True, sort="relevancy")
            docs = search_results.get_eids()
            if len(docs) > 0 or len(terms) == 1:
                break
            else:
                terms_copy = terms_copy[:-1] # Remove last keyword
        print("Found {} docs".format(len(docs)))
        
        global researchers
        publications = []
        researchers.clear()

        print("Getting publications from Scopus")
        for d in docs[:10]:
            try:
                print("Getting publication {}".format(d))
                publication_obj = Publication(d, terms)
                for a in publication_obj.authors:
                    if a.auid in [r.auid for r in researchers]:
                        print("Author {} already in researchers".format(a))
                        next(r for r in researchers if r.auid == a.auid).append_related_pubs(publication_obj.bib_entry)
                    else:
                        print("Getting author {}".format(a))
                        researcher = Researcher(a.auid)
                        researcher.append_related_pubs(publication_obj.bib_entry)
                        researchers.append(researcher)
                publications.append(publication_obj)
            except Exception as e:
                print("Error getting article {}: {}".format(d, str(e)))
                continue       
            
        researchers = sort_researchers(researchers)
        print("{} publications found".format(len(publications)))
        print("{} researchers found".format(len(researchers)))
        return {'publications': jsonpickle.encode(publications), 
                'researchers': jsonpickle.encode(researchers)}

# General search with keywords
@app.route('/get-news/',methods=["GET", "POST"])
def get_news():
    if request.method == "POST":
        try:    
            print("Searching with the keywords")
            global terms
            news_articles = []
            google_terms = terms.copy()
            search_url_base_ms = "https://www.googleapis.com/customsearch/v1/siterestrict?key=" + google_api_key + "&cx=" + google_cx_ms + "&q="
            search_url_base_sci = "https://www.googleapis.com/customsearch/v1/siterestrict?key=" + google_api_key + "&cx=" + google_cx_sci + "&q="
            search_url_base_cse = "https://www.googleapis.com/customsearch/v1?key=" + google_api_key + "&cx=" + google_cx_cse + "&q="
            for u in [search_url_base_ms, search_url_base_sci, search_url_base_cse]:
                query = "+".join([t for t in google_terms])
                search_url = u + query.replace(" ", "+")
                print("Searching with: " + search_url)
                try:
                    total_count = requests.get(url=search_url, headers=headers).json().get("searchInformation").get("totalResults")
                    print("Found {} results".format(total_count))
                except Exception as e:
                    print("Error getting total results: " + str(e))
                    total_count = "0"
                    continue
                if total_count != "0":
                    try:
                        results = requests.get(url=search_url, headers=headers).json().get("items")
                        print("Found {} items".format(len(results)))
                        news_articles += results
                    except Exception as e:
                        print("Error getting items: " + str(e))
        except Exception as e:
            print("Error getting news articles: " + str(e))

        # Get expert comments from the collected news articles
        print("Retrieving expert comments")
        global researchers
        preferred_articles = []
        other_articles = []
        print("Processing {} news articles".format(len(news_articles)))
        for s in news_articles:
            try:
                news_article_obj = NewsArticle(s.get("link"))
                if news_article_obj.comments and news_article_obj.is_credible() and article_title != news_article_obj.title:
                    bool = set([r.full_name for r in researchers] + [r.cleaned_name for r in researchers]) & set(news_article_obj.persons)
                    if bool:
                        preferred_articles.append(news_article_obj)
                    else:
                        other_articles.append(news_article_obj)
            except Exception as e:
                print("Error processing news article: " + str(e))
                continue

        result_articles = preferred_articles + other_articles
        print("{} articles found".format(len(result_articles)))
        return {'articles': jsonpickle.encode(result_articles)}

if __name__ == '__main__':
    app.run()
