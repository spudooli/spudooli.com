from spudoolicom import app
from flask_mysqldb import MySQL

mysql = MySQL()

app.config['MYSQL_HOST'] = '192.168.1.2'
app.config['MYSQL_USER'] = 'sammy'
app.config['MYSQL_PASSWORD'] = 'bobthefish'
app.config['MYSQL_DB'] = 'spudooli'

mysql = MySQL(app)