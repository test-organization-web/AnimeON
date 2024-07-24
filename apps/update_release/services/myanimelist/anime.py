import logging


logger = logging.getLogger(__name__)


class AnimeMixin:

    def get_anime_details(self, id) -> dict:
        id = str(id)
        params = {
            'fields': ','.join(self.anime_fields),
        }
        uri = f'anime/{id}'
        logger.info('Get anime details', extra={
            'message_id': 'myanimelist_get_anime_detail',
        })
        return self._api_handler.call(uri, params=params)

    # need pagination here
    def search_anime(self, keyword, limit=20) -> dict:
        uri = 'anime'
        params = {
            "q": keyword,
            'fields': ','.join(self.anime_fields),
            'limit': limit
        }
        logger.info('Search anime', extra={
            'message_id': 'myanimelist_search_anime',
        })
        return self._api_handler.call(uri=uri, params=params)

    def get_anime_ranking(self, ranking_type="all", limit=20) -> dict:
        uri = 'anime/ranking'
        ranking_types = [
            "all", "airing", "upcoming", "tv", "ova", "movie", "special",
            "bypopularity", "favorite"
        ]
        if ranking_type not in ranking_types:
            logger.info('Anime ranking not exist', extra={
                'message_id': 'myanimelist_get_anime_ranking',
                'uri': uri,
                'ranking_type': ranking_type,
            })
            return {}
        params = {
            "ranking_type": ranking_types,
            "fields": ','.join(self.anime_fields),
            "limit": limit
        }
        logger.info('Get anime ranking', extra={
            'message_id': 'myanimelist_get_anime_ranking',
        })
        return self._api_handler.call(uri=uri, params=params)

    def get_seasonal_anime(self, year, season, sort="anime_score", limit=20) -> dict:
        seasons = ["winter", "spring", "summer", "fall"]
        if season not in seasons:
            logger.info('Anime season not exist', extra={
                'message_id': 'myanimelist_get_seasonal_anime',
                'season': season,
            })
            return {}

        sort_options = ["anime_score", "anime_num_list_users"]
        if sort not in sort_options:
            logger.info('Anime sort not exist', extra={
                'message_id': 'myanimelist_get_seasonal_anime',
                'sort': sort,
            })
            return {}
        uri = f'anime/season/{year}/{season}'

        params = {
            "sort": sort,
            "limit": limit,
            "fields": ','.join(self.anime_fields)
        }
        logger.info('Get anime ranking', extra={
            'message_id': 'myanimelist_get_seasonal_anime',
        })
        return self._api_handler.call(uri=uri, params=params)

    def get_suggested_anime(self, limit=20, offset=0) -> dict:
        uri = 'anime/suggestions'
        params = {
            "limit": limit,
            "offset": offset
        }
        logger.info('Get anime ranking', extra={
            'message_id': 'myanimelist_get_suggested_anime',
        })
        return self._api_handler.call(uri=uri, params=params)
