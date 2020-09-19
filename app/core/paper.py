
import json
from json import JSONEncoder

class GenericEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o,Author):
            return {"name": o.__str__()}
        if isinstance(o, Paper):
            if o.author is not None:
                return {"title": o.__str__(), "doi" : o.doi, "author": f'{", ".join([a.__str__() for a in o.author])}'}
            else:
                return {"title": o.__str__(), "doi" : o.doi, "author": "Not Available"}
        if isinstance(o, Reference):
            return {"key": o.key, "title": o.title, "doi": o.doi}

class GraphEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Paper):
            return o.doi
        if isinstance(o, Reference):
            return o.key

class Paper:
    """This class represents the basic papers.
    """    
    # papers will at least have title or not
    def __init__(self,title,url,doi,citation_count,references_count, author, subtitle, reference):
        """
        Parameters
        ----------
        title : str
            title of the paper
        url : str
            URL form of the paper's DOI
        doi : str
            DOI of the paper 
        citation_count : int
            no of citations with Crossref
        references_count : int
            no of references cited in Crossref
        author : list
            list of `Author`, may be None
        subtitle : list
            list of papers subtitles (str), may be None
        reference : list
            list of `Reference`, may be None
        """
        self._title = title
        self._url = url
        self._doi = doi
        self._citation_count = citation_count
        self._references_count = references_count
        self._author = author
        self._references = reference
        self._subtitle = subtitle

    def has_references(self):
        return self._references != None

    @property
    def doi(self):
        return self._doi

    @property
    def references(self):
        return self._references

    @property
    def author(self):
        return self._author
    
    @property
    def title(self):
        return ", ".join(self._title)

    def __str__(self):
        if self._subtitle is not None:
            return f'{self._title} {self._subtitle}'
        else: 
            return f'{self._title}'
    
    def __repr__(self):
        return f'Title: {self._title}\nSub-Title: {self._subtitle}'

    # def __eq__(self, other):
    #     return self.doi == other.doi

class Reference:
    """This class represents a reference.
    """
    def __init__(self, key, title, doi):
        self._key = key
        self._title = title
        self._doi = doi

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        self._key = new_key
    
    @property
    def title(self):
        return self._title

    @property
    def doi(self):
        return self._doi
    
    @doi.setter
    def doi(self, new_doi):
        self._doi = new_doi

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return f'{self._title}'

    def __repr__(self):
        return f'{self._title}'

    # def __eq__(self, other):
    #     return self.doi == other.doi

class Author:
    """This class represents the author of a paper.
    """

    def __init__(self, family, given, affiliation):
        """
        Parameters
        ---------
        family : str
            family name of author
        given : str
            given name of author, may be None
        affiliation : list
            list of `Affiliation`, may be None
        """
        self._family = family
        self._given = given
        self._affiliation = affiliation

    @property
    def name(self):
        """Return the name of the author.
        Returns
        -------
        str 
            name from family and given
        """
        if self._given is None:
            return f'{self._family}'
        return f'{self._given} {self._family}'

    def __str__(self):
        if self._affiliation and self._given is not None:
            return f'{self._family}, {self._given}, {self._affiliation[0]}'
        elif self._given is not None:
            return f'{self._family}, {self._given}'
        else:
            return f'{self._family}'

    def __repr__(self):
        if self._affiliation and self._given is not None:
            return f'{self._family}, {self._given}, {self._affiliation[0]}'
        elif self._given is not None:
            return f'{self._family}, {self._given}'
        else:
            return f'{self._family}'

class Affiliation:
    """This class represents the affiliation of the author.
    """

    def __init__(self, name):
        """
        Parameters
        ----------
        name : list
            list of str which are affiliations
        """
        self._name = name
    
    @property
    def names(self):
        """Return the name of the affiliation.
        """
        return self._name

    def __str__(self):
        return f'{self._name}'
    
    def __repr__(self):
        return f'{self._name}'


