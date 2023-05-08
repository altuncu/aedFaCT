from pybliometrics.scopus import AbstractRetrieval
from util.util import *
import model.researcher as r

class Publication:
    def __init__(self, scopus_eid, search_keywords):
        self.scopus_eid = scopus_eid
        self.pub = AbstractRetrieval(scopus_eid)
        
        if not self.__is_valid__():
            raise Exception("Invalid publication")

        self.title = self.pub.title
        self.abstract = self.__get_abstract__()
        self.highlighted_abstract = self.__highlight_keywords__(self.abstract, search_keywords)
        self.author_keywords = self.pub.authkeywords
        self.authors = self.pub.authors
        self.auth_profiles = [r.Researcher(a.auid) for a in self.authors]
        self.authors_str = ", ".join([str(a.full_name) + " (" + str(a.affiliation) + ")" for a in self.auth_profiles])
        self.venue = self.__get_venue__()
        if self.pub.coverDate:
            self.year = self.pub.coverDate[:4]
        else:
            self.year = "Unknown"
        if self.pub.doi:
            self.doi_link = "https:\\doi.org/" + self.pub.doi
        else:
            self.doi_link = self.pub.scopus_link
        self.bib_entry = self.pub.get_html()

    def __is_valid__(self):
        if self.pub is None or None in [self.pub.title, self.pub.authors, self.__get_abstract__()]:
            return False
        else:
            return True

    def __get_abstract__(self):
        if self.pub.abstract:
            return self.pub.abstract.replace("©", "")
        elif self.pub.description:
            return self.pub.description.replace("©", "")
        else:
            return None

    def __get_venue__(self):
        if self.pub.confname:
            return self.pub.confname
        elif self.pub.publicationName:
            return self.pub.publicationName
        else:
            return "Unknown"

    def __highlight_keywords__(self, text, keywords):
        for word in keywords:
            text = re.sub(word, "<b>" + word + "</b>", text, flags=re.IGNORECASE)
        return text