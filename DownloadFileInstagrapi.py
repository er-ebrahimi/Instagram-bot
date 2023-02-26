from instagrapi import Client
import os
cl = Client()
USERNAME = input('enter user name: ')
PASSWORD = input('enter password: ')
your_dest = input('enter the user name of that channel you want to download: ')
cl.login(USERNAME, PASSWORD)

print('login is done')
path = 'C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp'

# code = cl.media_pk_from_url("https://www.instagram.com/p/CopL5apAytK/")
# code = int(code)
# print(f'code is initilized: {code}')

# video_type = cl.media_info(code).url

user_id = cl.user_id_from_username(your_dest)

print(f"user id catched {user_id}")

media_list = cl.user_medias(user_id,1)

print(f'media list catched its size is {len(media_list)}')

for media in media_list:
    print(f'media.pk is {media.pk}')
    if media.media_type == 1 :
        cl.photo_download(media.pk, folder=path)
        print("photo downloaded")
    elif media.media_type == 2 and media.product_type == 'feed':
        cl.video_download(media.pk, folder=path)
        print("video downloaded")
    elif media.media_type == 2 and media.product_type == 'igtv':
        cl.igtv_download(media.pk, folder=path)
        print("igtv downloaded")
    elif media.media_type == 2 and media.product_type == 'clips':
        cl.clip_download(media.pk, folder=path)
        print("clip downloaded")
    elif media.media_type == 8 :
        cl.album_download(media.pk, folder=path)
        print("album downloaded")
    else:
        print("couldn't find the type of media")
    

def findMedia(name: str, medias):
    for i in range(len(medias)):
        if name in medias[i].pk:
            return i


for data in os.listdir(path):
    print(f'media.pk is {media.pk}')
    index = 0
    # index = findMedia(data,media_list)
    # if type(index) == type(0):
    upload_path = os.path.join(path,data)
    if media.media_type == 1 :
        cl.photo_upload(path=upload_path,caption= media_list[index].caption_text)
        print("photo uploaded")
    elif media.media_type == 2 and media.product_type == 'feed':
        cl.video_upload(path=upload_path,caption= media_list[index].caption_text)
        print("video uploaded")
    elif media.media_type == 2 and media.product_type == 'igtv':
        cl.igtv_upload( path=upload_path,caption= media_list[index].caption_text)
        print("igtv uploaded")
    elif media.media_type == 2 and media.product_type == 'clips':
        cl.clip_upload( path=upload_path,caption= media_list[index].caption_text)
        print("clip uploaded")
    elif media.media_type == 8 :
        cl.album_upload( path=upload_path,caption= media_list[index].caption_text)
        print("album uploaded")
    else:
        print("couldn't find the type of media")
    # else:
    #     print(f'type of index wasnt int {index}')

print('finished')
