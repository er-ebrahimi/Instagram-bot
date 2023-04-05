# %%
from instagrapi import Client
import schedule
import os
import schedule
import time
import pickle
import import_ipynb
from User import User

# %%
file = input("Enter the file name: ")
users = []
def read_file(path: str):
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            index = line[0].index(':')
            username = User(line[0][0:index],line[0][index+1:],line[1:])
            print(username.username , username.password , username.resourceUsernameList)
            users.append(username)

        
read_file(f"./users/{file}.txt")
print(users[0].username , users[0].password , users[0].resourceUsernameList)
print(len(users))

# %%
for user in users:
    user.login()
    print(f"login is done for {user.username}")

# %%
for user in users:
    try:
        user.get_resourceInfoDic()
        print(f"resourceInfoDic is done for {user.username}")
    except Exception as e:
        print(e , user.username)
        continue

# %%
test = Client()
for user in users:
    for info in user._resourceInfoDic:
        user._resourceInfoDic[info].media_count = user._resourceInfoDic[info].media_count - 1
        print(f"media count is done for {user.username}")
        print(user._resourceInfoDic[info].media_count) 

# %%
print(users[0]._resourceInfoDic)

# %%
for user in users:
    with open(f"resources\{user.username}.pickle", "wb") as file:
        pickle.dump(users, file)

# %%
def remove_posts(user):
    posts = user.client.user_medias(user.client.user_id, 7)
    for post in posts:
        print(f"post {post.pk} is going to be deleted")
        user.client.media_delete(post.pk)
        print(f"post {post.pk} deleted")
print(users[0].username)
# remove_posts(users[0])


