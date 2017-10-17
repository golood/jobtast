from flask import render_template
from app import app, analis
import json
#import anal

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # выдуманный пользователь
    posts = [ # список выдуманных постов
        { 
            'author': { 'nickname': 'John' }, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': { 'nickname': 'Susan' }, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]

    table = analis.getTable()
    
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts,
        table = table)

@app.route('/index/json')
def get_json():
    data = {}
    table = analis.getTable()

    for key in table.keys():
        if (table[key]['count'] + table[key]['arrive']) < table[key]['mustbe']:
            data.setdefault(key)
            data[key] = {}
            data[key].setdefault("count")
            data[key]['count'] = table[key]['mustbe'] - (table[key]['count'] + table[key]['arrive'])
    
    return render_template("json.html",
        title = 'Home',
        data = json.dumps(data))
