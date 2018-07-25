from flask import Flask, jsonify, request, send_file, make_response
from datetime import datetime
from log import log

from engine import Engine
from spacy import displacy

from io import StringIO

app = Flask(__name__)

# isDev = True
isDev = False

engine = Engine(isDev)

@app.route('/')
def hello_world():
  return 'Welcome to smart cloud shell! Please help with testing/labeling at https://bizqnabootcamp.azurewebsites.net/'

@app.route('/cli/<string:query>')
def cliWithCmd(query):
  result = engine.getLegacyResult(query)
  return jsonify(result)

@app.route('/cli/help/<string:query>')
def cliWithHelp(query):
  result = engine.getLegacyResult(query)
  return jsonify(result)

@app.route('/q/<string:query>')
def getResponse(query):
  search = request.args.get('search')
  enableSearch = bool(search)

  custom = request.args.get('custom')
  enableCustomResponse = (custom)

  result = engine.getResponse(
    query,
    enableSearch = enableSearch,
    enableCustomResponse = enableCustomResponse)

  return jsonify(result)

@app.route('/diag')
def getDiag():
  return jsonify({
    "modelid": engine.cliModel.id
  })

@app.route('/nlp/qr/<string:query>')
def nlp_qr(query):
  rewrittenQuery = engine.cliModel.rewriteUserQuery(query)
  newQuery = rewrittenQuery["query"]
  return jsonify({
    "origin": query,
    "new": newQuery,
    "identical": (query == newQuery),
    "corrections": rewrittenQuery["corrections"]
  })

@app.route('/nlp/tokens/<string:query>')
def nlp_tokens(query):
  doc = engine.cliModel._nlp(query)

  tokens = [(token.text, token.dep_, token.head.text, token.head.pos_).__str__() for token in doc]

  return jsonify(tokens)

@app.route('/nlp/svg/<string:query>')
def nlp_svg(query):
  doc = engine.cliModel._nlp(query)
  svg = displacy.render(doc, style='dep')

  response = make_response(svg)
  response.content_type = 'image/svg+xml'
  return response

port = 80

if isDev:
  port = 5000

print("localhost:%d is serving" % port)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)
