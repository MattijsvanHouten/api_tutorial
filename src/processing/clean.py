from datetime import datetime
from typing import Any


def clean_song(songs: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": songs.get("id"),
        "title": songs.get("title"),
        "language": songs.get("language"),
        "lyrics": songs.get("lyrics"),
        "description": songs.get("description")["plain"],
        "release_date": datetime.strptime(songs.get("release_date"), "%Y-%m-%d").date(),
    }


def clean_artist(artist: dict[str, Any]) -> dict[str, Any]:
    songs = artist.get("songs")

    return {
        "id": artist.get("id"),
        "name": artist.get("name"),
        "url": artist.get("url"),
        "is_verified": artist.get("is_verified"),
        "description": artist.get("description")["plain"],
        "songs": [clean_song(song) for song in songs],
        "alternative_names": artist.get("alternate_names"),
    }
