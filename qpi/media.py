import gdata.youtube.service as youtube
import os
import queue
import re
import threading
import urlparse

ytservice = youtube.YouTubeService()
ytservice.ssl = True

def file_for_media_id(media_id, upload_dir):
  return os.path.join(upload_dir, '%d.mp3' % media_id)

class mediaplugin(object):
  _next_id = 0
  _next_id_lock = threading.RLock()

  def __init__(self):
    with mediaplugin._next_id_lock:
      self.media_id = mediaplugin._next_id
      mediaplugin._next_id += 1

class urlplugin(mediaplugin):
  pass

class uploadplugin(mediaplugin):
  def __init__(self, uploaded_file, upload_dir):
    mediaplugin.__init__(self)
    self.path = file_for_media_id(self.media_id, upload_dir)
    uploaded_file.save(self.path)

class youtube(urlplugin):
  template = 'youtube.html'

  @staticmethod
  def matches(parsed_url):
    return re.search(r'[www\.]?youtube.com', parsed_url.hostname)

  def __init__(self, url):
    urlplugin.__init__(self)

    self.url = url
    self.video_id = urlparse.parse_qs(url.query)['v'][0]
    self.ytdata = ytservice.GetYouTubeVideoEntry(video_id=self.video_id)

  def __str__(self):
    return '%s (YouTube)' % self.ytdata.media.title.text.decode('utf-8')

class mp3handler(uploadplugin):
  template = 'audio.html'

  @staticmethod
  def matches(uploaded_file):
    return uploaded_file.filename.endswith('.mp3')

  def __init__(self, uploaded_file, upload_dir):
    uploadplugin.__init__(self, uploaded_file, upload_dir)
    self.filename = uploaded_file.filename

  def __str__(self):
    return '%s (Upload)' % self.filename

def add_for_url(url):
  parsed_url = urlparse.urlparse(url)
  for plugin in urlplugin.__subclasses__():
    if plugin.matches(parsed_url):
      queue.push(plugin(parsed_url))
      return
  raise ValueError('No plugin for URL %s' % url)

def add_for_upload(uploaded, upload_dir):
  for plugin in uploadplugin.__subclasses__():
    if plugin.matches(uploaded):
      queue.push(plugin(uploaded, upload_dir))
      return
  raise ValueError('No plugin for file %s' % uploaded.filename)
