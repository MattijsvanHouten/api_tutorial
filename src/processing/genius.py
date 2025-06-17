import os
from typing import Optional

from dotenv import load_dotenv
from lyricsgenius import Genius
from lyricsgenius.types import Artist

load_dotenv()


def get_genius_interface(verbose: bool = False) -> Genius:
    return Genius(os.getenv("ACCESS_TOKEN"), verbose=False)


def fetch_artist(genius: Genius, name: str, songs: int = 3) -> Optional[Artist]:
    artist = genius.search_artist(name, max_songs=songs)
    return artist


def fetch_lyrics(
    genius: Genius, song_id: int, remove_section_headers: bool = True
) -> Optional[str]:
    return genius.lyrics(song_id, remove_section_headers)
