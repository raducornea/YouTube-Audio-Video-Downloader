import re

import user_interface as ui

if __name__ == '__main__':
    ui.Interface().open_application()

#
# from pytube import Playlist
# from pytube import YouTube
#
# # todo playlists SHOULD be linked ONLY by their PLAYLIST link (NOT VIDEO)
# playlist = Playlist('https://www.youtube.com/playlist?list=PLecgXXMM-YzT7KfWcAub4OJpu64alpKvM')
# # playlist = Playlist('https://www.youtube.com/watch?v=0nzI1vgtlFo&list=PLecgXXMM-YzT7KfWcAub4OJpu64alpKvM&index=1')
# playlist = Playlist("https://www.youtube.com/watch?v=pSbEuI2Z7oA&ab_channel=Apricot123")
# print(playlist.video_urls)
#
# # todo normal links ONLY for YouTube clips
# try:
#     video = YouTube('https://www.youtube.com/playlist?list=PLecgXXMM-YzT7KfWcAub4OJpu64alpKvM')
# except:
#     pass
#
# print("ok")
# # video = YouTube('https://www.youtube.com/watch?v=0nzI1vgtlFo&list=PLecgXXMM-YzT7KfWcAub4OJpu64alpKvM&index=1')
# # video = YouTube("https://www.youtube.com/watch?v=pSbEuI2Z7oA&ab_channel=Apricot123")
# # print(video.title)
#
#
# # print('Number of videos in playlist: %s' % len(playlist.video_urls))
# # playlist.download_all()