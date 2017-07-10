#This is for importing the requests and urllib files.
import requests,urllib
#This is for importing textblob library.
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
#This is for importing the plotting library.
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np


#Here is my Access token which is genenrate from my Instagram Account.
APP_ACCESS_TOKEN = '1946858049.0a70fa9.f8593965a37a472e9d9ed564dc32b7a5'

#Here is the base url.
BASE_URL = 'https://api.instagram.com/v1/'


#For the Insta_username you can use the Instabot.mriu.test.1 and uditk14



#This function is for fetching personal information like username, fullname, followers, followed by, no. of posts.
def self_info():

    #This request_url is using for requesting the url of the user.
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)

  print 'GET request url : %s' % (request_url)
    #This is using for storing the information which is come from the request_url and convert that information in proper
    #form  by using json function.

  user_info = requests.get(request_url).json()

    #Here we are checking user info that it comes with the status ok which is code 200.
  if user_info['meta']['code']==200:

    if len(user_info['data']):
    #Here we are printing the personal information.

      print 'Your UserName is:- %s' %(user_info['data']['username'])
      print 'Your Full_Name is:- %s' %(user_info['data']['full_name'])
      print 'You have %d Followers' %(user_info['data']['counts']['follows'])
      print 'No. of people you are following %d' %(user_info['data']['counts']['followed_by'])
      print 'You have %d posts' %(user_info['data']['counts']['media'])
    else:
      print 'The user does not exist'
  else:
      #Here we are printing some line if we get some other meta code other than 200.
    print 'The User have different Meta code other than 200'


#This function is use for getting the user id by usiing the user_name.
def get_user_id(insta_username):

    #In this we are requesting the url of getting the user_id by user_name.
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


#This function is for fetching the user info by taking the username of that username.
def get_user_info(insta_username):

    #Here we are calling the user_id function to get the user_id from the username.
  user_id= get_user_id(insta_username)

    #checking parameter which check the user_id isn't empty or not.
  if user_id==None:
    print 'User is not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_info = requests.get(request_url).json()
    #printing the user_info parameter
  print user_info

    #checking the meta code for getting the information.
  if user_info['meta']['code'] == 200:

    if len(user_info['data']):

        #Here we are printing the user_info like his/her username, No of followers, No of posts etc.
      print 'Username: %s' % (user_info['data']['username'])
      print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
      print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
      print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
      print 'There is no data for this user!'
  else:
    print 'Status code other than 200 received!'


#This function is using for getting our own recent post on Instagram.
def get_own_post():

    #Here is the api for getting the recent post of own.
  request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)

  print 'GET request url : %s' % (request_url)
  own_media = requests.get(request_url).json()
  if own_media['meta']['code'] == 200:
    if len(own_media['data']):

        #This is use for storing the image of .jpeg format in variable image_name.
      image_name = own_media['data'][0]['id'] + '.jpeg'
      image_url = own_media['data'][0]['images']['standard_resolution']['url']
      urllib.urlretrieve(image_url, image_name)
      print 'Your image has been downloaded!'
    else:
      print 'Post does not exist!'
  else:
    print 'Status code other than 200 received!'
  return None


#This function is for getting the recent post of any user by giving the username.
def get_user_post(insta_username):

    #Here we are fetching the user_id of the user by its username.
  user_id = get_user_id(insta_username)

    #checking for the user_id, if its empty then print that user doesn't exist.
  if user_id == None:
    print 'User does not exist!'
    exit()

    #Here is the Api of getting the  recent post of the user by its username.
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
      print 'There is no recent post!'
  else:
    print 'Status code other than 200 received!'
  return None



#This function is using for getting the post id from the user_id of the username.
def get_post_id(insta_username):

    #Here we are calling the user_id functon to getting the user_id of the user by which we can get the post_id
    #of the recent post made by the user.
  user_id = get_user_id(insta_username)
  if user_id == None:
    print 'User does not exist!'
    exit()
  request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
  print 'GET request url : %s' % (request_url)
  user_media = requests.get(request_url).json()

  if user_media['meta']['code'] == 200:
    if len(user_media['data']):

        #return the id of the recent media post by the user.
      return user_media['data'][0]['id']
    else:
      print 'There is no recent post of the user!'
      exit()
  else:
    print 'Status code other than 200 received!'
    exit()



#This function is for like a post of any user which is in your sandbox.
def like_a_post(insta_username):

    #Here we are calling the post_id function to get the id of the recent post.
  media_id = get_post_id(insta_username)

  request_url = (BASE_URL + 'media/%s/likes') % (media_id)

    #In this, we are using payload for accessing the token.
  payload = {"access_token": APP_ACCESS_TOKEN}

  print 'POST request url : %s' % (request_url)
  post_a_like = requests.post(request_url, payload).json()
  if post_a_like['meta']['code'] == 200:

      #This is for priting that you like the post successful.
    print 'Like was successful!'
  else:

      #This is for unsuccessful like post.
    print 'Your like was unsuccessful. Try again!'


#get_like_list functi
#  on is using for getting the list of people who like your  post by giving the username of the user.
def get_like_list(insta_username):

  mid = get_post_id(insta_username)

  #Here is the Api to get the list of people who like the post.
  request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (mid, APP_ACCESS_TOKEN)
  likes_lst = requests.get(request_url).json()

  if likes_lst['meta']['code'] == 200:
    if len(likes_lst['data']):
        for i in range(0,len(likes_lst['data'])):
            #This is for getting the list of people who like your post with their username, fullname and user_id.
            print 'username is:- %s'  %(likes_lst['data'][i]['username'])
            print 'Full Name is:- %s' %(likes_lst['data'][i]['full_name'])
            print 'User Id is :- %s' %(likes_lst['data'][i]['id'])
    else:
      print 'There is no recent post of the user!'
      exit()
  else:
    print 'Status code other than 200 received!'
    exit()


#This function is used for post a comment on the recent post of a username by its username.
def post_a_comment(insta_username):

    #This is for getting the user media_id on which you want to make a comment.
  media_id = get_post_id(insta_username)

  #Here we are asking for the comment that he/she wants to make on the user post.
  comment_text = raw_input('Your comment: ')

  payload = {'access_token': APP_ACCESS_TOKEN, 'text': comment_text}
  request_url = (BASE_URL + 'media/%s/comments') % (media_id)
  print 'POST request url : %s' % (request_url)

  make_comment = requests.post(request_url, payload).json()

  if make_comment['meta']['code'] == 200:

      #This is for printing that you have successfully commented on the post.
    print 'Successfully added a new comment!'
  else:
    print 'Unable to add comment. Try again!'


#This function is using for fetching the list of comment on a particular post.
def get_comment_list(insta_username):

  media_id = get_post_id(insta_username)

  #Here is the Api for comment session.
  request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
  comment_list = requests.get(request_url).json()

  if comment_list['meta']['code'] == 200:
    if len(comment_list['data']):

        #This for loop print all the comment which are on the post of the user.
      for i in range(0, len(comment_list['data'])):
        print comment_list['data'][i]['text']
    else:
      print 'There is no recent post of the user!'
      exit()
  else:
    print 'Status code other than 200 received!'
    exit()

#This function is use for deleting all the negative comment which are made on the particular post f any user.
def delete_negative_comment(insta_username):

    media_id = get_post_id(insta_username)

    #Here is the Api for requesting the url of the particular media by media_id function.
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            #This for loop is using to make the comment_id and comment_text.
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']

                #Here is textblob who Analyse the natureof the comment.
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




#There are three array which are use in tag_name function for storing the hashtag, name and the media count.
name=[]
a=[]
b=[]




#tag_name function is use for getting the Analyzer on a trending theme.
def tag_name():

    #This for loop is using for getting the popular hashtag out of four. if you want to make greater than you change range from 4 to any other.
    for i in range(4):

        #Here we are taking the hashtag from the user .
        names = raw_input('enter the HashTag you want to search ')

        #This is for append all the hashtag with other.
        name.append(names)

        #This is the Api for getting the media count.
        request_url = (BASE_URL + 'tags/%s?access_token=%s') % (names , APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        tag_list = requests.get(request_url).json()
        if tag_list['meta']['code'] == 200:
            if len(tag_list['data']):
                a= tag_list['data']['media_count']
                b.append(a)

                #This is for printing the media count which is in b and printing the name in name variable.
                print b
                print name
            else:
                print 'There is no recent post of the user!'
                exit()
        else:
            print 'Status code other than 200 received!'
            exit()
    x = np.arange(4)


    #This function is use for plotting a graph of all the trending theme.
    def plot(x, pos):
        return '%100.0f' % (x * 1e-1)

    formatter = FuncFormatter(plot)

    #This all are the features of the graph like what to print on the x-axis and on y-axis.
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(formatter)
    plt.bar(x, b)
    plt.xticks(x, name)
    plt.show()


#This function is for showing the grapgh on the screen.
plt.show()



#This is the main function from where our bot is start.
def start_bot():

  while True:

      #Here is the menu from where we select our choice.
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
    print '10.Fetch Trending Theme with the help of HashTag\n'
    print '11.Exit'



    #This is for  entering the choice and the function will act according to it.
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



#Here is the pick up line of our project.
start_bot()
