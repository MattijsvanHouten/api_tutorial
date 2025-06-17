import logging

from dotenv import load_dotenv

from data.models import Base
from data.session import get_engine, get_session
from processing.clean import clean_artist
from processing.genius import fetch_artist, get_genius_interface
from processing.process import insert_artist_data_to_db
from settings import settings

logger = logging.getLogger(__file__)
logger.setLevel(settings.log_level)

load_dotenv()  # Load .env variables

engine = get_engine(settings.database_url)
SessionLocal = get_session(engine)

# Create tables in the database if they don't exist
logger.info("Creating tables in the database if they don't exist...")
Base.metadata.create_all(bind=engine)


def main() -> None:
    genius = get_genius_interface()
    artist = fetch_artist(genius, "Billie Eilish")
    cleaned_artist = clean_artist(artist.to_dict())

    with SessionLocal() as session:
        insert_artist_data_to_db(session, cleaned_artist)


if __name__ == "__main__":
    main()
