import config
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

print(client.collections['spudooli-website'].documents.search({
    'q': 'auckland',
    'query_by': 'headline, body',
    'include_fields': 'headline, body, url',
}))


# drop_response = client.collections['news'].delete()
# print(drop_response)