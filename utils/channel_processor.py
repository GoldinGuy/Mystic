import os

import googleapiclient.discovery
import googleapiclient.errors

# Parses the channels list and prints an env var containing all the upload playlists from youtube

API_KEY = os.environ["YOUTUBE_API_KEY"]


def main():
    channels_text = open("utils/youtube_channels_list.txt").read()
    channels = []
    playlists = []
    i = 0
    for line in channels_text.splitlines():
        if line.endswith("?"):
            continue
        if line == "==playlists==":
            i = 1
        try:
            id = line.split("#")[1].strip()
            if i == 0:
                channels.append(id)
            elif i == 1:
                playlists.append(id)
        except:
            pass

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=API_KEY)

    upload_playlists = []
    for channel in channels[1:]:
        try:
            request = youtube.channels().list(part="contentDetails", id=channel)
            response = request.execute()
            uploads_id = response["items"][0]["contentDetails"]["relatedPlaylists"][
                "uploads"
            ]
        except:
            request = youtube.channels().list(
                part="contentDetails", forUsername=channel
            )
            response = request.execute()
            uploads_id = response["items"][0]["contentDetails"]["relatedPlaylists"][
                "uploads"
            ]
        upload_playlists.append(uploads_id)

    print("YOUTUBE_CHANNEL_IDS=" + ";".join(upload_playlists + playlists))


if __name__ == "__main__":
    main()
