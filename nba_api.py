import tweepy
from time import sleep
from textwrap import TextWrapper
import redis

class StreamNBAListener(tweepy.StreamListener):
	"""
	A custom class that manipulates Twitter stream.
	"""
	
	status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
	# r = redis.Redis(host = 'localhost', port = 6379, db = 0)
	
	def on_status(self, status):
		"""
		Define listener's behavior when a new status is streamed to me.
		
		Commented out code for storing to Redis DB--will worry about that
		later. Maybe a future project.
		"""
		
		name = status.author.screen_name
		t = status.created_at
		source = status.source
		text = status.text
		
		# Some statuses do not have coordinates. Deal with them. 
		if status.coordinates:
			coords = status.coordinates['coordinates']
		else:
			coords = '.'

		try:
			print self.status_wrapper.fill(text)
			print '\n %s  %s  via %s\n' % (name, t, source)
			print status.coordinates['coordinates']
		except:
			# Catch any unicode errors while printing to console
			# and just ignore them to avoid breaking application.
			pass
				
		# Messing with Redis.
		# if r.exists(status.created_at):
		# 	key = str(status.created_at) + "-1"
		# else:
		# 	key = str(status.created_at)
		# self.r.rpush(key, status.author.screen_name)
		# if coords:
		# 	self.r.rpush(key, status.coordinates['coordinates'])			
		# else:
		# 	self.r.rpush(key, '.')
		# self.r.rpush(key, status.text.encode('utf-8'))
		
		# Outfiling data in CSV format.
		outfile = open('./game1.txt', 'a')
		outfile.write('%s, %s, %s, %s\n' %
		                  (t, name.encode('utf-8'), coords, text.encode('utf-8')))
		outfile.close()
	
	def on_error(self, status_code):
		print "Error! Status code: %s" % status_code
		return True

	def on_timeout(self):
		outfile.close()
		print "Nap time! ZZZZZZZZZzzzzzz"

def start_api(auth_dict):
    """
    Start and authenticate Twitter API instance. Create a global out
    of the returned API.
    """

    auth = tweepy.OAuthHandler(auth_dict['C_KEY'], auth_dict['C_SECRET'])
    auth.set_access_token(auth_dict['A_KEY'], auth_dict['A_SECRET'])
    api = tweepy.API(auth)

    return api, auth

def open_stream(api, auth):
    """
    Opens Twitter stream for data access.
    """

    # Twitter streaming requires user to use OAuth. Tweepy has a listener
    # that handles Twitter stream. I think this is how it must be instantiated.
    listen = StreamNBAListener(api)
    stream = tweepy.Stream(auth, listen)

    return stream

def tweets_by_location(stream, coords, boxSize = 1):
    """
    Return tweets in user-defined locations. Start with Dallas and
    Miami for this project.

    Twitter's statuses/filter method returns a stream of statuses
    with user-specified filters. tweets_by_location() should be 
    used to sample statuses in a given area.

    coord = list of coordinates provided as tuples
    boxSize = size of box around city. 
    """

    # Read the doc string above: I should NOT filter on player names
    # here. Use this method to develop a sample of tweets in a location.
    # Twitter API takes long/lat pairs.
    #
    # From http://www.infoplease.com/ipa/A0001796.html:
    # Dallas: center = -96.46, 32.46 
    # Miami: center = -80.12, 25.46
	# USA: bounding box: -179.15, 18.91, -66.94, 71.44

    boxes = ""

    for x in coords:
        c1 = (x[0] - boxSize / 2, x[1] - boxSize / 2)
        c2 = (x[0] + boxSize / 2, x[1] + boxSize / 2)
        box = (c1, c2)
        for y in box:
            boxes += str(y)

    # What does a Tweepy stream return? Play around with this at home.
    stream = open_stream(api)
    stream.filter(locations = boxes)
    sleep(1)
