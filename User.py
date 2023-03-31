from instagrapi import Client
"""
resourceUserNamesDic is a dictionary that contains the user name as key and Media
"""
class User:
    def __init__(self, username, password, resourceUsernameList):
        self.username = username
        self.password = password
        self.resourceUsernameList = resourceUsernameList
        self._resourceInfoDic = {}
        self.client = Client()
    def login(self):
        self.client.login(self.username, self.password)
    def get_resourceInfoDic(self):
        for resourceUserName in self.resourceUsernameList:
            if resourceUserName not in self._resourceInfoDic:
                self._resourceInfoDic[resourceUserName] = self.client.user_info_by_username(resourceUserName)
                print("resourceInfoDic updated")