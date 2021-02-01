import pandas as pd
from utils.date import to_datetime
from functools import wraps
nb_author = 16

class DataFrameGenertion:
    def __init__(self):
        self.columns = self._generate_columns()
        self.df = pd.DataFrame(columns=self.columns)
        self.d = None
        self.article = None

    def _generate_columns(self):
        columns = ["pmid", "title", "abstract", "date", "journal", "substance", "author_list", "affiliation_list"]

        for i in range(0, nb_author):
            columns.append(f'author_{i}')
            columns.append(f'affiliation_{i}')
        return columns

    def try_data(func):
        """
        decorator to add before every function that get information from article :
        """
        @wraps(func)
        def inner(self):
            try:
                return func(self)
            except:
                return None

        return inner

    def normalize_data(func):
        @wraps(func)
        def inner(self, dic_key):
            data_l = func(self)
            if data_l != None:
                name = dic_key.strip('list')
                for i in range(len(data_l)):
                    self.d[f'{name}{i}'] = self.d[dic_key][i]
                    if i > nb_author:
                        break
            return data_l
        return inner

    @try_data
    def get_abstract(self):
        return self.article["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]

    @try_data
    @normalize_data
    def get_affiliation_list(self):
        return [ele['Affiliation'] for ele in self.article["MedlineCitation"]['Article']['AuthorList'][0]['AffiliationInfo']]

    @try_data
    @normalize_data
    def get_author_list(self):
        return [ele['ForeName'] + " " + ele['LastName'] for ele in
                self.article["MedlineCitation"]['Article']['AuthorList']]

    @try_data
    def get_chemical_list(self):
        return ', '.join([str(ele['NameOfSubstance']) for ele in self.article["MedlineCitation"]["ChemicalList"]])

    def update_df(self, article):
        self.d = {}
        self.article = article
        self.d['abstract'] = self.get_abstract()
        self.d['pmid'] = str(article["MedlineCitation"]["PMID"])
        self.d['title'] = article["MedlineCitation"]['Article']['ArticleTitle']
        self.d['date'] = to_datetime(article["MedlineCitation"]["DateCompleted"])
        self.d['journal'] = article["MedlineCitation"]["MedlineJournalInfo"]['MedlineTA']
        self.d['author_list'] = self.get_author_list()
        self.d['affiliation_list'] = self.get_affiliation_list()
        self.d['author_list'] = self.get_chemical_list()
        self.df = self.df.append(self.d, ignore_index=True)
