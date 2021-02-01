from Bio import Entrez

pubmed_mail = "your.email@example.com"

def search_query(query, retmax):
    Entrez.email = pubmed_mail
    handle = Entrez.esearch(db='pmc',
                            sort='relevant',
                            retstart = 0,
                            retmax=retmax,
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)

    return results['IdList']


def fetch_details(id_list):
    ids = id_list
    Entrez.email = pubmed_mail
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)['PubmedArticle']
    return results
