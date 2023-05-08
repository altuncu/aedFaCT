from pybliometrics.scopus import AuthorRetrieval
import requests

class Researcher:
    def __init__(self, scopus_auid):
        self.auid = scopus_auid
        self.profile = AuthorRetrieval(scopus_auid)
        self.full_name = self.profile.given_name + " " + self.profile.surname
        self.cleaned_name = " ".join([w for w in self.full_name.split() if "." not in w])
        self.affiliation = self.__get_affiliation__()
        self.orcid = self.profile.orcid
        self.scopus_link = self.profile.self_link
        self.other_links = self.__get_other_links__()
        self.related_pubs = []

    def __get_affiliation__(self):
        if self.profile.affiliation_current[0]:
            if self.profile.affiliation_current[0].parent_preferred_name:
                return self.profile.affiliation_current[0].preferred_name + ", " + \
                       self.profile.affiliation_current[0].parent_preferred_name
            else:
                return self.profile.affiliation_current[0].preferred_name
        else:
            return None

    def __get_other_links__(self):
        if self.orcid:
            try:
                headers = {'Accept': 'application/json'}
                request_url = "https://pub.orcid.org/v3.0/" + self.orcid + "/researcher-urls"
                url = requests.get(request_url, headers=headers).json()['researcher-url']
                if url:
                    return [u['url']['value'] for u in url]
                else:
                    return []
            except:
                return []
        else:
            return []

    def append_related_pubs(self, pub):
        self.related_pubs.append(pub)

def sort_researchers(researchers):
    return sorted(researchers, key=lambda x: (len(x.related_pubs), len(x.other_links)), reverse=True)