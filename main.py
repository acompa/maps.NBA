from nba_api import *

auth_info = {'C_KEY': 'pHheCvrqLZErbKaGJntkYg',
             'C_SECRET': 'cgH9b02lOLBFN6mJWoKFFmLMPBN0YCzuV6kVimcyZ8',
             'A_KEY': '20386865-e1Q8eG7FLVaWSZo7o5pkjJ4e2KperJCJY2xr2QoXH',
             'A_SECRET': 'vCh0Q6hUo7M8LGocb3KnmniEvmEBTw7LzkPHhJUFcQ'}

api, auth = start_api(auth_info)
stream = open_stream(api, auth)

# r = redis.Redis(host = 'localhost', port = 6379, db = 0)
stream.filter(locations = [-179.15, 18.91, -66.94, 71.44])