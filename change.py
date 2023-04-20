from instagrapi import Client
import schedule
import os
import schedule
import time
import pickle
from User import User
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG)
path = 'C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp'
current_dir = os.getcwd()
print("Current Directory:", current_dir)
# Create a new folder
new_folder_name = "tmp"
new_folder_path = os.path.join(current_dir, new_folder_name)
if not os.path.exists(current_dir + "/" + new_folder_name):
    os.mkdir(new_folder_path)
print("New folder created at:", new_folder_path)
path = new_folder_path

user_in_file = []
print("in resources files:")
for i,file in enumerate(os.listdir("resources")):
    all_resources = os.path.join("resources", file)
    with open(all_resources, "rb") as file:
        users_new = pickle.load(file)
        print(users_new)
        #for user in users_new:
        #    print(user.username, end=" ")
        user_in_file.append(users_new)
        #logging.info(f'adding {users_new[-1].username} to user_in_file')
        #print(f"adding {users_new[-1].username} to user_in_file")

def rewrite(users_new):
    for user in users_new:
        with open(f"all_resources/{user.username}.pickle", "wb") as file:
            print(f"rewriting {user.username}.pickle")
            logging.info(f"rewriting {user.username}.pickle")
            pickle.dump(user, file)
            print(f"{user.username}.pickle rewritten")
            logging.info(f"{user.username}.pickle rewritten")
            file.close()
for i in user_in_file:
    print(i)
    print(i)
    #i.resourceUsernameList[-1] = i.resourceUsernameList[-1].strip("\n")
    #print(i.resourceUsernameList)

#print("start writing")
#rewrite(user_in_file)
#print("finished")