## Deprecated :(
I won't update this anymore.
as today (3/6/2022) it's still working, i don't guarantee any support.

# CovidPy BETA 🦠

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/340c661b7668410b977e42a2c351cffa)](https://app.codacy.com/gh/CovidPyLib/CovidPy?utm_source=github.com&utm_medium=referral&utm_content=CovidPyLib/CovidPy&utm_campaign=Badge_Grade_Settings)

CovidPy is a python library to work with DCCs (Digital Covid Certificates).
Using this library you can:

- Decode the content of a DCC and get the raw json
- Encode a VALID json and create a recognizable DCC (it will only work with a json containing a valid DCC's info and will still be marked as invalid since it's not signed with a valid european private key)
- Verify a DCC it will verify the validity of a DCC also checking if it's not revoked

Please remember that this library is in it's early stages and it's not complete, there could be some bugs or missing features, if you find any, please report in an issue
if you have any question you can open an issue or ask me on [telegram](https://t.me/cagavo)
if you know how to improve this library, please send me a pull request, you can find a list of things to do [here](#TODO)

### Installing

``` bash
pip install covidpylib
```

or

``` bash
pip install git+https://github.com/covidpylib/covidpy
```

### Examples
If you are searching for an example you can try [GreenPassValidator](https://github.com/CovidPyLib/GreenPassValidator), a very simple telegram bot that shows how to use this library

## Credits

- Files used to encode DCCs were generated using [this](https://github.com/ehn-dcc-development/ehn-sign-verify-python-trivial/blob/main/gen-csca-dsc.sh) 
- To get Public Keys we use [this API](https://verifier-api.coronacheck.nl/v4/verifier/public_keys)
- To get the revoked DCCs we use [this API](https://get.dgc.gov.it/v1/dgc/settings)

## TODO

- Update verificaton to use the italian API (https://get.dgc.gov.it/v1/) instead of the old one (https://verifier-api.coronacheck.nl/v4/)
- Support verification rules
- Docs
- Examples

## Licensed under GPL v3.0 or later


![GPLV3.0LATERLOGO](https://www.gnu.org/graphics/gplv3-or-later.png "Licensed under GPL v3.0 or later")

### Useful links

- https://forum.italia.it/t/verifica-green-pass-api/25190/85?page=5
- https://github.com/ministero-salute/dcc-utils/issues/1
- https://ec.europa.eu/health/system/files/2021-04/digital-green-certificates_dt-specifications_en_0.pdf
- https://ec.europa.eu/health/documents/community-register/html/
- https://github.com/ehn-dcc-development/ehn-dcc-schema
