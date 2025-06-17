from datetime import date
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ArtistSongAssociation(Base):
    __tablename__ = "artist_songs"

    artist_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("artists.id"), primary_key=True
    )
    song_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("songs.id"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"ArtistTitleAssociation(artist_id={self.artist_id}, song_id={self.song_id}>)"


class AltName(Base):
    __tablename__ = "alt_names"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    artist_id: Mapped[int] = mapped_column(sa.ForeignKey("artists.id"))
    name: Mapped[str] = mapped_column(sa.String)

    artist: Mapped["Artist"] = relationship(
        "Artist", back_populates="alternative_names"
    )


class Artist(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String)
    url: Mapped[str] = mapped_column(sa.String)
    is_verified: Mapped[bool] = mapped_column(sa.Boolean)
    description: Mapped[str] = mapped_column(sa.String)

    alternative_names: Mapped[list["AltName"]] = relationship(
        "AltName", back_populates="artist"
    )
    songs: Mapped[list["Song"]] = relationship(
        "Song", secondary="artist_songs", back_populates="artists"
    )

    def __repr__(self) -> str:
        return f"<Artist(id={self.id}), name={self.name}>"


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String)
    language: Mapped[str] = mapped_column(sa.String)
    lyrics: Mapped[Optional[str]] = mapped_column(sa.String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(sa.String, nullable=True)
    release_date: Mapped[date] = mapped_column(sa.Date)

    artists: Mapped[list["Artist"]] = relationship(
        "Artist", secondary="artist_songs", back_populates="songs"
    )

    def __repr__(self) -> str:
        return f"<Song(id={self.id}, title={self.title})>"


# from sqlalchemy import create_engine

# engine = create_engine("sqlite:///data/data.db")
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
