from spudoolicom import app
from flask import render_template


@app.route('/')
def main():
    return render_template('index.html')