# -*- coding: utf-8 -*-
"""Exceptions for the pyPostcode module."""


class PostcodeException(Exception):
    """Base class for pyPostcode Exceptions."""
    def __init__(self, message):
        super(PostcodeException, self).__init__(message)
        self.message = message


class PostcodeBadRequestError(PostcodeException):
    """Use this when receiving http 400 code."""
    def __init__(self, message):
        super(PostcodeBadRequestError, self).__init__(message)


class PostcodeApiKeyError(PostcodeException):
    """Use this when receiving http 401 code.

    In reality an invalid api key will often be answered with a 403
    (not authorized) response.
    """
    def __init__(self, message):
        super(PostcodeApiKeyError, self).__init__(message)


class PostcodeAuthorizationError(PostcodeException):
    """Use this when receiving http 403 code."""
    def __init__(self, message):
        super(PostcodeAuthorizationError, self).__init__(message)


class PostcodeNotFoundError(PostcodeException):
    """Use this when receiving http 404 code."""

    def __init__(self, message):
        super(PostcodeNotFoundError, self).__init__(message)


class PostcodeLimitError(PostcodeException):
    """Use this when receiving http 429 code.

    Returned when limit for free account reached.
    """
    def __init__(self, message):
        super(PostcodeLimitError, self).__init__(message)


class PostcodeUnknownError(PostcodeException):
    """Use this when receiving unexpected http code."""
    def __init__(self, message):
        super(PostcodeUnknownError, self).__init__(message)


class PostcodeValidationError(PostcodeException):
    """Use this when user requests info for non existing postcode."""
    def __init__(self, message):
        super(PostcodeValidationError, self).__init__(message)


class PostcodeBadArgumentError(PostcodeException):
    """Use this when arguments for Api call are invalid."""
    def __init__(self, message):
        super(PostcodeBadArgumentError, self).__init__(message)
