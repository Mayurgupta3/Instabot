import requests

APP_ACCESS_TOKEN = '1946858049.0a70fa9.f8593965a37a472e9d9ed564dc32b7a5'
BASE_URL = 'https://api.instagram.com/v1/'


def self_info():

  request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code']==200:
    if len(user_info['data']):
      print 'Your UserName is:- %s' %(user_info['data']['username'])
      print 'Your Full_Name is:- %s' %(user_info['data']['full_name'])
      print 'You have %d Followers' %(user_info['data']['counts']['follows'])
      print 'No. of people you are following %d' %(user_info['data']['counts']['followed_by'])
      print 'You have %d posts' %(user_info['data']['counts']['media'])
    else:
      print 'The user does not exist'
  else:
    print 'The User have different Meta code other than 200'
self_info()