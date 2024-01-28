# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import (
    float_or_none,
    int_or_none,
    parse_iso8601,
    str_or_none,
    strip_or_none,
    traverse_obj,
    url_or_none,
)


class KickClipIE(InfoExtractor):
    _VALID_URL = r'https?:\/\/(?:www\.)?kick\.com\/[\w\W]+\?clip=(?P<id>clip_[0-9a-zA-Z]+)'

    _TESTS = [{
        'url': 'https://kick.com/xqc?clip=clip_01H811MXG4FBR62FXPE1AXABDH',
        'md5': 'dd6ac9903ae5df10d51a460de0b4d847',
        'info_dict': {
            'id': 'clip_01H811MXG4FBR62FXPE1AXABDH',
            'ext': 'mp4',
            'title': 'soda',
            'channel': 'xqc',
            'thumbnail': r're:^https?://.*\.png.*$',
            'created_at': '20240128',
            'creator': 'wasab7i'
        }
    }]

    def _real_extract(self, url):
        id = self._match_id(url)

        headers = {
            'Accept': 'application/json',
        }

        data = self._download_json(f'https://kick.com/api/v2/clips/{id}', id, headers=headers)

        clip = data['clip']
        creator = data['creator']
        channel = data['channel']
        formats = self._extract_m3u8_formats(
            clip['video_url'], id, 'mp4')
        self._sort_formats(formats)

        return {
            'id': id,
            'formats': formats,
            'title': clip.get('title'),
            'channel': str_or_none(channel.get('slug')),
            'thumbnail': url_or_none(clip.get('video_url')),
            'creator': str_or_none(creator.get('slug')),
        }




class KickVideoIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?kick\.com/video/(?P<id>[0-9a-zA-Z-]+)'
    _TESTS = [{
        'url': 'https://kick.com/video/e335c041-acca-4c5f-9c4e-1a6e4643462c',
        'md5': 'dd6ac9903ae5df10d51a460de0b4d847',
        'info_dict': {
            'id': 'e335c041-acca-4c5f-9c4e-1a6e4643462c',
            'ext': 'mp4',
            'title': '2',
            'uploader': 'xQc',
            'thumbnail': r're:^https?://.*\.jpg.*$',
            'timestamp': 1706416672,
            'upload_date': '20240128',
        }
    }]

    def _real_extract(self, url):
        id = self._match_id(url)

        headers = {
            'Accept': 'application/json',
        }

        data = self._download_json(f'https://kick.com/api/v1/video/{id}', id, headers=headers)

        formats = self._extract_m3u8_formats(
            data['source'], id, 'mp4')
        self._sort_formats(formats)
        livestream = data['livestream']
        strip_lambda = lambda x: strip_or_none(x) or None

        return {
            'id': id,
            'formats': formats,
            'title': livestream.get('session_title'),
            'uploader': traverse_obj(livestream, ('channel', 'user', 'username'), expected_type=strip_lambda),
            'thumbnail': url_or_none(livestream.get('thumbnail')),
            'duration': float_or_none(livestream.get('duration'), scale=1000),
            'timestamp': traverse_obj(data, 'updated_at', 'created_at', expected_type=parse_iso8601),
            'release_timestamp': parse_iso8601(data.get('created_at')),
            'view_count': int_or_none(data.get('views')),
            'is_live': livestream.get('is_live'),
            'channel': traverse_obj(livestream, ('channel', 'slug'), expected_type=strip_lambda),
            'categories': traverse_obj(data, ('categories', Ellipsis, 'name'), expected_type=strip_lambda) or None,
            'tags': traverse_obj(data, ('categories', Ellipsis, 'tags', Ellipsis), expected_type=strip_lambda) or None,
        }
