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


def get_user_id(insta_username):
  request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()

  if user_info['meta']['code']==200:
    if len(user_info['data']):
      return user_info['data'][0]['id']
    else:
      return None
  else:
    print 'Status code other than 200 received!'
    exit()


def get_user_info(insta_username):

  user_id= get_user_id(insta_username)
  if user_id==None:
    print 'User is not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()
  print user_info

  if user_info['meta']['code'] == 200:
    if len(user_info['data']):
      print 'Username: %s' % (user_info['data']['username'])
      print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
      print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
      print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
      print 'There is no data for this user!'
  else:
    print 'Status code other than 200 received!'


def start_bot():
  while True:
    print '\n'
    print 'Hey! Welcome to instaBot!'
    print 'Here are your menu options:'
    print '1.Get your own details\n'
    print '2.Get details of a user by username\n'
    print '3.Exit'

    choice = raw_input("Enter you choice: ")
    if choice == '1':
      self_info()
    elif choice == '2':
      insta_username = raw_input("Enter the username of the user: ")
      get_user_info(insta_username)
    elif choice == '3':
      exit()
    else:
      print "wrong choice"

start_bot()
