from spudoolicom import app, db, forms, config
from flask import render_template, request, flash
from datetime import datetime
import typesense


client = typesense.Client({
  'nodes': [{
    'host': 'localhost', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',      # For Typesense Cloud use 443
    'protocol': 'http'   # For Typesense Cloud use https
  }],
  'api_key': config.api_key,
  'connection_timeout_seconds': 2
})


@app.route('/search/')
def search():
    if request.method == "GET":
        args = request.args
        searchquery = args.get('q')

        searchresults = client.collections['spudooli-website'].documents.search({'q': searchquery, 'query_by': 'headline, body', 'include_fields': 'id, headline, body', 'limit': 10})
        
        return render_template('search.html', searchresults = searchresults, searchquery = searchquery)