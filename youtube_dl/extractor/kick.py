# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import float_or_none, str_or_none, traverse_obj, unified_timestamp, url_or_none

class KickVideoIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?kick\.com/video/(?P<id>[\w\W]+)'
    _TEST = {
        'url': 'https://kick.com/video/e335c041-acca-4c5f-9c4e-1a6e4643462c',
        'md5': 'b85792f8d770b7869483365b4a8b2278',
        'info_dict': {
            'id': 'e335c041-acca-4c5f-9c4e-1a6e4643462c',
            'ext': 'mp4',
            'title': '2',
            'description': 'THE BEST AT ABSOLUTELY EVERYTHING. THE JUICER. LEADER OF THE JUICERS.',
            'upload_date': '20240124',
            'timestamp': 1706091601,
            'uploader': 'xQc',
            'uploader_id': '676',
            'channel': 'xqc',
            'channel_id': '668',
            'duration': 27228.0,
            'categories': ['Just Chatting'],
            'thumbnail': r're:^https?://.*\.jpg',
            'tags': ["IRL"]
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        headers = {
            'Authorization': f'Bearer {self._get_cookies("https://kick.com/").get("XSRF-TOKEN")}'
        }
        response = self._download_json(
            f'https://kick.com/api/v1/video/{video_id}', video_id, note='Downloading API JSON',
            headers=headers
        )

        return {
            'id': video_id,
            'formats': self._extract_m3u8_formats(response['source'], video_id, 'mp4'),
            'title': traverse_obj(
                response, ('livestream', ('session_title', 'slug')), get_all=False, default=''),
            'description': traverse_obj(response, ('livestream', 'channel', 'user', 'bio')),
            'channel': traverse_obj(response, ('livestream', 'channel', 'slug')),
            'channel_id': str_or_none(traverse_obj(response, ('livestream', 'channel', 'id'))),
            'uploader': traverse_obj(response, ('livestream', 'channel', 'user', 'username')),
            'uploader_id': str_or_none(traverse_obj(response, ('livestream', 'channel', 'user_id'))),
            'timestamp': unified_timestamp(response.get('created_at')),
            'duration': float_or_none(traverse_obj(response, ('livestream', 'duration')), scale=1000),
            'thumbnail': traverse_obj(
                response, ('livestream', 'thumbnail'), expected_type=url_or_none),
            'categories': traverse_obj(response, ('livestream', 'categories', ..., 'name')),
            'tags': traverse_obj(response, ('livestream', 'categories', ..., 'tags', ...)) or None,
        }