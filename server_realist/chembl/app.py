
from flask import Flask
import random as ran
import requests as r
import pandas as pd
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

URL = 'https://www.ebi.ac.uk/chembl/api/data/activity/search.json?q={symbol}&limit=50'


@app.route('/<symbol>')
def chembl(symbol):
    data = r.get(URL.format(symbol = symbol)).json()
    try:
        data = pd.DataFrame(data.get('activities'))
        counts = pd.DataFrame(data.standard_type.value_counts()).rename(columns = {'standard_type':'counts'})
        counts.index.name = 'standard_type'
        counts = counts.reset_index()
    except:
        counts = pd.DataFrame(columns = ['standard_type','counts'])
    return counts.to_json(orient = 'records')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
