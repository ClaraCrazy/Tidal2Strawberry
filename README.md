# Tidal2Strawberry, a long needed script

![2023-04-02-093545](https://user-images.githubusercontent.com/55334727/229339313-177159c2-ca1c-4705-a043-791a9b4356d9.png)


#### Note, this script was written by @WillyJL, a good friend of mine. All credits to him. Sponsorship links on this repository will be his.

-----

### Why / What is this?

Tidal is known for not having a linux client. Theres Tidal-hifi but thats just an embedded Browser window. Not useful at all. I wanted my Master quality. Ofc, this will not give me the best I can have, due to tidals MQA format, but my FLAC files will still be higher quality than they were before. *yay*

This script allows you to convert either a single, or all Tidal playlists of any account to be importable in Strawberry. The original author of said player has neglected Playlists for over three years now, so we took it upon ourselves.

### How does it work?

- It takes a Tidal playlist or user URL as a launch argument. If you dont pass one, it will ask you for it upon running.

- Once given its link, it will scrape the Tidal website for that User / Playlist and get all playlist data, arrange it how Strawberry needs it, and then saves it to a .xspf file Strawberry can read

### Perfect solution?

**No**. I'm working on writing a playlist patch for tidal, or paying someone else due to limited time. This script will not garuantee Master quality. Its a 50/50 if the picked version of a track is Master, even tho the playlist is full of only those.
