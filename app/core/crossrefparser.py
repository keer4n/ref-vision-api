from core.paper import Paper, Reference, Affiliation, Author
import warnings
import logging

logger = logging.getLogger('crossrefparser')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class ParseWarning(Warning):
    pass

# To view if a field is requried (i.e. will be always present) or not consult:
# https://github.com/Crossref/rest-api-doc/blob/master/api_format.md#contributor
class CrossRefRestParser:
    """ response parser for crossref
    parses response to produce Papers and References.

    """
    
    def parse_response(self, api_return):
        mapping_dict = {
            'work': self.parse_work,
            'work-list': self.parse_work_list
        }
        return mapping_dict[api_return['message-type']](api_return['message'])

    def parse_work(self, work):
        logger.debug("Parsing work")
        title = work.get('title')
        url = work.get('URL')
        doi = work.get('DOI')
        citation_count = work.get('is-referenced-by-count')
        references_count = work.get('references-count')

        author = work.get('author', None)
        if author is not None: author = CrossRefRestParser.parse_author(author)

        subtitle = work.get('subtitle', None)
        
        reference = work.get('reference',None)
        if reference is not None: reference = CrossRefRestParser.parse_reference(reference) 
        
        parsed_paper = Paper(title, url, doi, citation_count, references_count, author, subtitle, reference)
        return parsed_paper
    
    def parse_work_list(self, work_list):
        parsed_papers = []
        for item in work_list["items"]:
            parsed_papers.append(self.parse_work(item))
        return parsed_papers


    # TODO: right now assumes either "unstructured" or "article-title" is present, fix thattat
    @staticmethod
    def parse_reference(references):
        parsed_references = []
        for ref in references:
            key = ref.get('key')
            title = ref.get('unstructured', None)
            doi = ref.get('DOI', None)

            #give priority to 'article-title'
            if title is None: title = ref.get('article-title', None) 
            if title is None: title = ref.get('series-title', None) 
            if title is None: title = ref.get('volume-title',None) 
            if title is None: title = ref.get('journal-title', None)

            parsed_reference = Reference(key,title,doi)
            parsed_references.append(parsed_reference)
        return parsed_references

    @staticmethod
    def parse_author(authors):
        """
        Returns
        -------
        list
            list of `Author` for the paper
        """
        parsed_author = []
        for auth in authors:
            given = auth.get('given', None)
            family = auth.get('family')
            affiliation = auth.get('affiliation', None)
            if affiliation is not None: affiliation = CrossRefRestParser.parse_affiliation(affiliation)
            author = Author(family,given,affiliation)
            parsed_author.append(author)
        return parsed_author
        
    @staticmethod
    def parse_affiliation(affiliations):
        """
        Returns
        -------
        list 
            list of `Affiliation` for the author
        """
        parsed_affiliation = []
        for aff in affiliations:
            name = aff.get('name')
            affiliation = Affiliation(name)
            parsed_affiliation.append(affiliation)
        return parsed_affiliation