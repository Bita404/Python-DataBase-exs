import requests

class Music:
    def __init__(self, name, artist_name, album_name, link):
        self.name = name 
        self.artist_name = artist_name
        self.album_name = album_name
        self.link = link

    def __str__(self):
        return f"{self.name} by {self.artist_name}\nAlbum: {self.album_name}\nPreview: {self.link}"

class GetSong:
    URL = "https://itunes.apple.com/search"

    def __init__(self, term):
        self.term = term

    def request(self):
        response = requests.get(self.URL, params={"term": self.term, "media": "music"})
        if response.status_code == 200:
             return response.json()
        return []


    @staticmethod
    def Read_data(item):
        name = item.get("trackName", "No Title")
        artist_name = item.get("artistName", "Unknown Artist")
        album_name = item.get("collectionName", "Unknown Album")
        link = item.get("previewUrl", "No URL")
        return name, artist_name, album_name, link

    def music_objects(self):
        data = self.request()
        if not data:
            print("No results Found ! !")
            return []

        results = data.get("results", [])
        music_objects = []
        for item in results:
            name, artist_name, album_name, link = self.Read_data(item)
            music = Music(name, artist_name, album_name, link)
            music_objects.append(music)
        return music_objects

if __name__ == "__main__":
    search = input("Enter the name of the song to search: ")
    fetcher = GetSong(search)
    music_list = fetcher.music_objects()

    if music_list:
        print("\n--- Song Results ---\n")
        for music in music_list:
            print(music)
            print("-" * 40)  ####...lines between results
    else:
        print("No results Found !  !")
