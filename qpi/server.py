import flask
import media
import queue

_app = flask.Flask('qpi')

@_app.route('/client')
def _client():
  item = queue.pop()
  if item:
    return flask.render_template(item.template, item=item)
  return flask.render_template('empty.html')

@_app.route('/')
def _main():
  return flask.render_template('main.html', queue=queue.as_list())

@_app.route('/url', methods=['POST'])
def _url():
  url = flask.request.form['url']
  if url:
    media.add_for_url(url)
  return flask.redirect(flask.url_for('_main'))

def run_server(port):
  _app.run(debug=True, port=port)

if __name__ == '__main__':
  run_server()
