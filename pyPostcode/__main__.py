#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Script to call the pyPostcode API from the command line."""
# pylint: disable=invalid-name
from __future__ import print_function
import argparse
import logging
import traceback

from .api import Api


def main(args):
    """Main routine."""
    try:
        api_interface = Api(args.api_key)
        address_info = api_interface.get_postcode_info(
            args.postcode, args.house_number)
        print(
            "%(street)s %(house_number)s\n"
            "%(postcode)s  %(town)s\n"
            "%(province)s" % {
                'street': address_info.street,
                'house_number': args.house_number,
                'postcode': args.postcode.upper(),
                'town': address_info.town,
                'province': address_info.province})
    except Exception:  # pylint: disable=broad-except
        traceback.print_exc()


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Retrieve address information for postcode and housenumber.\n"
            "Example: python pyPostcode.py -a <db>"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        dest='api_key', help="The api-key for the postcode api.")
    parser.add_argument(dest='postcode', help="Postal code.")
    parser.add_argument(dest='house_number', help="House number.")
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig()
    parms = get_args()
    main(parms)
