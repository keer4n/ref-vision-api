import requests
from core.crossrefparser import CrossRefRestParser
from core.grapher import Grapher
import warnings 

class APIWarning(Warning):
    pass

class QueryService:
    """ base class for consuming source apis
    """
    
    BASE_URL = "https://api.crossref.org/works"
    def __init__(self, base_url=BASE_URL):
        """ sets the base url and class
        Parameters
        ----------
        base_url : str
            base_url for source apis
        """
        self.base_url = base_url

    
    def _fetch(self, 
               relative_path='', 
               params=None):
        """ generic fetch
        Parameters
        ----------
        relative_path : str
            relative uri
        params : dict
            key-value pair of parameters to specify in get request

        Returns
        -------
        dict 
            response json if successful

        Warns
        -----
        APIWarning
            if API query returns anything other than 200
        """
        query_url = f'{self.base_url}/{relative_path}'
        response = requests.get(query_url, params=params)
        if response.status_code != 200:
            warnings.warn("API query unsuccessful", APIWarning)
        return response.json()

    # TODO: probably url encode doi as recommended in:
    # https://github.com/CrossRef/rest-api-doc#api-overview
    def fetch_by_doi(self, doi):
        """ fetch resource by DOI
        Prameters
        ---------
        doi : str
            standard doi string
        """
        return self._fetch(doi)

    def fetch_by_query(self, query, rows=5):
        """ fetch resource by query string
            The query result defaults to 5 results per page unless
            explicitly specified.
        Parameters
        ----------
        query : str
            query string
        rows : int
            no. of rows to fetch
        """
        params = {"query": query, "rows":rows, "filter":"has-references:true"}
        #params = {"query": query, "rows":rows}
        return self._fetch(params=params)


# ret = QueryService().fetch_by_doi("10.1145/3133956.3134093")
# paper = CrossRefRestParser().parse_response(ret)
# g = Grapher(paper)
# g.create()
# print(g.graph())