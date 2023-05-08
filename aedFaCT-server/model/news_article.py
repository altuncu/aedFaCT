from urllib.parse import urlparse
import spacy
import func_timeout
from newspaper import Article
from util.util import *

# Load spacy model
nlp = spacy.load('en_core_web_md')

# Global variables
cred_rating_urls = {"www.npr.org": "https://mediabiasfactcheck.com/npr/",
                    "www.bbc.com": "https://mediabiasfactcheck.com/bbc/",
                    "www.nbcnews.com": "https://mediabiasfactcheck.com/nbc-news/",
                    "www.cbsnews.com": "https://mediabiasfactcheck.com/cbs-news/",
                    "www.abcnews.go.com": "https://mediabiasfactcheck.com/abc-news/",
                    "www.euronews.com": "https://mediabiasfactcheck.com/euronews/",
                    "www.apnews.com": "https://mediabiasfactcheck.com/associated-press/",
                    "www.pbs.org": "https://mediabiasfactcheck.com/pbs/",
                    "news.sky.com": "https://mediabiasfactcheck.com/sky-news/",
                    "www.reuters.com": "https://mediabiasfactcheck.com/reuters/",
                    "www.science.org": "https://mediabiasfactcheck.com/science-magazine/",
                    "www.eurekalert.org": "https://mediabiasfactcheck.com/eurekaalert/",
                    "www.sciencedaily.com": "https://mediabiasfactcheck.com/science-daily/",
                    "www.sciencenews.org": "https://mediabiasfactcheck.com/science-news/",
                    "www.technologyreview.com": "https://mediabiasfactcheck.com/mit-technology-review/",
                    "www.the-scientist.com": "https://mediabiasfactcheck.com/the-scientist/",
                    "www.popsci.com": "https://mediabiasfactcheck.com/popular-science/",
                    "www.sciencealert.com": "https://mediabiasfactcheck.com/sciencealert/",
                    "www.livescience.com": "https://mediabiasfactcheck.com/live-science/",
                    "theconversation.com": "https://mediabiasfactcheck.com/the-conversation/"
                    }

class NewsArticle:
    def __init__(self, url):
        self.url = url
        self.article = runFunction(self.__get_article__, 10, None)
        
        if not self.__is_valid__():
            raise Exception("Invalid article")

        self.title = self.article.title
        self.text = self.article.text
        self.source = urlparse(url).hostname
        self.source_category = self.__get_source_category__(self.source)

        if self.source in cred_rating_urls:
            self.cred_rating_url = cred_rating_urls[self.source]

        self.date = self.__set_date__()
        self.comments, self.persons, self.orgs = self.__retrieve_comments__()

    def __is_valid__(self):
        if self.article is None or None in [self.article.title, self.article.text]:
            return False
        return True

    def __get_article__(self):
        try:
            article = Article(self.url)
            article.download()
            article.parse()
            return article
        except Exception as e:
            print("Error retrieving article: " + str(e))
            return None

    def __get_source_category__(self, source):
        if source in ["www.theguardian.com", "www.bbc.com", "www.reuters.com", "www.npr.org", 
                      "www.nbcnews.com", "www.cbsnews.com", "abcnews.go.com", "www.euronews.com", 
                      "apnews.com", "www.pbs.org"]:
            return "mainstream"
        elif source in ["www.science.org", "www.eurekalert.org", "www.sciencedaily.com", "www.sciencenews.org", 
                        "www.technologyreview.com", "www.the-scientist.com", "www.popsci.com", "www.sciencealert.com", 
                        "www.livescience.com", "theconversation.com"]:
            return "science"
        else:
            return "other"

    def __set_date__(self):
        if self.article.publish_date:
            return self.article.publish_date.strftime("%d.%m.%Y")
        else:
            return "Unknown"

    def __retrieve_comments__(self):
        try:
            print("Retrieving comments from " + self.url + "...")
            spacy_doc = nlp(self.text)
            parags = paragraphs(spacy_doc)
            persons = set()
            orgs = set()
            content = ""
            org_indicators = ["university", "institute", "academy", "research center", "research centre", "school of"]
            quotes = ["\"", "\'", "“", "”", "‘", "’"]

            for ent in spacy_doc.ents:
                if ent.label_ == 'PERSON':
                    persons.add(ent.text)
                if ent.label_ == 'ORG' and any(t in ent.text.lower() for t in org_indicators):
                    orgs.add(ent.text)

            # The Conversation articles are written by academics
            if "theconversation.com/" in self.url:
                self.article.nlp()
                content = str(self.article.summary)
                if any(person in content for person in persons) or any(org in content for org in orgs) or any(m in content for m in quotes):
                    content = "".join(["<b>" + t.text + "</b>" + t.whitespace_ if t.ent_type_ in ['PERSON', 'ORG'] else t.text + t.whitespace_ for t in spacy_doc])
                return content, persons, orgs
            else: 
                for p in parags:
                    if any(person in p.text for person in persons) and any(org in p.text for org in orgs) and any(m in p.text for m in quotes):
                        content += "".join(["<b>" + t.text + "</b>" + t.whitespace_ if t.ent_type_ in ['PERSON', 'ORG'] else t.text + t.whitespace_ for t in p]).strip() + "<br>"
                if content == "":
                    return None, None, None
                else:
                    return content, persons, orgs
        except Exception as e:
            print("Error retrieving comments: " + str(e))
            return None, None, None

    def is_credible(self):
        f = open('util/data/unreliable-sources.txt', 'r', encoding='utf8')
        if binary_search(f, self.source):
            f.close()
            return False
        else:
            f.close()
            return True

# Helper functions
def paragraphs(document):
    start = 0
    for token in document:
        if token.is_space and token.text.count("\n") > 1:
            yield document[start:token.i]
            start = token.i
    yield document[start:]

def runFunction(f, max_wait, default_value):
    try:
        return func_timeout.func_timeout(max_wait, f)
    except func_timeout.FunctionTimedOut:
        pass
    return default_value