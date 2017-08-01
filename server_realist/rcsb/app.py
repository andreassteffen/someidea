from flask import Flask
from flask import jsonify
import random as ran
import requests as r
import pandas as pd
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

URL = 'http://mygene.info/v3/query?q=symbol:{symbol}&fields=pdb&species=9606&size=1&entrezonly=1'


@app.route('/<symbol>')
def rcsb(symbol):
    res = r.get(URL.format(symbol = symbol))
    try:
        pdb = res.json().get('hits')[0].get('pdb')[0]
    except:
        pdb = '1aq1'

    return jsonify({'pdb':pdb})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
