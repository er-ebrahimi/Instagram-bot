# %%
from instagrapi import Client
import schedule
import os
import schedule
import time
import pickle
from User import User

# %% [markdown]
# 1.At first read from file in user file <br> 
# 2.Then start login in all the accounts <br>
# 3.Then get info of all the resources <br>
# 4.Decrease one from all the user for uploading one media later

# %%
users = []
user_in_file = []
def read_file(path: str):
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            line[-1] = line[-1].strip("\n")
            index = line[0].index(':')
            username = User(line[0][0:index],line[0][index+1:],line[1:])
            print(username.username , username.password , username.resourceUsernameList)
            users.append(username)

    print(users[0].username , users[0].password , users[0].resourceUsernameList)
    print(len(users))
        


# %%
def login():
    for user in users:
        user.login()
        print(f"login is done for {user.username}")

# %%
def resourceInfoDic():
    """_summary_: get information for each resource in resourceUsernameList
    """
    for user in users:
        try:
            user.get_resourceInfoDic()
            print(f"resourceInfoDic is done for {user.username}")
        except Exception as e:
            print(e , user.username)
            continue

# %%
def media_count():
    """decrease one media count for each user
    """
    for user in users:
        for info in user._resourceInfoDic:
            user._resourceInfoDic[info].media_count = user._resourceInfoDic[info].media_count - 1
            print(f"media count is done for {user.username}")
            print(user._resourceInfoDic[info].media_count) 

# %%
def write_file(all_users):
    for user in all_users:
        with open(f"./resources/{user.username}.pickle", "wb") as file:
            pickle.dump(user, file)
            print(f"write_file is done for {user.username}")

# %%
def remove_posts(user):
    posts = user.client.user_medias(user.client.user_id, 7)
    for post in posts:
        print(f"post {post.pk} is going to be deleted")
        user.client.media_delete(post.pk)
        print(f"post {post.pk} deleted")

# %%
def removeResource(username: str, user_in_file: list):
    """delete one of the resources from the resource list of the user

    Args:
        username (str): username of that resource
    """
    for user in user_in_file:
        print(user)
        for resource in user.resourceUsernameList:
            print(resource)
            if resource == username:
                user.resourceUsernameList.remove(resource)
                print(f"resource {username} is removed from {user.username}")
                user.get_resourceInfoDic()
                break

# %% [markdown]
# Read pickle file

# %%
def read_pickle(resources: str="resources"):
    """_summary_: read pickle files and return a list of users

    Returns:
        resources: name of file that contains all the users
    """
    print("in resources files:")
    for file in os.listdir("resources"):
        resource_path = os.path.join("resources", file)
        with open(resource_path, "rb") as file:
            users_new = pickle.load(file)
            print(file)
            user_in_file.append(users_new[-1])
            print(f"adding {users_new[-1].username} to user_in_file")
    return user_in_file

# %%
if __name__ == "__main__":
    while True:
        print("0. read file then login then get info then decrease media count then write file")
        print("1. remove resource")
        print("2. remove posts")
        print("3. rewrite file")
        print("4. print info")
        print("5. exit")
        option = input("Enter the option: ")
        if option == "0":
            file = input("Enter the file name: ")
            read_file(f"./users/{file}.txt")
            login()
            resourceInfoDic()
            media_count()
            write_file(users)
        elif option == "1":
            username = input("Enter the username: ")
            user_in_file = read_pickle()
            removeResource(username, user_in_file)
        elif option == "2":
            username = input("Enter the username: ")
            for user in users:
                if user.username == username:
                    remove_posts(user)
        elif option == "3`":
            ask = input("Do you want to Enter the file name: ")
            if ask == "yes":
                file = input("Enter the file name: ")
                read_file(f"./users/{file}.txt")
            else:
                read_pickle()
            write_file(user_in_file)
        elif option == "4":
            for user in user_in_file:
                print(user.username)
                for info in user._resourceInfoDic:
                    print(info)
                    print(user._resourceInfoDic[info].media_count)
        elif option == "5":
            break


