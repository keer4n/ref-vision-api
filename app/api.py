import requests
import json
from flask import Flask, jsonify, request

from core.finder import QueryService
from core.crossrefparser import CrossRefRestParser
from core.grapher import Grapher
from core.paper import GenericEncoder, GraphEncoder

# app =  Flask(__name__, static_folder="../build", static_url_path='/')

app = Flask(__name__)

finder = QueryService()
parser = CrossRefRestParser()

@app.route("/api/s")
def search():    #TODO: probably should sanitize ?
    """ generic query string search
    search for a query returning result list which can be further used
    to select specific papers with doi to create graph
    
    Parameters
    ----------
    queryString : str
        search query provided by the user
    
    Returns
    -------
    json
        response json
    """
    resp = finder.fetch_by_query(request.args.get("query"))
    print(resp)
    papers = parser.parse_response(resp)
    return json.dumps(papers, cls=GenericEncoder)
    

@app.route("/api/q/doi/<doi>")
def query_doi(doi):
    """ specific request using doi
    the doi is queried directly
    
    Parameters
    ----------
    doi : str
        specially formatted doi string

    Returns
    -------
    json
        response json containing the work referenced by doi
    """
    return finder.fetch_by_doi(doi)



# @app.route("/")
# def index():
#     return app.send_static_file("index.html")

@app.route("/api/g")
def draw_graph():
    
    # ret = QueryService().fetch_by_doi("10.1145/3133956.3134093")
    ret = QueryService().fetch_by_doi(request.args.get("doi"))
    paper = CrossRefRestParser().parse_response(ret)
    g = Grapher(paper)
    g.create()
    from networkx.readwrite import json_graph
    
    d = json_graph.node_link_data(g.graph)  # node-link format to serialize
    return json.dumps(d,cls=GraphEncoder,indent=4)
    # write json
    # return json.dump(d, open("force/force.json", "w"), cls=GenericEncoder)
    # return app.send_static_file("force.html")

# if __name__ == "__main__":
#     app.run()