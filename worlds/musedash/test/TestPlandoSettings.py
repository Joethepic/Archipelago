from . import MuseDashTestBase


class TestIncludedSongSizeDoesntGrow(MuseDashTestBase):
    options = {
        "additional_song_count": 15,
        "allow_just_as_planned_dlc_songs": True,
        "include_songs": [
            "Operation Blade",
            "Autumn Moods",
            "Fireflies",
        ]
    }

    def test_included_songs_didnt_grow_item_count(self) -> None:
        muse_dash_world = self.multiworld.worlds[1]
        assert len(muse_dash_world.included_songs) == 15, \
            f"Logical songs size grew when it shouldn't. Expected 15. Got {len(muse_dash_world.included_songs)}"

    def test_included_songs_plando(self) -> None:
        muse_dash_world = self.multiworld.worlds[1]
        songs = muse_dash_world.included_songs.copy()
        songs.append(muse_dash_world.victory_song_name)

        assert "Operation Blade" in songs, "Logical songs is missing a plando song: Operation Blade"
        assert "Autumn Moods" in songs, "Logical songs is missing a plando song: Autumn Moods"
        assert "Fireflies" in songs, "Logical songs is missing a plando song: Fireflies"