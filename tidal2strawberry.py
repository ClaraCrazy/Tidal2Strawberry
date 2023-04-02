# Imports
import asyncio
import pathlib
import aiohttp
import sys
import bs4
import sys
import os

headers = {
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    "accept-encoding": 'gzip, deflate, br',
    "accept-language": 'en-US,en;q=0.9',  # Only actually needed one LOL
    "cache-control": 'max-age=0',
    "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    "sec-ch-ua-mobile": '?0',
    "sec-ch-ua-platform": 'Linux"',
    "sec-fetch-dest": 'document',
    "sec-fetch-mode": 'navigate',
    "sec-fetch-site": 'same-origin',
    "sec-fetch-user": '?1',
    "upgrade-insecure-requests": '1',
    "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}


def is_class(name: str):
    def _is_class(elem: bs4.element.Tag):
        return hasattr(elem, "get_attribute_list") and name in elem.get_attribute_list("class")
    return _is_class

async def convert(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as req:
        raw = await req.read()
    html = bs4.BeautifulSoup(raw, "lxml")

    playlist_name = html.head.title.text.strip().removesuffix("on TIDAL").strip()
    tracks = list(html.find_all(is_class("track-wrapper")))
    if not tracks:
        print(f"Failed exporting '{playlist_name}'!")
        return

    xml = bs4.BeautifulSoup("""
        <playlist version="1" xmlns="http://xspf.org/ns/0/">
            <trackList>
            </trackList>
        </playlist>
    """, "xml")
    trackList = xml.find("trackList")

    cleantext = lambda text: " ".join(line.strip() for line in text.splitlines() if line.strip())
    for i, track_elem in enumerate(tracks):
        track = xml.new_tag("track")
        track_name = track_elem.find(is_class("track-name")).find("a")
        track_album = track_elem.find(is_class("track-info")).find(is_class("secondary-title")).find("a")

        track.insert(0, xml.new_tag("location"))
        track.location.string = "tidal%3A" + track_name.get("href").strip().rstrip("/").rsplit("/", 1)[1]

        track.insert(1, xml.new_tag("title"))
        track.title.string = cleantext(track_name.text)

        track.insert(2, xml.new_tag("creator"))
        track.creator.string = ", ".join(cleantext(el.text) for el in list(track_elem.find(is_class("artist-list")).find_all("a")))

        track.insert(3, xml.new_tag("album"))
        track.album.string = cleantext(track_album.text)

        track.insert(4, xml.new_tag("trackNum"))
        track.trackNum.string = str(i + 1)

        trackList.insert(i, track)

    xml = str(xml)
    xml = "\n".join(line.strip() for line in xml.splitlines() if line.strip())
    pathlib.Path(f"{playlist_name}.xspf").write_text(xml)
    print(f"Exported '{playlist_name}'!")

async def main():
    os.system('cls' if os.name=='nt' else 'clear')
    try:
            url = sys.argv[1]
    except:
        print("This script allows you to convert Tidal playlist URLs to xspf files Strawberry can read")
        url = input("Please enter either a profile URL or a playlist URL to start the conversion.\n\nLink: ")
    async with aiohttp.ClientSession(headers=headers) as session:
        urls = set()

        if "/browse/playlist/" in url:
            async with session.get(url) as req:
                raw = await req.read()
            html = bs4.BeautifulSoup(raw, "lxml")
            user = html.select_one('a[href*="/browse/user/"]')
            if user:
                choice = input("Do you want to download all the playlists by this user? (y/N) ")
                if choice.lower() not in ("y", "yes"):
                    user = None
            if user:
                url = "https://tidal.com" + user.get("href")
            else:
                urls.add(url)

        if "/browse/user/" in url:
            async with session.get(url) as req:
                raw = await req.read()
            html = bs4.BeautifulSoup(raw, "lxml")
            for playlist in html.select('a[href*="/browse/playlist/"]'):
                urls.add("https://tidal.com" + playlist.get("href"))

        if not urls:
            print("Nothing to export!")
            return

        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(convert(session, url)))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
