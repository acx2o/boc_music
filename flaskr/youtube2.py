
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import os

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = os.environ['DEVELOPER_KEY']
# DEVELOPER_KEY = os.environ['DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query):
    print('------------------')
    print(query)
    # print(type(query))

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    print("***********************")
    print( youtube.search().list(
    q=query,#検索キーワード
    part="id,snippet",
    maxResults=10
    ))
    search_response = youtube.search().list(
    q=query,#検索キーワード
    part="id,snippet",
    maxResults=10
    ).execute()

    videos = []
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    print(search_response)
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            # videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
            videos.append([search_result["snippet"]["title"],search_result["id"]["videoId"]])
            print("***********************")
            print(search_result["snippet"]["title"])
    # print("***********************")
    # print()
    # print("***********************")
    # print(videos[0][1])
    return videos[0][1]
    # print("Videos:\n", "\n".join(videos), "\n")



if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

    try:
        youtube_search(args)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
