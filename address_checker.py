import json

import Levenshtein


class SubdistrictPayload:

    def __init__(self, lang):
        pass

    @classmethod
    def load_subdistricts(cls, lang='id', filename=None):
        if filename is None:
            path = "{}-{}.json".format("subdistricts", lang)
        else:
            path = filename

        with open(path) as json_file:
            data = json.load(json_file)
        return data


class AddressChecker:

    def __init__(self, subdistricts, key_index, string_matics=None):
        self.subdistricts = subdistricts
        self.key_index = key_index
        self.string_matrics = string_matics or Levenshtein

    def get_sim_subdistrict(self, keyword, include_only=[], count=10):
        '''
            get list subdistricts with scored by subdistrict
        :param keyword: your subdistrict name
        :param include_only: list of subdistrict please reference this file
        :param count: how many records do you want to get
        :return: list of subdistrict with lowest score
        '''
        search_key_named = 'subdistrict_name'
        results = []
        for subdistrict in self.subdistricts:
            if not include_only:
                sub = {}
                sub[self.key_index] = subdistrict[self.key_index]
                sub['score'] = self.string_matrics.distance(keyword, subdistrict[search_key_named].lower())
                results.append(sub)

            elif subdistrict[self.key_index] in include_only:
                sub = {}
                sub[self.key_index]= subdistrict[self.key_index]
                sub['score'] = self.string_matrics.distance(keyword, subdistrict[search_key_named].lower())
                results.append(sub)


        tmp = sorted(results, key=lambda i: i['score'])
        return list(filter(lambda x: x['score'] < 5, tmp))
        # return [{subdistrict} for subdistrict in tmp]

    def get_sim_city(self, keyword, include_only=[], count=10):
        '''
            get list subdistrict with scored by city
        :param keyword: your subdistrict name
        :param subdistricts: list of subdistrict please reference this file
        :param count: how many records do you want to get
        :return: list of subdistrict with lowest score
        '''
        search_key_named = 'city_name'
        results = []
        for subdistrict in self.subdistricts:
            if not include_only:
                sub = {}
                sub[self.key_index] = subdistrict[self.key_index]
                sub['score'] = self.string_matrics.distance(keyword, subdistrict[search_key_named].lower())
                results.append(sub)
            elif subdistrict[self.key_index] in include_only:
                sub = {}
                sub[self.key_index] = subdistrict[self.key_index]
                sub['score'] = self.string_matrics.distance(keyword, subdistrict[search_key_named].lower())
                results.append(sub)
        return sorted(results, key=lambda i: i['score'])[0:count]

    def check_if_extact_string(self, subdistricts):
        '''
            get only exact match : 0 => same
        :param subdistricts: list of subdistrict please reference this file
        :return:
        '''
        return list(filter(lambda x: x['score'] == 0, subdistricts))

    def suggest(self, subdistrict_name, city_name):
        """
            suggest subdistrict when user typo
        :param subdistrict_name:
        :param city_name:
        :return:
        """

        cities = self.get_sim_subdistrict(subdistrict_name, count=5)
        other_cities = self.check_if_extact_string(cities)
        if other_cities == []:
            result = self.get_sim_city(city_name, [city['subdistrict_code'] for city in cities], 1)
        else:
            result = self.get_sim_city(city_name, [city['subdistrict_code'] for city in other_cities], 1)
        return result
