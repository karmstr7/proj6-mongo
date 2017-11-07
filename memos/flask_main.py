"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.
Representation conventions for dates:
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will
   - User input/output is in local (to the server) time.
"""

import flask
from flask import g
from flask import request
from flask import url_for

import uuid
import ast
import logging

import sys

# Date handling
import arrow
# Mongo database
from pymongo import MongoClient

import config
CONFIG = config.configuration()


MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
    CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST,
    CONFIG.DB_PORT,
    CONFIG.DB)


print("Using URL '{}'".format(MONGO_CLIENT_URL))


###
# Globals
###

app = flask.Flask(__name__)
app.secret_key = CONFIG.SECRET_KEY

####
# Database connection per server process
###

try:
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, CONFIG.DB)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

TEXT_MAX_LENGTH = 250


###
# Pages
###
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    g.memos = get_memos()
    for memo in g.memos:
        app.logger.debug("Memo: " + str(memo))
    return flask.render_template('index.html')


@app.route("/create")
def create():
    app.logger.debug("Create")
    text = flask.request.args.get('text')
    date = flask.request.args.get('date')
    if len(text) > TEXT_MAX_LENGTH:
        rslt = 'error'
    else:
        app.logger.debug("text: {} date: {}".format(text, date))
        collection.insert_one({'type': 'dated_memo', 'date': date, 'text': text, 'token': make_token()})
        rslt = 'OK'
    return flask.jsonify(result=rslt)


@app.route("/remove")
def remove():
    """
    Delete a list of memos.
    :return: JSON
    """
    app.logger.debug("Remove")
    tokens = flask.request.args.get('tokens')
    tokens = ast.literal_eval(tokens)
    for token in tokens:
        if collection.find({'token': token}):
            collection.delete_one({'token': token})
    return flask.jsonify(result='OK')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################


@app.template_filter('humanize')
def humanize_arrow_date(date):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case.
    """
    try:
        then = arrow.get(date).to('local')
        now = arrow.utcnow().to('local')
        if then.date() == now.date():
            human = "Today"
        else:
            human = then.humanize(now)
            if human == "in a day":
                human = "Tomorrow"
    except:
        human = date
    return human


#############
#
# Functions available to the page code above
#
##############
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = []
    for record in collection.find({"type": "dated_memo"}):
        record['date'] = arrow.get(record['date']).isoformat()
        del record['_id']
        records.append(record)
    return sort_memos(records)


def sort_memos(memos):
    """
    Bubble sort the memos into chronological order.
    :param memos: list
    :return: list/string
    """
    try:
        for i in range(len(memos)-1):
            for j in range(i+1, len(memos)):
                if memos[j]['date'] < memos[i]['date']:
                    temp = memos[i]
                    memos[i] = memos[j]
                    memos[j] = temp
    except:
        return 'Error'
    return memos


def make_token():
    """
    Create a (pseudo)random string UUID object using UUID.
    :return: An UUID object that's been converted to type string.
    """
    token = str(uuid.uuid4())
    return token


app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
app.run(port=CONFIG.PORT, host="0.0.0.0")
