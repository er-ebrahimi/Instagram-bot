from instagrapi import Client
import schedule
import os
import schedule
import time
cl = Client()
USERNAME = input('enter user name: ')
PASSWORD = input('enter password: ')
your_dest = input('enter the user name of that channel you want to download: ')
cl.login(USERNAME, PASSWORD)

print('login is done')
path = 'C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\Instagram-bot\\tmp'


user_id = cl.user_id_from_username(your_dest)

print(f"user id catched {user_id}")

def download_post():
    try:
        media_list = cl.user_medias(user_id,3)
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
            
        for data in os.listdir(path):
            print(f'media.pk is {media.pk}')
            index = 0
            # index = findMedia(data,media_list)
            upload_path = os.path.join(path,data)
            if type(index) != False:
                if media.media_type == 1 :
                    print(f"photo uploading in path {upload_path}")
                    cl.photo_upload(path=upload_path,caption= media_list[index].caption_text)
                    print("photo uploaded")
                elif media.media_type == 2 and media.product_type == 'feed':
                    print(f"media uploading in path {upload_path}")
                    cl.video_upload(path=upload_path,caption= media_list[index].caption_text)
                    print("video uploaded")
                elif media.media_type == 2 and media.product_type == 'igtv':
                    print(f"igtv uploading in path {upload_path}")
                    cl.igtv_upload( path=upload_path,caption= media_list[index].caption_text)
                    print("igtv uploaded")
                elif media.media_type == 2 and media.product_type == 'clips':
                    print(f"clip uploading in path {upload_path}")
                    cl.clip_upload( path=upload_path,caption= media_list[index].caption_text)
                    print("clip uploaded")
                elif media.media_type == 8 :
                    print(f"album uploading in path {upload_path}")
                    cl.album_upload( paths=upload_path,caption= media_list[index].caption_text)
                    print("album uploaded")
                else:
                    print("couldn't find the type of media")
            else:
                print(f'type of index wasnt int {index}')

        print('finished')
    except Exception as e:
        print(f'Exception occuerd: {e}')
        ques = input('Do you want to start downloading again:(Y/N) ')
        if ques == 'Y' or ques == 'y':
            download_post()
        elif ques == 'N' or ques == 'n':
            exit()



# download_post()
schedule.every().day.at("01:30").do(download_post)
# Run the scheduled functions
while True:
    schedule.run_pending()
    time.sleep(1)
