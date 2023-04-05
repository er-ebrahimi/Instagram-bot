# %%
from instagrapi import Client
import schedule
import os
import schedule
import time
import pickle
import import_ipynb
from User import User
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG)
path = 'C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp'


# %% [markdown]
# Read users and acounts

# %%
user_in_file = []
for file in os.listdir("resources"):
    with open("resources/" + file, "rb") as file:
        users_new = pickle.load(file)
        for user in users_new:
            if user.username not in user_in_file:
                user_in_file.append(users_new[0])
                print(f"adding {user.username} to user_in_file")

# %%
user_in_file

# %%
print(user_in_file[0]._resourceInfoDic)

# %%
def remove_file(path: str):
    """remove file from path it usually used to remove uploaded file from tmp folder

    Args:
        path (str): path of file
    """
    for i in range(3):
        try:
            if type(path) == list:
                for p in path:
                    print(f"removing file {p}")
                    os.remove(p)
                    print('file removed')
            else:
                print(f"removing file {path}")
                os.remove(path)
                print('file removed')
            break
        except Exception as e:
            print(e)
            print(f"retrying to remove file {path} after {i} times")
            time.sleep(2)
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
    print(f"changing comment {comment} for {user.username} from {resUsername.username}")
    if '@' in comment:
        comment = comment.replace(resUsername.username, user.username)
        print(f"comment changed to {comment}")
    else:
        print(f"comment not changed")
    return comment


# %%
def upload_post(posts: dict, path: str, cl, media_list: list,new_info, remove_uploaded: bool = True):
    tested_media = []#this var use in exception handling and remove the media that is cause of exception
    try:
        for i,media in enumerate( media_list):
            if media.media_type == 1 :
                print(f"photo uploading in path {posts[media.pk]}")
                cl.photo_upload(path=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("photo uploaded")

            elif media.media_type == 2 and media.product_type == 'feed':
                print(f"media uploading in path {posts[media.pk]}")
                cl.video_upload(path=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("video uploaded")               

            elif media.media_type == 2 and media.product_type == 'igtv':
                print(f"igtv uploading in path {posts[media.pk]}")
                cl.igtv_upload( path=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("igtv uploaded")

            elif media.media_type == 2 and media.product_type == 'clips':
                print(f"clip uploading in path {posts[media.pk]}")
                cl.clip_upload( path=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("clip uploaded")

            elif media.media_type == 8 :
                cl.album_upload( paths=posts[media.pk],caption= change_comment(media.caption_text,cl,new_info))
                print("album uploaded")

            else:
                print("couldn't find the type of media")
            if remove_uploaded:
                remove_file(posts[media.pk])
                print('file removed')
                posts.pop(media.pk)
                print('post removed')
                media_list.pop(i)
                print('media removed')
    except Exception as e:
        print(f'Exception occuerd: {e}')
        ques = input('Do you want to start uploading again:(Y/N) ')
        if ques == 'Y' or ques == 'y':
            media_list.remove(tested_media)
            upload_post(posts, path, cl, media_list,new_info)
        elif ques == 'N' or ques == 'n':
            pass
    print('finished')
    # print('start removing files')
    # for i in media_list:
    #     remove_file(posts[i.pk])
    # print('files removed')
    media_list.clear()
    print('media list cleared')
    posts.clear()
    print('posts cleared')


# %%
def download_post(cl, new_info, path, amount ,media_list = []):
    tested_media = []
    try:
        posts = {}
        if media_list == []:
            media_list = cl.user_medias(new_info.pk ,amount)
        len_media = len(media_list)
        print(f'media list catched its size is {len(media_list)}')
        for media in media_list:
            tested_media = media
            downloaded = True
            print(f'media.pk is {media.pk}')
            if media.media_type == 1 :
                posts[media.pk]=cl.photo_download(media.pk, folder=path)
                print("photo downloaded")
                upload_post(posts, path, cl, media_list,new_info)
            elif media.media_type == 2 and media.product_type == 'feed':
                posts[media.pk]=cl.video_download(media.pk, folder=path)
                print("video downloaded")
            elif media.media_type == 2 and media.product_type == 'igtv':
                posts[media.pk]=cl.igtv_download(media.pk, folder=path)
                print("igtv downloaded")
            elif media.media_type == 2 and media.product_type == 'clips':
                posts[media.pk]=cl.clip_download(media.pk, folder=path)
                print("clip downloaded")
            elif media.media_type == 8 :
                posts[media.pk]=cl.album_download(media.pk, folder=path)
                print("album downloaded")
            else:
                print("couldn't find the type of media")
                downloaded = False
            len_media -=1
            print(f"one media finished and {len_media} is left")
            if downloaded:
                upload_post(posts, path, cl, media_list,new_info)
    except Exception as e:
        print(f'Exception occuerd: {e}')
        ques = input('Do you want to download again or start uploading:(Y/N) ')
        if ques == 'Y' or ques == 'y':
            media_list.remove(tested_media)
            download_post(cl, new_info.pk, path,amount, media_list)
        elif ques == 'N' or ques == 'n':
            pass
    

# %%
def rewrite(users_new):
    for user in users_new:
        with open(f"resources\{user.username}.pickle", "wb") as file:
            print(f"rewriting {user.username}.pickle")
            pickle.dump(users_new, file)
            print(f"{user.username}.pickle rewritten")
            file.close()

# %%
def run():
    for user in user_in_file:
        for resource in user._resourceInfoDic:
            new_info = user.client.user_info_by_username(resource)
            if new_info.media_count  != user._resourceInfoDic[resource].media_count:
                print(f"{resource} has new media")
                download_post(user.client, new_info, path, new_info.media_count - user._resourceInfoDic[resource].media_count)
                user._resourceInfoDic[resource] = new_info
                print(f"{resource} updated")
            else:
                print(f"{resource} has no new media")
                print(f"amount of media is {new_info.media_count}")
    rewrite(user_in_file)
    remove_all()

# %%
run()
schedule.every().day.at("01:30").do(run)
# Run the scheduled functions
while True:
    schedule.run_pending()
    time.sleep(1)

# %%
comment = "hello @the_fitness.body how are you @the_fitness.body"
if '@' in comment:
    comment = comment.replace('the_fitness.body', "body")
print(comment)

# %%
remove_all()

# %%
rewrite(user_in_file)


