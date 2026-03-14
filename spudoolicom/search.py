from spudoolicom import app, db, forms
from flask import render_template, request, flash
import typesense


client = typesense.Client({
  'nodes': [{
    'host': app.config['TYPESENSE_HOST'],
    'port': app.config['TYPESENSE_PORT'],
    'protocol': 'http'
  }],
  'api_key': app.config['TYPESENSE_API_KEY'],
  'connection_timeout_seconds': 2
})


@app.route('/search')
def search():
    if request.method == "GET":
        args = request.args
        searchquery = args.get('q')

        searchresults = client.collections['spudooli-website'].documents.search({'q': searchquery, 'query_by': 'headline, body', 'include_fields': 'id, headline, body', 'limit': 10})
        
        return render_template('search.html', searchresults = searchresults, searchquery = searchquery)