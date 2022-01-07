from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
import math

es = Elasticsearch()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    page_size = 10
    keyword = request.args.get('keyword')

    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    body = {
        'size': page_size,
        'from': page_size * (page_no-1),
        'query': {
            'multi_match': {
                "query": keyword,
                "type": "cross_fields",
                "fields": [],
                "slop": 2,
                "operator": "or"                
            }
        }
    }

    res = es.search(index='game_character', doc_type='', body=body)
    hits = [{'game_char_id': doc['_source']['id'], 
            'char_name': doc['_source']['name'], 
            'game_name': doc['_source']['game'], 
            'char_gender': doc['_source']['gender'], 
            'description': doc['_source']['description']} 
            for doc in res['hits']['hits']]
    page_total = math.ceil(res['hits']['total']['value']/page_size)
    return render_template('search.html', keyword=keyword, hits=hits, page_no=page_no, page_total=page_total)