# %%
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
os.mkdir(new_folder_path)
print("New folder created at:", new_folder_path)
path = new_folder_path


# %% [markdown]
# Read users and acounts

# %%
user_in_file = []
for file in os.listdir("resources"):
    with open("resources/" + file, "rb") as file:
        users_new = pickle.load(file)
        # print(users_new)
        # for user in users_new:
        #     print(f'{user.username} {user.password} {user.client.media}')
        #     if user not in user_in_file:
        #         user_in_file.append(users_new)
        #         logging.info(f'adding {user.username} to user_in_file')
        #         # print(f"adding {user.username} to user_in_file")
        print(file)
        user_in_file.append(users_new[-1])
        logging.info(f'adding {users_new[-1].username} to user_in_file')
        print(f"adding {users_new[-1].username} to user_in_file")

# %%
user_in_file

# %%
def remove_file(input_path: list):
    """remove file from path it usually used to remove uploaded file from tmp folder

    Args:
        path (str): path of file
    """
    removed = False
    if type(input_path) != list:
        path = [input_path]
    else:
        path = input_path.copy()
    for p in path:
        for i in range(3):
            try:
                if os.access(p, os.W_OK):
                    print(f"removing file {p}")
                    logging.info(f"removing file {p}")
                    os.remove(p)
                    print('file removed')
                    logging.info('file removed')
                    break
                else:
                    print(f"{p} is engaiging with another process")
                    logging.info(f"{p} is engaiging with another process")
                    time.sleep(1)
            except OSError as e:
                    print(e)
                    logging.error(e)
                    print(f"retrying to remove file {path} after {i} times")
                    logging.error(f"retrying to remove file {path} after {i} times")
                    time.sleep(1)
                    continue

# %%
def remove_all():
    """if you want to remove all file from tmp folder use this function
    """
    try:
        for i in os.listdir(path):
            os.remove(path + '\\' + i)
            print(f"removed {i}")
    except Exception as e:
        print(e)

# %%
def change_comment(comment:str,user:User, resUsername:Client):
    if '@' in comment:
        comment = comment.replace(resUsername.username, user.username)
        print(f"comment changed")
        logging.info(f"comment changed")
    else:
        print(f"comment not changed")
        logging.info(f"comment not changed")
    return comment


# %%
def upload_post(posts: dict, path: str, cl, medias: list,new_info, remove_uploaded: bool = True):
    """upload downloaded posts to instagram

    Args:
        posts (dict): it is dictionary which key is media pk and value is path of media
        path (str): path of tmp folder
        cl (Client): our client object
        media_list (list): list of media
        new_info (_type_): new information of resourses
        remove_uploaded (bool, optional): if you want to to upload and delete it from your directory. Defaults to True.
    """
    print("upload func------------------------------------------------------------")
    tested_media = []#this var use in exception handling and remove the media that is cause of exception
    if not os.path.exists(path):
        print(f'Exception occuerd: current directory doesnt exist')
        logging.error(f'Exception occuerd: current directory doesnt exist')
        current_dir = os.getcwd()
        print("Current Directory:", current_dir)
        # Create a new folder
        new_folder_name = "tmp"
        new_folder_path = os.path.join(current_dir, new_folder_name)
        os.mkdir(new_folder_path)
        print("New folder created at:", new_folder_path)
        path = new_folder_path
    print(f"medias in upload func is {[med.pk for med in medias]}")
    for media in  medias:
        tested_media = media
        try:
            if media.media_type == 1 :
                print(f"photo uploading in path {posts[media.pk]}")
                logging.info(f"photo uploading in path {posts[media.pk]}")
                cl.photo_upload(path=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("photo uploaded")
                logging.info("photo uploaded")

            elif media.media_type == 2 and media.product_type == 'feed':
                print(f"media uploading in path {posts[media.pk]}")
                logging.info(f"media uploading in path {posts[media.pk]}")
                cl.video_upload(path=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("video uploaded")               
                logging.info("video uploaded")               

            elif media.media_type == 2 and media.product_type == 'igtv':
                print(f"igtv uploading in path {posts[media.pk]}")
                logging.info(f"igtv uploading in path {posts[media.pk]}")
                cl.igtv_upload( path=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("igtv uploaded")
                logging.info("igtv uploaded")

            elif media.media_type == 2 and media.product_type == 'clips':
                print(f"clip uploading in path {posts[media.pk]}")
                logging.info(f"clip uploading in path {posts[media.pk]}")
                cl.clip_upload( path=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("clip uploaded")
                logging.info("clip uploaded")

            elif media.media_type == 8 :
                cl.album_upload( paths=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("album uploaded")
                logging.info("album uploaded")

            else:
                print("couldn't find the type of media")
                logging.info("couldn't find the type of media")
            if remove_uploaded:
                remove_file(posts[media.pk])
                print('file removed')
                logging.info('file removed')
        except KeyError as e:
            print(e)
            print(f"media {media.pk} is not in {posts}")
            logging.error(f"media {media.pk} is not in {posts}")
    print("upload func finished------------------------------------------------------------")
    #TODO every time you get key error delete last media and decrease index by 1        
    
    


# %%
def download_post(cl:Client, new_info, path, amount ,media_list = []):
    tested_media = []

    posts = {}
    if media_list == []:
        media_list = cl.user_medias(new_info.pk ,amount)
    len_media = len(media_list)
    print(f'media list catched its size is {len(media_list)}')
    logging.info(f'media list catched its size is {len(media_list)}')
    if not os.path.exists(path):
        print(f'Exception occuerd: current directory doesnt exist')
        logging.error(f'Exception occuerd: current directory doesnt exist')
        current_dir = os.getcwd()
        print("Current Directory:", current_dir)
        # Create a new folder
        new_folder_name = "tmp"
        new_folder_path = os.path.join(current_dir, new_folder_name)
        os.mkdir(new_folder_path)
        print("New folder created at:", new_folder_path)
        path = new_folder_path
    for media in media_list:
        tested_media = media
        downloaded = True
        print(f'media.pk is {media.pk}')
        logging.info(f'media.pk is {media.pk}')
        if media.media_type == 1 :
            posts[media.pk]=cl.photo_download(media.pk, folder=path)
            print("photo downloaded")
            logging.info("photo downloaded")
        elif media.media_type == 2 and media.product_type == 'feed':
            posts[media.pk]=cl.video_download(media.pk, folder=path)
            print("video downloaded")
            logging.info("video downloaded")
        elif media.media_type == 2 and media.product_type == 'igtv':
            posts[media.pk]=cl.igtv_download(media.pk, folder=path)
            print("igtv downloaded")
            logging.info("igtv downloaded")
        elif media.media_type == 2 and media.product_type == 'clips':
            posts[media.pk]=cl.clip_download(media.pk, folder=path)
            print("clip downloaded")
            logging.info("clip downloaded")
        elif media.media_type == 8 :
            posts[media.pk]=cl.album_download(media.pk, folder=path)
            print("album downloaded")
            logging.info("album downloaded")
        else:
            print("couldn't find the type of media")
            logging.info("couldn't find the type of media")
            downloaded = False
        len_media -=1
        print(f"one media finished and {len_media} is left")
        logging.info(f"one media finished and {len_media} is left")
        if downloaded:
            #upload just one video and delete that video from directory
            upload_post(posts, path, cl, [media],new_info)
    print('finished')
    media_list.clear()
    print('media list cleared')
    logging.info('media list cleared')
    posts.clear()
    print('posts cleared')
    logging.info('posts cleared')
    
    

# %%
def rewrite(users_new):
    for user in users_new:
        with open(f"resources\{user.username}.pickle", "wb") as file:
            print(f"rewriting {user.username}.pickle")
            logging.info(f"rewriting {user.username}.pickle")
            pickle.dump(users_new, file)
            print(f"{user.username}.pickle rewritten")
            logging.info(f"{user.username}.pickle rewritten")
            file.close()

# %%
def run():
    for user in user_in_file:
        for resource in user._resourceInfoDic:
            new_info = user.client.user_info_by_username(resource)
            if new_info.media_count  != user._resourceInfoDic[resource].media_count:
                print(f"{resource} has new media")
                logging.info(f"{resource} has new media")
                posts = new_info.media_count - user._resourceInfoDic[resource].media_count 
                download_post(user.client, new_info, path, 3 if posts  > 3 else posts)
                user._resourceInfoDic[resource] = new_info
                print(f"{resource} updated")
                logging.info(f"{resource} updated")
            else:
                print(f"{resource} has no new media")
                logging.info(f"{resource} has no new media")
                print(f"amount of media is {new_info.media_count}")
                logging.info(f"amount of media is {new_info.media_count}")
    rewrite(user_in_file)
    print('remove all files')
    remove_all()

# %%
run()
schedule.every().day.at("01:30").do(run)
# Run the scheduled functions
logging.info("start the scheduler")
while True:
    schedule.run_pending()
    time.sleep(1)

# %%
print(len(user_in_file))
for user in user_in_file:
    user.username
    for resource in user._resourceInfoDic:
        print(resource)

# %%
remove_all()

# %%
rewrite(user_in_file)

# %%
def remove_posts(user):
    posts = user.client.user_medias(user.client.user_id, 7)
    for post in posts:
        print(f"post {post.pk} is going to be deleted")
        user.client.media_delete(post.pk)
        print(f"post {post.pk} deleted")
print(user_in_file[1].username)
# remove_posts(user_in_file[1])


