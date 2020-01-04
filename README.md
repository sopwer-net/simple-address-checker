# simple-address-checker
Getting suggestion when you type typo address using Levenshtein Algorithm

#how to use

```
pip install simple-address-checker

from address_checker import SubdistrictPayload, AddressChecker

subdistricts = SubdistrictPayload.load_subdistricts('id')

add_checker = AddressChecker(subdistricts, 'subdistrict_code')

add_checker.suggest(subdistrict_name='pameungpek',city_name='bandung')

```