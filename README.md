# W.I.P. CovidPy 🦠

CovidPy is a python library to work with DCCs (Digital Covid Certificates).
Using this library you can:

1) Decode the content of a DCC and get the raw json
2) Encode a VALID json and create a recognizable DCC (it will only work with a json containint a valid DCC's info)
3) Verify a DCC it will verify the validity of a DCC also checking if it's not revoked

Please remember that this library is in it's early stages and it's not complete, there could be some bugs or missing features, if you find any, please report in an issue
if you have any question you can open an issue or ask me on [telegram](t.me/cagavo)
if you know how to improve this library, please send me a pull request, you can find a list of things to do [here](#TODO)

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

### useful links

- https://forum.italia.it/t/verifica-green-pass-api/25190/85?page=5
- https://github.com/ministero-salute/dcc-utils/issues/1