from traveltime import AcceptType, dto
from traveltime.dto import Location
from traveltime.dto.requests import time_map, time_filter, routes, Rectangle
from traveltime.dto.requests.routes import RoutesRequest
from traveltime.dto.requests.time_filter import TimeFilterRequest

from traveltime.dto.requests.time_map import *
from traveltime.dto.responses.map_info import MapInfoResponse
from traveltime.dto.responses.routes import RoutesResponse
from traveltime.dto.responses.time_filter import TimeFilterResponse
from traveltime.dto.responses.time_map import TimeMapResponse
from traveltime.utils import *

from geojson_pydantic import FeatureCollection


class TravelTimeSdk:

    def __init__(self, app_id: str, api_key: str) -> None:
        self.__app_id = app_id
        self.__api_key = api_key

    def map_info(self) -> MapInfoResponse:
        return send_get_request(MapInfoResponse, 'map-info', self.__headers(AcceptType.JSON))

    async def map_info_async(self) -> MapInfoResponse:
        return await send_get_request_async(MapInfoResponse, 'map-info', self.__headers(AcceptType.JSON))

    def time_map(
        self,
        arrival_searches: List[dto.requests.time_map.ArrivalSearch],
        departure_searches: List[dto.requests.time_map.DepartureSearch],
        unions: List[Union] = None,
        intersections: List[Intersection] = None
    ) -> TimeMapResponse:
        return send_post_request(
            TimeMapResponse,
            'time-map',
            self.__headers(AcceptType.JSON),
            TimeMapRequest(
                departure_searches=departure_searches,
                arrival_searches=arrival_searches,
                unions=unions,
                intersections=intersections
            )
        )

    async def time_map_async(
        self,
        arrival_searches: List[dto.requests.time_map.ArrivalSearch] = None,
        departure_searches: List[dto.requests.time_map.DepartureSearch] = None,
        unions: List[Union] = None,
        intersections: List[Intersection] = None
    ) -> TimeMapResponse:
        return await send_post_request_async(
            TimeMapResponse,
            'time-map',
            self.__headers(AcceptType.JSON),
            TimeMapRequest(
                departure_searches=departure_searches,
                arrival_searches=arrival_searches,
                unions=unions,
                intersections=intersections
            )
        )

    def time_filter(
        self,
        locations: List[Location],
        departure_searches: List[dto.requests.time_filter.DepartureSearch],
        arrival_searches: List[dto.requests.time_filter.ArrivalSearch]
    ) -> TimeFilterResponse:
        return send_post_request(
            TimeFilterResponse,
            'time-filter',
            self.__headers(AcceptType.JSON),
            TimeFilterRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    async def time_filter_async(
        self,
        locations: List[Location],
        departure_searches: List[dto.requests.time_filter.DepartureSearch],
        arrival_searches: List[dto.requests.time_filter.ArrivalSearch]
    ) -> TimeFilterResponse:
        return await send_post_request_async(
            TimeFilterResponse,
            'time-filter',
            self.__headers(AcceptType.JSON),
            TimeFilterRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    def routes(
        self,
        locations: List[Location],
        departure_searches: List[dto.requests.routes.DepartureSearch],
        arrival_searches: List[dto.requests.routes.ArrivalSearch]
    ) -> RoutesResponse:
        return send_post_request(
            RoutesResponse,
            'routes',
            self.__headers(AcceptType.JSON),
            RoutesRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    async def routes_async(
        self,
        locations: List[Location],
        departure_searches: List[dto.requests.time_filter.DepartureSearch],
        arrival_searches: List[dto.requests.time_filter.ArrivalSearch]
    ) -> RoutesResponse:
        return await send_post_request_async(
            RoutesResponse,
            'routes',
            self.__headers(AcceptType.JSON),
            RoutesRequest(
                locations=locations,
                departure_searches=departure_searches,
                arrival_searches=arrival_searches
            )
        )

    def geocoding(
        self,
        query: str,
        limit: Optional[int] = None,
        within_countries: Optional[List[str]] = None,
        format_name: Optional[bool] = None,
        format_exclude_country: Optional[bool] = None,
        rectangle: Optional[Rectangle] = None
    ) -> FeatureCollection:
        full_query = {
            'query': query,
            'limit': limit,
            'within.country': self.__combine_countries(within_countries),
            'format.name': format_name,
            'format.exclude.country': format_exclude_country,
            'bounds': self.__bounds(rectangle)
        }
        params = {key: str(value) for (key, value) in full_query.items() if value is not None}
        return send_get_request(FeatureCollection, 'geocoding/search', self.__headers(AcceptType.JSON), params)

    def geocoding_reverse(self, lat: float, lng: float, within_countries: Optional[List[str]] = None):
        full_query = {
            'lat': lat,
            'lng': lng,
            'within.country': self.__combine_countries(within_countries)
        }
        params = {key: str(value) for (key, value) in full_query.items() if value is not None}
        return send_get_request(FeatureCollection, 'geocoding/reverse', self.__headers(AcceptType.JSON), params)

    @staticmethod
    def __bounds(rectangle: Optional[Rectangle]) -> Optional[str]:
        if rectangle is not None:
            return f'{rectangle.min_lat},{rectangle.min_lng},{rectangle.max_lat},{rectangle.max_lng}'
        else:
            return None

    @staticmethod
    def __combine_countries(within_countries: Optional[List[str]]) -> Optional[str]:
        return ','.join(within_countries) if within_countries is not None and len(within_countries) != 0 else None

    def __headers(self, accept_type: AcceptType) -> Dict[str, str]:
        return {
            'X-Application-Id': self.__app_id,
            'X-Api-Key': self.__api_key,
            'Content-Type': 'application/json',
            'Accept': accept_type.value
        }
