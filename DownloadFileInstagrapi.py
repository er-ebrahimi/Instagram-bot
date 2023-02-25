from instagrapi import Client
cl = Client()
USERNAME = input('enter user name: ')
PASSWORD = input('enter password: ')
your_dest = input('enter the user name of that channel you want to download: ')
cl.login(USERNAME, PASSWORD)

print('login is done')

# code = cl.media_pk_from_url("https://www.instagram.com/p/CopL5apAytK/")
# code = int(code)
# print(f'code is initilized: {code}')

# video_type = cl.media_info(code).url

user_id = cl.user_id_from_username(your_dest)

print(f"user id catched {user_id}")

media_list = cl.user_medias(user_id,3)

print(f'media list catched its size is {len(media_list)}')

for media in media_list:
    print(f'media.pk is {media.pk}')
    if media.media_type == 1 :
        cl.photo_download(media.pk, folder='C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp')
        print("photo downloaded")
    elif media.media_type == 2 and media.product_type == 'feed':
        cl.video_download(media.pk, folder='C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp')
        print("video downloaded")
    elif media.media_type == 2 and media.product_type == 'igtv':
        cl.igtv_download(media.pk, folder='C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp')
        print("igtv downloaded")
    elif media.media_type == 2 and media.product_type == 'clips':
        cl.clip_download(media.pk, folder='C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp')
        print("clip downloaded")
    elif media.media_type == 8 :
        cl.album_download(media.pk, folder='C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp')
        print("album downloaded")
    else:
        print("couldn't find the type of media")







print('finished')