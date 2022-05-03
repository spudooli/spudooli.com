import typesense
import mysql.connector
import time
import sys

connection = mysql.connector.connect(
    host="192.168.1.2",
    user="sammy",
    password="bobthefish",
    database="spudooli",
)

client = typesense.Client({
  'nodes': [{
    'host': 'localhost', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',      # For Typesense Cloud use 443
    'protocol': 'http'   # For Typesense Cloud use https
  }],
  'api_key': "NfIrs3e3cS8H6hctV0eGsAmFaCQc181QtlAwdMZHIiiMNt6I",
  'connection_timeout_seconds': 2
})


spin = 1
def spinner():
  global spin
  if spin == 1:
    spin = spin + 1
    return "|"
  elif spin == 2:
    spin = spin + 1
    return "/"
  elif spin == 3:
    spin = spin + 1
    return "-"
  elif spin == 4:
    spin = 1
    return "\\"

 
cursor = connection.cursor()
cursor.execute("SELECT id, headline, body, datetime FROM pixelpost_pixelpost")
items = cursor.fetchall()
cursor.close()
for item in items:
    sys.stdout.write(spinner())
    sys.stdout.flush()
    sys.stdout.write('\b')
    datetime = time.mktime(item[3].timetuple())
    datetime = str(datetime).split('.')[0]
    postitem = {'id': str(item[0]), 'headline': item[1], 'body': str(item[2]), 'datetime': int(datetime)}
    print(postitem)
    client.collections['spudooli-website'].documents.upsert(postitem)