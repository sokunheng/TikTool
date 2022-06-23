import requests
import os
from threading import Thread

from ._helpers import download, getHeaders


class User:

    def __init__(self, username):
        self.username = username
        # make the request call only once and save the response data
        self.data = requests.get(
            f"https://www.tiktok.com/api/user/detail/?device_id=7098862702289995269&uniqueId={self.username}", headers=getHeaders()).json()

    def downloadAllVideos(self, watermark=True):
        # check if user is a private account or does not exist in one go
        try:
            if self.data["userInfo"]["user"]["privateAccount"] == True:
                print("[!] Account is Private! Skipping...")
                return
        except KeyError:
            print("[!] User Does Not Exist! Skipping...")
            return

        # get the user secUid which is unique for every user
        sec_uid = self.data["userInfo"]["user"]["secUid"]

        # get the list of all the user published videos
        data = requests.get(
            f"https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/post/?sec_user_id={sec_uid}&count=33&device_id=9999999999999999999&max_cursor=0&aid=1180", headers=getHeaders()).json()
        videos = data["aweme_list"]

        # create the directories for the specific user
        if not os.path.exists(f"downloads/users/{self.username}"):
            os.makedirs(f"downloads/users/{self.username}")
        if not os.path.exists(f"downloads/users/{self.username}/wm"):
            os.makedirs(f"downloads/users/{self.username}/wm")
        if not os.path.exists(f"downloads/users/{self.username}/no-wm"):
            os.makedirs(f"downloads/users/{self.username}/no-wm")

        # download each video
        count = 0
        for video in videos:
            count += 1

            # get the video download link
            if watermark == True:
                download_url = video["video"]["download_addr"]["url_list"][0]
            else:
                download_url = video["video"]["play_addr"]["url_list"][0]

            uri = video["video"]["download_addr"]["uri"]

            # check if video is already downloaded
            if os.path.exists(f"downloads/users/{self.username}/{'wm' if watermark == True else 'no-wm'}/{uri}.mp4"):
                continue

            # download and save the video
            download_path = f"downloads/users/{self.username}/{'wm' if watermark == True else 'no-wm'}/{uri}.mp4"
            # using threads so we don't have to wait for each video to complete
            download_thread = Thread(target=download, args=(
                download_url, download_path,))
            download_thread.start()

    def downloadProfilePicture(self):
        # check if image is already downloaded
        if os.path.exists(f"downloads/users/{self.username}/{self.username}-profile.jpeg"):
            print("[!] Image Already Downloaded! Skipping...")
            return

        # get the image download link
        try:
            download_url = self.data["userInfo"]["user"]["avatarLarger"]
        except KeyError:
            print("[!] User Does Not Exist! Skipping...")
            return

        # create the directories for the specific user
        if not os.path.exists(f"downloads/users/{self.username}"):
            os.makedirs(f"downloads/users/{self.username}")

        # download and save the image
        download_path = f"downloads/users/{self.username}/{self.username}-profile.jpeg"
        download(download_url, download_path)
