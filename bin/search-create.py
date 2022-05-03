import typesense

client = typesense.Client({
  'nodes': [{
    'host': 'localhost', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',      # For Typesense Cloud use 443
    'protocol': 'http'   # For Typesense Cloud use https
  }],
    'api_key':"NfIrs3e3cS8H6hctV0eGsAmFaCQc181QtlAwdMZHIiiMNt6I",
    'connection_timeout_seconds': 2
})

website_schema = {
  'name': 'spudooli-website',
  'fields': [
    {'name': 'id', 'type': 'int32' },
    {'name': 'headline', 'type': 'string' },
    {'name': 'body', 'type': 'string' },
    {'name': 'datetime', 'type': 'int64' },
    {'name': 'url', 'type': 'string', 'index': False, "optional": True }
  ]
}

client.collections.create(website_schema)