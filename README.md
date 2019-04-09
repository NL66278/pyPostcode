pyPostcode
==========

## Introduction

This is a Python library to request information from the PostcodeApi.nu API.
This API allows you to search for Dutch addresses using zipcodes.

For more information about this API, please visit http://postcodeapi.nu

This library supports only the v2 api.


## Installation

### PyPI
`pip install pyPostcode`

### Manually

You can run pyPostcode by changing to the main directory and call it as a
package with the three required arguments:

python -m pyPostcode <api-key> <postal code> <house_number>

pyPostcode works with Python 2.7.x and 3.5.x (you're welcome to test other
versions)

### API-key

The API can only be used when you have your own API-key.
You can request this key by visiting: http://www.postcodeapi.nu/#pakketten


## Example

### Basic usage

Get the address by using the zipcode and the house number

```python
#!/usr/bin/python

from pyPostcode import Api

postcodeapi = Api('{YOUR_API_KEY}') # Set your own API-key
result = postcodeapi.getaddress('1011AC', 154) # use address search
print result.street, result.house_number, result.town
```

### Result data

the following information can be gathered from the result:

* street
* house_number
* postcode
* town
* municipality
* province
* latitude
* longitude
* x ([Rijksdriehoek]/[Trigonometrical] coordinate)
* y ([Rijksdriehoek]/[Trigonometrical] coordinate)

## Limitations

All messages/feedback are for now in Dutch. These should in the future
be in English, Dutch or possibly other languages based on user locale.

## License

"PostcodeApi" is owned by Apiwise, see http://postcodeapi.nu for more
information.
I am in no way affiliated with PostcodeAPI or the Apiwise organization.

[Rijksdriehoek]: http://nl.wikipedia.org/wiki/Rijksdriehoekscoördinaten
[Trigonometrical]: http://en.wikipedia.org/wiki/Triangulation_station

