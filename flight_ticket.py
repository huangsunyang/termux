# -*- coding: utf-8 -*-

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
#"cookie": 'DomesticUserHostCity=HGH|%ba%bc%d6%dd; _abtest_userid=e300feb9-d437-4066-91a6-307d0a5dc7e3; _RSG=P.4y5CKmTGA2sRAk0kNQe9; _RDG=28cb5d7496f13525bc0a66be5737ce73a5; _RGUID=a41dc143-05f0-4f99-9a1a-5ee02e29bd82; _ga=GA1.2.1609504349.1546684021; _gcl_dc=GCL.1546684021.CJmp1Pu21t8CFcLZvAodHGQD4Q; MKT_Pagesource=PC; Union=SID=155952&AllianceID=4897&OUID=baidu81|index|||; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; gad_city=78a2062d1790b42fa1a75f591a7869b2; _RF1=220.184.99.104; _gid=GA1.2.191128210.1546965319; traceExt=campaign=CHNbaidu81&adid=index; StartCity_Pkg=PkgStartCity=2; appFloatCnt=2; FD_SearchHistorty={"type":"S","data":"S%24%u676D%u5DDE%28HGH%29%24HGH%242019-01-25%24%u91CD%u5E86%28CKG%29%24CKG"}; _bfa=1.1546684018278.12esyf.1.1546684018278.1546965316310.2.12; _bfs=1.11; MKT_OrderClick=ASID=48971520899&CT=1546965879006&CURL=https%3A%2F%2Fflights.ctrip.com%2Fitinerary%2Foneway%2Fhgh-ckg%3Fdate%3D2019-01-26&VAL={"pc_vid":"1546684018278.12esyf"}; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1546965879008%7D%5D; _jzqco=%7C%7C%7C%7C1546965319470%7C1.555693439.1546684021103.1546965871880.1546965879024.1546965871880.1546965879024.undefined.0.0.11.11; __zpspc=9.2.1546965319.1546965879.10%231%7Cbaidu%7Ccpc%7Cbaidu81%7C%25E6%2590%25BA%25E7%25A8%258B%25E5%25AE%2598%25E7%25BD%2591%25E9%25A6%2596%25E9%25A1%25B5%7C%23; _bfi=p1%3D10320673302%26p2%3D10320673302%26v1%3D12%26v2%3D11',
"origin": "https://flights.ctrip.com",
"referer": "https://flights.ctrip.com/itinerary/oneway/hgh-ckg?date=2019-04-19",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}


payload = {"flightWay":"Oneway","classType":"ALL","hasChild":False,"hasBaby":False,"searchIndex":1,"airportParams":[{"dcity":"HGH","acity":"CKG","date":"2019-04-19","dcityid":17,"acityid":4}]}
res = requests.post("https://flights.ctrip.com/itinerary/api/12808/products", headers=headers, data=json.dumps(payload))

a = json.loads(res.text)[u'data'][u'routeList']
print a
