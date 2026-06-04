import m3u8
from typing import List
from pathlib import Path


class M3u8Parser:
    def __init__(
            self,
            m3u8_content: str,
            ):
        self.m3u8_object = m3u8.loads(m3u8_content)

    def get_video_uris(self) -> List[str]:
        if self.m3u8_object.is_variant:
            raise ValueError("The provided m3u8 content is a variant playlist. Use get_playlists() instead.")
        video_uris = list()
        for index, segment in enumerate(self.m3u8_object.segments):
            video_uris.append(segment.uri)
        return video_uris

    def get_playlists(self) -> List[str]:
        sorted_playlists = sorted(
            self.m3u8_object.playlists,
            key=lambda pl: pl.stream_info.resolution[1],
            reverse=True
        )
        sorted_playlist_uris = [pl.uri for pl in sorted_playlists]
        return sorted_playlist_uris