from instagrapi import Client
cl = Client()
USERNAME = input('enter user name: ')
PASSWORD = input('enter password: ')
cl.login(USERNAME, PASSWORD)

print('login is done')

code = cl.media_pk_from_url("https://www.instagram.com/p/CopL5apAytK/")
code = int(code)
print(f'code is initilized: {code}')

# video_type = cl.media_info(code).url



video_url = cl.media_info(code).video_url

print(f'video is initilized: {video_url}')

cl.video_download_by_url(video_url, folder='C:\\Users\\Erfun\\OneDrive\\Documents\\Projects\\bot\\tmp')

print('finished')