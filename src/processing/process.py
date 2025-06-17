import logging
from typing import Any

from sqlalchemy.orm import Session

from data.models import AltName, Artist, ArtistSongAssociation, Song
from settings import settings
from utils.helpers import get_or_create

logger = logging.getLogger(__file__)
logger.setLevel(settings.log_level)


def load_artist_fields(artist: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": artist.get("id"),
        "name": artist.get("name"),
        "url": artist.get("url"),
        "is_verified": artist.get("is_verified"),
        "description": artist.get("description"),
    }


def insert_artist_data_to_db(db: Session, artist_dict: dict[str, Any]) -> None:
    logger.debug("Processing artist: %s", artist_dict.get("name"))

    artist_fields = load_artist_fields(artist_dict)

    get_or_create(db, Artist, **artist_fields)  # Add artist to db if not existing
    for alt_name in artist_dict.get("alternative_names"):
        get_or_create(
            db, AltName, artist_id=artist_dict.get("id"), name=alt_name
        )  # Add alt name to db if not existing

    songs = artist_dict.get("songs")

    for song in songs:
        get_or_create(db, Song, **song)  # Add song to db if not existing
        get_or_create(
            db,
            ArtistSongAssociation,
            artist_id=artist_dict.get("id"),
            song_id=song.get("id"),
        )  # Add artist song association if not existing

    logger.info("Artist and songs data processed successfully!")
