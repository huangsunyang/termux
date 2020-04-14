# -*- coding: utf-8 -*-
import sys
import requests
import json

headers = {
    "authority": "flights.ctrip.com:",
    "method": "POST",
    "path": "/itinerary/api/12808/products",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-length": "224",
    "content-type": "application/json",
    "origin": "https://flights.ctrip.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

payload = {
    "flightWay": "Oneway",
    "classType": "ALL",
    "hasChild": False,
    "hasBaby": False,
    "searchIndex": 1,
    "airportParams": [
        {
            "dcity": "SHA",
            "acity": "CKG",
            "date": "2011-04-19",
            # "dcityname": '上海',
            # "acityname": '重庆'
        }
    ]
}


class JsonObjectMeta(type):
    """
    return origin data if is basic type
    return JsonObject Wrapper if is list or dict
    """

    def __call__(self, *args, **kwargs):
        obj = args[0]
        if isinstance(obj, (tuple, list, dict)):
            return super(JsonObjectMeta, self).__call__(*args, **kwargs)
        return obj


class JsonObject(object):
    """
    simple wrapper for dict and list
    use . operator to visit dict content
    """
    __metaclass__ = JsonObjectMeta

    def __init__(self, json):
        self._json = json

    def __getattr__(self, item):
        return JsonObject(self._json[item])

    def __getitem__(self, item):
        return JsonObject(self._json[item])

    def __repr__(self):
        return repr(self._json)

    def generator(self):
        for each in self._json:
            yield JsonObject(each)
        raise StopIteration

    def __iter__(self):
        return self.generator()

    @classmethod
    def loads(cls, text):
        return JsonObject(json.loads(text))


class UnicodeWriter(object):
    """
    unicode wrapper for file writer
    originally unicode text written to file is not correct
    automatic encode to utf-8 for unicode type, and str() for other types
    """

    def __init__(self, file_name):
        self.file = open(file_name, 'w') if file_name else sys.stdout

    def write(self, *texts, **kwargs):
        sep = kwargs.get('sep', '')
        end = kwargs.get('end', '')
        for text in texts:
            text = text.encode('utf-8') if isinstance(text, unicode) else str(text)
            self.file.write(text)
            self.file.write(sep)
        self.file.write(end)


class PayloadFromatter(object):
    @classmethod
    def format(cls, depart_city, arrival_city, date):
        pay_load = payload.copy()
        pay_load['airportParams'] = [{
            "dcity": cls.city_tlc(depart_city) or 'HGH',
            "acity": cls.city_tlc(arrival_city) or 'CKG',
            "date": cls.date_format(date) or '2010-4-20',
        }]
        return pay_load

    @classmethod
    def dump(cls, *args):
        return json.dumps(cls.format(*args))

    @classmethod
    def city_tlc(cls, city_name):
        return city_name

    @classmethod
    def date_format(cls, date):
        return date


class DataArchiever(object):
    def __init__(self, depart_city, arrival_city, date, to_file=''):
        self.products_data = JsonObject.loads(
            requests.post(
                "https://flights.ctrip.com/itinerary/api/12808/products",
                headers=headers,
                data=PayloadFromatter.dump(depart_city, arrival_city, date)
            ).text
        )
        self.routes_data = self.products_data.data.routeList
        self.writer = UnicodeWriter(to_file)

    def parse(self):
        if not self.routes_data:
            self.writer.write('no data received')
            return
        for route in self.routes_data:
            leg = route.legs[0]
            flight = leg.flight
            cabins = leg.cabins
            characteristic = leg.characteristic
            self.writer.write(
                u'{}->{}'.format(
                    flight.departureAirportInfo.airportName,
                    flight.arrivalAirportInfo.airportName,
                ),
                flight.airlineName,
                flight.flightNumber,
                flight.departureDate,
                flight.arrivalDate,
                characteristic.lowestPrice,
                sep=' ', end='\n',
            )


if __name__ == '__main__':
    DataArchiever('SHA', 'CSX', None).parse()
