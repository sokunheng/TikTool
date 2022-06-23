## Features

- [x] Download videos with watermark
- [x] Download videos without watermark
- [x] Download video thumbnail
- [x] Download video audio
- [x] Download video audio cover
- [x] Get details/info about a video
- [x] Download all videos published by a user with watermark
- [x] Download all videos published by a user without watermark
- [x] Download user profile picture

## Installation

TikTool is still unreleased, but contributions to the project are highly appreciated.
Install the module using the following command to test it out and help us develop the project further.

```bash
pip install "git+https://github.com/simonfarah/TikTool.git#egg=TikTool"
```

## Usage

- ### Video Related Functions

    #### Main setup
    ```python
    from TikTool import Video

    video = Video("https://www.tiktok.com/@tiktok/video/xxxxxxxxxx")

    # !!!!! #
    # video link must be in this format
    ```

    #### Download video with or without watermark
    ```python
    # download video with watermark
    video.downloadVideo(watermark=True)

    # download video without watermark
    video.downloadVideo(watermark=False)

    # if the watermark parameter was not passed,
    # it will be set to True by default
    ```

    #### Download video thumbnail
    ```python
    # download video thumbnail
    video.downloadThumbnail()
    ```

    #### Download audio from video
    ```python
    # download audio from video
    video.downloadAudio()
    ```
    #### Download audio cover from video
    ```python
    # download audio cover from video
    video.downloadAudioCover()
    ```

    #### Get video details/info
    ```python
    # get global details about video
    video.getDetails()
    ```
    - Response structure :
    ```python
    {
        "shares": {
            "total": TOTAL_SHARES,
            "shares_via_whatsapp": TOTAL_SHARES_VIA_WHATSAPP
        },
        "views_count": VIDEO_VIEWS_COUNT,
        "downloads_count": VIDEO_DOWNLOADS_COUNT,
        "likes_count": VIDEO_LIKES_COUNT,
        "comments_count": VIDEO_COMMENTS_COUNT,
        "download": {
            "wm": [LIST OF DOWNLOAD LINKS - WITH WATERMARK],
            "no-wm": [LIST OF DOWNLOAD LINKS - WITHOUT WATERMARK]
        },
        "music": {
            "name": MUSIC_NAME,
            "owner_username": MUSIC_OWNER_USERNAME,
            "owner_name": MUSIC_OWNER_NAME,
            "download_link": MUSIC_DOWNLOAD_LINK,
            "cover_image": MUSIC_COVER_IMAGE_DOWNLOAD_LINK
        },
        "hashtags": [LIST OF HASHTAGS]
    }
    ```

- ### User Related Funtions

    #### Main setup
    ```python
    from TikTool import User

    user = User("username")
    ```

    #### Download all the user published videos with or without watermark
    ```python
    # download all the user published videos (with watermark)
    user.downloadAllVideos(watermark=True)

    # download all the user published videos (without watermark)
    user.downloadAllVideos(watermark=False)

    # if the watermark parameter was not passed,
    # it will be set to True by default
    ```

    #### Download the user profile picture
    ```python
    # download the user profile picture
    user.downloadProfilePicture()
    ```

## Where are the downloaded files
All the downloaded files will be saved in this folder structure.
The `downloads` folder being :
 - At the same directory level of the script running the funtion downloading a file
 - Or in the project root folder

        .
        ├── ...
        ├── downloads                             # All downloaded files will be downloaded here
        |   |
        │   ├── videos                            # Each video will have a folder named after his ID
        |   |   ├── 6871...                       #   Each of those folders will contain the : 
        |   |   ├── 5381...                       #   - downloaded video (with or without watermark)
        |   |   ├── 8142...                       #   - downloaded video thumbnail
        |   |   ├── 6897...                       #   - downloaded audio
        |   |   ├── 8687...                       #   - downloaded audio cover
        |   |   └── ...
        |   |
        │   ├── users                             # Each user will have a folder named after his username
        |   |   ├── username1
        |   |   |   ├── wm                        # All the user downloaded videos will be here (with watermark) 
        |   |   |   ├── no-wm                     # All the user downloaded videos will be here (without watermark)    
        |   |   |   ├── username1-profile.jpeg    # The user profile picture
        |   |   |
        |   |   ├── username2
        |   |   |   ├── wm  
        |   |   |   ├── no-wm      
        |   |   |   ├── username2-profile.jpeg 
        |   |   └── ...
        |   |
        └── ...
