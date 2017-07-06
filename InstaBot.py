import requests,urllib
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN = '1946858049.0a70fa9.f8593965a37a472e9d9ed564dc32b7a5'
BASE_URL = 'https://api.instagram.com/v1/'


'''
c=[]
d=[]
e=[]
'''

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


def get_own_post():
  request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  own_media = requests.get(request_url).json()
  if own_media['meta']['code'] == 200:
    if len(own_media['data']):
      image_name = own_media['data'][0]['id'] + '.jpeg'
      image_url = own_media['data'][0]['images']['standard_resolution']['url']
      urllib.urlretrieve(image_url, image_name)
      print 'Your image has been downloaded!'
    else:
      print 'Post does not exist!'
  else:
    print 'Status code other than 200 received!'
  return None


def get_user_post(insta_username):
  user_id = get_user_id(insta_username)
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_media = requests.get(request_url).json()
  if user_media['meta']['code'] == 200:
    if len(user_media['data']):
      image_name = user_media['data'][0]['id'] + '.jpeg'
      image_url = user_media['data'][0]['images']['standard_resolution']['url']
      urllib.urlretrieve(image_url, image_name)
      print 'Your image has been downloaded!'
    else:
      print "There is no recent post!"
  else:
    print "Status code other than 200 received!"
  return None



def get_post_id(insta_username):
  user_id = get_user_id(insta_username)
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_media = requests.get(request_url).json()

  if user_media['meta']['code'] == 200:
    if len(user_media['data']):
      return user_media['data'][0]['id']
    else:
      print 'There is no recent post of the user!'
      exit()
  else:
    print 'Status code other than 200 received!'
    exit()



def like_a_post(insta_username):
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + 'media/%s/likes') % (media_id)
  payload = {"access_token": APP_ACCESS_TOKEN}
  print 'POST request url : %s' % (request_url)
  post_a_like = requests.post(request_url, payload).json()
  if post_a_like['meta']['code'] == 200:
    print 'Like was successful!'
  else:
    print 'Your like was unsuccessful. Try again!'


def get_like_list(insta_username):
  mid = get_post_id(insta_username)
  request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (mid, APP_ACCESS_TOKEN)
  likes_lst = requests.get(request_url).json()
  print likes_lst



def post_a_comment(insta_username):
  media_id = get_post_id(insta_username)
  comment_text = raw_input("Your comment: ")
  payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
  request_url = (BASE_URL + 'media/%s/comments') % (media_id)
  print 'POST request url : %s' % (request_url)

  make_comment = requests.post(request_url, payload).json()

  if make_comment['meta']['code'] == 200:
    print "Successfully added a new comment!"
  else:
    print "Unable to add comment. Try again!"

def get_comment_list(insta_username):
  media_id = get_post_id(insta_username)
  request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
  comment_list = requests.get(request_url).json()

  if comment_list['meta']['code'] == 200:
    if len(comment_list['data']):
      for i in range(0, len(comment_list['data'])):
        print comment_list['data'][i]['text']
    else:
      print 'There is no recent post of the user!'
      exit()
  else:
    print 'Status code other than 200 received!'
    exit()


def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

'''
def tag_name():
  name = raw_input('enter the HashTag you want to search')
  request_url = (BASE_URL + 'tags/search?q=%s&access_token=%s') % (name, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  tag_list = requests.get(request_url).json()
  if tag_list['meta']['code'] == 200:
    if len(tag_list['data']):
      for i in range(0, len(tag_list['data'])):
        a = tag_list['data'][i]['media_count']
        b = tag_list['data'][i]['name']
        c.append(a)
        d.append(b)
      print c
      print d
      labels =
      sizes = [15, 30, 45, 10]
      explode = (0, 0.1, 0, 0)

      fig1, ax1 = plt.subplots()
      ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
              shadow=True, startangle=90)
      ax1.axis('equal')
      plt.show()
    else:
      print 'There is no recent post of the user!'
      exit()
  else:
    print 'Status code other than 200 received!'
    exit()

'''


def start_bot():
  while True:
    print '\n'
    print 'Hey! Welcome to instaBot!'
    print 'Here are your menu options:'
    print '1.Get your own details\n'
    print '2.Get details of a user by username\n'
    print '3.Get your own recent post\n'
    print '4.Get user post\n'
    print '5.Like a user post\n'
    print '6.Get like list\n'
    print '7.Post comment on users post\n'
    print '8.Get list comment on recent post\n'
    print '9.Delete negative comment\n'
    print '10.Get count of HashTag\n'
    print '11.Exit'

    choice = raw_input('Enter you choice: ')
    if choice == '1':
      self_info()
    elif choice == '2':
      insta_username = raw_input('Enter the username of the user: ')
      get_user_info(insta_username)
    elif choice == '3':
      get_own_post()
    elif choice == '4':
      insta_username = raw_input('Enter the username of the user: ')
      get_user_post(insta_username)
    elif choice == '5':
      insta_username = raw_input('Enter the username of the user')
      like_a_post(insta_username)
    elif choice == '6':
      insta_username = raw_input('Enter username')
      get_like_list(insta_username)
    elif choice == '7':
      insta_username = raw_input('Enter the username of the user')
      post_a_comment(insta_username)
    elif choice == '8':
      insta_username = raw_input('Enter the username of the user')
      get_comment_list(insta_username)
    elif choice == '9':
      insta_username = raw_input('Enter the username of the user')
      delete_negative_comment(insta_username)
    elif choice == '10':
      tag_name()
    elif choice == '11':
      exit()
    else:
      print 'wrong choice'


start_bot()
