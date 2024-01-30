# coding: utf-8
from __future__ import unicode_literals
import re

from youtube_dl.utils import str_or_none, traverse_obj

from .common import InfoExtractor


class DzenEmbeddedIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?dzen\.ru/embed/(?P<id>[a-zA-Z0-9]+)'
    _TEST = {
        'url': 'https://dzen.ru/embed/vnVEaPfaSym8',
        'md5': '52da73c2eb1a469e5bdb0d294b0cdaeb',
        'info_dict': {
            'id': 'vnVEaPfaSym8',
            'ext': 'm3u8',
            'title': 'ИКЕА под новым брендом? Обзор SWED HOUSE "IKEA" ожидание / реальность',
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(
            url, video_id)

        formats = []
        json_str = re.search(r'Dzen.player.init\(({[\s\w\D\d]*})', webpage)
        json_dict = self._parse_json(json_str.group(1), video_id)
        data = json_dict['data']
        print(traverse_obj(data, ('content', 'streams', 1, 'url')))
        formats.extend(self._extract_m3u8_formats(
            traverse_obj(data, ('content', 'streams', 1, 'url')),
            video_id,
            m3u8_id='hls'
        ))
        return {
            'id': video_id,
            'title': str_or_none(traverse_obj(data, ('content', 'streams', 0, 'title'))),
            'formats': formats,
        }