# -*- coding: utf-8 -*-
"""Api wrapper for https://postcode-api.apiwise.nl"""
import re
try:
    from urllib.request import urlopen, Request, HTTPError  # for Python 3
except ImportError:
    from urllib2 import urlopen, Request, HTTPError  # for Python 2

import json
import logging

from . import exceptions
from .resources import AddressResource


_logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


# One non zero digit, three other digits, wo letters but not SA, SD or SS.
# Before using expression postal code will be normalized (no space, uppercase).
VALID_DUTCH_POSTCODE = re.compile(r'^[1-9][0-9]{3}(?!SA|SD|SS)[A-Z]{2}$')

# House number must be between 1 and 5 digits, not starting with 0.
VALID_DUTCH_HOUSE_NUMBER = re.compile(r'^[1-9][0-9]{0,4}$')


class Api(object):
    """Encapsulate calls to postcode-api."""

    def __init__(self, api_key, api_version=(2, 0, 0)):
        if not api_key:
            raise exceptions.PostcodeApiKeyError(
                "Api key is noodzakelijk."
                " Vraag deze aan via http://postcodeapi.nu")
        self.api_key = api_key
        self.api_version = api_version
        self.url = 'https://postcode-api.apiwise.nl'

    def request(self, path=None):
        """Helper function for HTTP GET requests to the API.

        The result data will be converted to a json dictionary.
        """
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en",
            "X-Api-Key": self.api_key}
        try:
            result = urlopen(Request(self.url + path, headers=headers))
            code = result.getcode()
            if code == 200:
                resultdata = result.read()
                if isinstance(resultdata, bytes):
                    resultdata = resultdata.decode("utf-8")  # for Python 3
                jsondata = json.loads(resultdata)
                return jsondata
            self.handle_response_error(code)
        except HTTPError as http_error:
            code = http_error.getcode()
            _logger.exception(
                "Fout opgetreden in postcode API aanroep %s"
                " met code %d en omschrijving %s.",
                path, code, http_error.reason)
            self.handle_response_error(code)
        except Exception:  # pylint: disable=broad-except
            # Be prepared for all expected or unexpected occurences,
            # that may, or may not, occur.
            _logger.exception(
                "Onverwachte fout opgetreden in postcode API aanroep.")
            raise

    def get_postcode_info(self, postcode, house_number):
        """Get info for postcode.

        Throw exception if any error occurs.
        """
        postcode = postcode.replace(' ', '').upper()
        if not VALID_DUTCH_POSTCODE.match(postcode):
            raise exceptions.PostcodeBadArgumentError(
                "Ongeldige postcode %s" % postcode)
        house_number = house_number or ''
        if not VALID_DUTCH_HOUSE_NUMBER.match(house_number):
            raise exceptions.PostcodeBadArgumentError(
                "Ongeldig huisnummer %s" % house_number)
        path = '/v2/addresses/?postcode={0}&number={1}'.format(
            str(postcode), str(house_number))
        data = self.request(path)
        resource = AddressResource(data)
        if resource.is_empty:
            raise exceptions.PostcodeValidationError(
                "Geen geldige postcode + huisnummer combinatie:"
                "%s %s." % (postcode, house_number))
        return resource

    def getaddress(self, postcode, house_number=None):
        """Return info for postcode, or None.

        This function is deprecated. It silences all exceptions. Replace by
        calls to get_postcode_info().
        """
        try:
            return self.get_postcode_info(
                postcode, house_number=house_number)
        except exceptions.PostcodeException as exc:
            _logger.error(
                'Fout bij opzoeken van %s%s%s op %s: %d %s',
                postcode, house_number and ' ' or '', house_number, self.url,
                exc.status, exc.message)
        except Exception as exc:  # pylint: disable=broad-except
            _logger.exception(exc)
        return False

    def handle_response_error(self, status):
        """Translate http response codes into errors."""
        if status == 200:
            return  # should not raise error
        if status == 400:
            raise exceptions.PostcodeBadRequestError(
                "Ongeldige aanroep in %s" % self.url)
        if status == 401:
            raise exceptions.PostcodeApiKeyError(
                "Ongeldige Api Key %s" % self.api_key)
        if status == 403:
            raise exceptions.PostcodeAuthorizationError(
                "Geen toestemming voor deze aanroep in %s" % self.url)
        if status == 404:
            raise exceptions.PostcodeNotFoundError(
                "gevraagde gegevens niet gevonden voor aanroep in %s" %
                self.url)
        if status == 429:
            raise exceptions.PostcodeLimitError(
                "Het maximale aantal aanroepen van de api is al bereikt")
        raise exceptions.PostcodeUnknownError(
            "Onverwachte http response code %d ontvangen van api aanroep" %
            status)
