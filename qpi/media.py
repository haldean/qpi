import gdata.youtube.service as youtube
import re
import queue
import urlparse

ytservice = youtube.YouTubeService()
ytservice.ssl = True

class mediaplugin(object):
  pass

class youtube(mediaplugin):
  template = 'youtube.html'

  @staticmethod
  def matches(parsed_url):
    return re.search(r'[www\.]?youtube.com', parsed_url.hostname)

  def __init__(self, url):
    self.url = url
    self.video_id = urlparse.parse_qs(url.query)['v'][0]
    self.ytdata = ytservice.GetYouTubeVideoEntry(video_id=self.video_id)

  def __str__(self):
    return '%s (YouTube)' % self.ytdata.media.title.text

def add_for_url(url):
  parsed_url = urlparse.urlparse(url)
  for plugin in mediaplugin.__subclasses__():
    if plugin.matches(parsed_url):
      queue.push(plugin(parsed_url))
      return
  raise ValueError('No plugin for URL %s' % url)
