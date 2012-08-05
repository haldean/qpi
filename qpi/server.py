import flask
import media
import os
import queue

_app = flask.Flask('qpi')
_upload_dir = None

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

@_app.route('/delete/<int:media_id>')
def _delete(media_id):
  queue.remove(media_id)
  return flask.redirect(flask.url_for('_main'))

@_app.route('/upload', methods=['POST'])
def _upload():
  if not _upload_dir:
    raise ValueError('Uploads are disabled.')

  uploaded_file = flask.request.files['file']
  media.add_for_upload(uploaded_file, _upload_dir)
  return flask.redirect(flask.url_for('_main'))

@_app.route('/stream/<int:media_id>')
def _stream(media_id):
  return flask.send_file(media.file_for_media_id(media_id, _upload_dir))

def run_server(port, upload_dir='/tmp/qpi_uploads/'):
  global _upload_dir
  _upload_dir = upload_dir
  if not os.path.exists(_upload_dir):
    os.makedirs(_upload_dir)
  _app.run(debug=True, port=port)

if __name__ == '__main__':
  run_server()
