# -*- coding: utf-8 -*-
"""Resources wrap the results from an Api call."""


class AddressResource(object):
    """Wrap the result of an /v2/addresses/?postcode={0}&number={1} call."""
    # pylint: disable=missing-docstring

    def __init__(self, resultdata):
        data = resultdata.get('_embedded', {}).get('addresses', [])
        if data:
            data = data[0]
        self._data = data

    @property
    def is_empty(self):
        return False if self._data else True

    @property
    def street(self):
        return self._data['street']

    @property
    def house_number(self):
        """
        House number can be empty when postcode search
        is used without house number
        """
        return self._data.get('number', self._data.get('house_number'))

    @property
    def postcode(self):
        return self._data.get('postcode')

    @property
    def town(self):
        return self._data.get('city', {}).get('label', self._data.get('town'))

    @property
    def municipality(self):
        result = self._data.get('municipality', {})
        if isinstance(result, dict):
            result = result.get('label')
        return result

    @property
    def province(self):
        result = self._data.get('province', {})
        if isinstance(result, dict):
            result = result.get('label')
        return result

    def _get_geo_coordinates(self, geo_type):
        return self._data.get('geo', {}).get('center', {}).get(geo_type)\
            .get('coordinates', [None, None])

    @property
    def latitude(self):
        if self._data.get('latitude'):
            return self._data.get('latitude')
        return self._get_geo_coordinates('wgs84')[1]

    @property
    def longitude(self):
        if self._data.get('longitude'):
            return self._data.get('longitude')
        return self._get_geo_coordinates('wgs84')[0]

    @property
    def x(self):  # pylint: disable=invalid-name
        if self._data.get('x'):
            return self._data.get('x')
        return self._get_geo_coordinates('rd')[0]

    @property
    def y(self):  # pylint: disable=invalid-name
        if self._data.get('y'):
            return self._data.get('y')
        return self._get_geo_coordinates('rd')[1]
