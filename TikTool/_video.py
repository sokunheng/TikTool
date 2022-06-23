import requests
import os

from ._helpers import download, getHeaders


class Video:

    def __init__(self, link):
        try:
            self.video_id = link.split("/")[5]
        except IndexError:
            raise ValueError("The link provided is not a valid tiktok link")

        if "?" in self.video_id:
            self.video_id = self.video_id[:self.video_id.find("?")]

        # make the request call only once and save the response data
        self.data = data = requests.get(
            f"https://api.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{self.video_id}%5D", headers=getHeaders()).json()

    def downloadVideo(self, watermark=True):
        # check if video is already downloaded
        if os.path.exists(f"downloads/videos/{self.video_id}/{self.video_id}-wm.mp4") and watermark == True:
            print("[!] Video Already Downloaded! Skipping...")
            return
        if os.path.exists(f"downloads/videos/{self.video_id}/{self.video_id}-no-wm.mp4") and watermark == False:
            print("[!] Video Already Downloaded! Skipping...")
            return

        # get the video download link
        try:
            if watermark == True:
                download_url = self.data["aweme_details"][0]["video"]["download_addr"]["url_list"][0]
            else:
                download_url = self.data["aweme_details"][0]["video"]["play_addr"]["url_list"][0]
        except KeyError:
            print("[!] Video Does Not Exist! Skipping...")
            return

        # download and save the video
        if not os.path.exists(f"downloads/videos/{self.video_id}"):
            os.makedirs(f"downloads/videos/{self.video_id}")

        download_path = f"downloads/videos/{self.video_id}/{self.video_id}-{'wm' if watermark == True else 'no-wm'}.mp4"
        download(download_url, download_path)

    def downloadThumbnail(self):
        # check if thumbnail is already downloaded
        if os.path.exists(f"downloads/videos/{self.video_id}/{self.video_id}-thumbnail.jpeg"):
            print("[!] Thumbnail Already Downloaded! Skipping...")
            return

        # get the thumbnail download link
        try:
            download_url = self.data["aweme_details"][0]["video"]["origin_cover"]["url_list"][0]
        except KeyError:
            print("[!] Video Does Not Exist! Skipping...")
            return

        # download and save the thumbnaill
        if not os.path.exists(f"downloads/videos/{self.video_id}"):
            os.makedirs(f"downloads/videos/{self.video_id}")

        download_path = f"downloads/videos/{self.video_id}/{self.video_id}-thumbnail.jpeg"
        download(download_url, download_path)

    def downloadAudio(self):
        # check if audio is already downloaded
        if os.path.exists(f"downloads/videos/{self.video_id}/{self.video_id}-audio.mp3"):
            print("[!] Audio Already Downloaded! Skipping...")
            return

        # get the audio download link
        try:
            download_url = self.data["aweme_details"][0]["music"]["play_url"]["uri"]
        except KeyError:
            print("[!] Video Does Not Exist! Skipping...")
            return

        # download and save the audio
        if not os.path.exists(f"downloads/videos/{self.video_id}"):
            os.makedirs(f"downloads/videos/{self.video_id}")

        download_path = f"downloads/videos/{self.video_id}/{self.video_id}-audio.mp3"
        download(download_url, download_path)

    def downloadAudioCover(self):
        # check if image is already downloaded
        if os.path.exists(f"downloads/videos/{self.video_id}/{self.video_id}-audio-cover.jpeg"):
            print("[!] Audio Already Downloaded! Skipping...")
            return

        # get the image download link
        try:
            download_url = self.data["aweme_details"][0]["music"]["cover_large"]["url_list"][0]
        except KeyError:
            print("[!] Video Does Not Exist! Skipping...")
            return

        # download and save the audio
        if not os.path.exists(f"downloads/videos/{self.video_id}"):
            os.makedirs(f"downloads/videos/{self.video_id}")

        download_path = f"downloads/videos/{self.video_id}/{self.video_id}-audio-cover.jpeg"
        download(download_url, download_path)

    def getDetails(self):
        hashtags = []
        for hashtag in self.data["aweme_details"][0]["text_extra"]:
            hashtags.append(hashtag["hashtag_name"])

        response = {
            "shares": {
                "total": self.data["aweme_details"][0]["statistics"]["share_count"],
                "shares_via_whatsapp": self.data["aweme_details"][0]["statistics"]["whatsapp_share_count"]
            },
            "views_count": self.data["aweme_details"][0]["statistics"]["play_count"],
            "downloads_count": self.data["aweme_details"][0]["statistics"]["download_count"],
            "likes_count": self.data["aweme_details"][0]["statistics"]["digg_count"],
            "comments_count": self.data["aweme_details"][0]["statistics"]["comment_count"],
            "download": {
                "wm": self.data["aweme_details"][0]["video"]["download_addr"]["url_list"],
                "no-wm": self.data["aweme_details"][0]["video"]["play_addr"]["url_list"]
            },
            "music": {
                "name": self.data["aweme_details"][0]["music"]["title"],
                "owner_username": self.data["aweme_details"][0]["music"]["owner_handle"],
                "owner_name": self.data["aweme_details"][0]["music"]["owner_nickname"],
                "download_link": self.data["aweme_details"][0]["music"]["play_url"]["uri"],
                "cover_image": self.data["aweme_details"][0]["music"]["cover_large"]["url_list"][0]
            },
            "hashtags": hashtags
        }

        return response
