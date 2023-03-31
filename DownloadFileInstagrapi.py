from instagrapi import Client
import schedule
import os
import schedule
import time

class MyClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_media_id = None

    def user_medias(self, user_id, amount=12, last_media_id=None):
        """
        Get user medias
        :param user_id: User ID
        :param amount: Amount of medias to get
        :param last_media_id: Last media ID
        :return: List of Media
        """
        if last_media_id is None:
            last_media_id = self.last_media_id
        medias = self.user_medias_v1(user_id, amount, last_media_id)
        if medias:
            self.last_media_id = medias[-1].pk
        return medias

cl = Client()
USERNAME = input('enter user name: ')
PASSWORD = input('enter password: ')
your_dest = input('enter the user name of that channel you want to download: ')
cl.login(USERNAME, PASSWORD)

print('login is done')
path = 'C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp'


user_id = cl.user_id_from_username(your_dest)

print(f"user id catched {user_id}")

user_info = cl.user_info(user_id)

print(f"user info: amount  catched {user_info.media_count}")

def remove_file(path: str):
    if type(path) is list:
        for p in path:
            print(f"removing file {p}")
            os.remove(p)
            print('file removed')
    else:
        print(f"removing file {path}")
        os.remove(path)
        print('file removed')

def download_post():
    try:
        posts = {}
        media_list = cl.user_medias(user_id,2)
        print(f'media list catched its size is {len(media_list)}')
        for media in media_list:
            print(f'media.pk is {media.pk}')
            if media.media_type == 1 :
                posts[media.pk]=cl.photo_download(media.pk, folder=path)
                print("photo downloaded")
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
            
    except Exception as e:
        print(f'Exception occuerd: {e}')
        ques = input('Do you want to download again or start uploading:(Y/N) ')
        if ques == 'Y' or ques == 'y':
            download_post()
        elif ques == 'N' or ques == 'n':
            pass
    while True:
        try:
            for media in media_list:
                if media.media_type == 1 :
                    print(f"photo uploading in path {posts[media.pk]}")
                    cl.photo_upload(path=posts[media.pk],caption= media.caption_text)
                    print("photo uploaded")

                elif media.media_type == 2 and media.product_type == 'feed':
                    print(f"media uploading in path {posts[media.pk]}")
                    cl.video_upload(path=posts[media.pk],caption= media.caption_text)
                    print("video uploaded")               

                elif media.media_type == 2 and media.product_type == 'igtv':
                    print(f"igtv uploading in path {posts[media.pk]}")
                    cl.igtv_upload( path=posts[media.pk],caption= media.caption_text)
                    print("igtv uploaded")

                elif media.media_type == 2 and media.product_type == 'clips':
                    print(f"clip uploading in path {posts[media.pk]}")
                    cl.clip_upload( path=posts[media.pk],caption= media.caption_text)
                    print("clip uploaded")

                elif media.media_type == 8 :
                    print(f"album uploading in path {posts[media.pk]} with this caption {media.caption_text}")
                    cl.album_upload( paths=posts[media.pk],caption= media.caption_text)
                    print("album uploaded")

                else:
                    print("couldn't find the type of media")
        except Exception as e:
            print(f'Exception occuerd: {e}')
            ques = input('Do you want to start uploading again:(Y/N) ')
            if ques == 'Y' or ques == 'y':
                continue
            elif ques == 'N' or ques == 'n':
                break
        print('finished')
        print('start removing files')
        for i in media_list:
            remove_file(posts[i.pk])
        print('files removed')
        media_list.clear()
        print('media list cleared')
        posts.clear()
        print('posts cleared')
        break
        

download_post()
schedule.every().day.at("01:30").do(download_post)
# Run the scheduled functions
while True:
    schedule.run_pending()
    time.sleep(1)
