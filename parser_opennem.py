import dateutil.parser
from pandas import date_range

def parse_request_json(request_json):
    raw_data = request_json['data']
    for i in range(len(raw_data)):
        if(i < (len(raw_data)-1) ):
            assert(raw_data[i]['type']=='power')
        else:
            assert(raw_data[i]['type']=='price')

    ## META
    meta = {x:request_json[x] for x in request_json if x!='data'}

    ## PRICE
    price = {}
    price_raw = raw_data[len(raw_data)-1]

    #meta
    price['meta'] = {x:price_raw[x] for x in price_raw if x!='history'}
    price['meta']['start'] = price_raw['history']['start']
    price['meta']['last'] = price_raw['history']['last']
    price['meta']['interval'] = price_raw['history']['interval']

    #data
    price['data'] = [x for x in zip( date_range(
        start=dateutil.parser.parse(price_raw['history']['start']), 
        end=dateutil.parser.parse(price_raw['history']['last']), 
        periods=len(price_raw['history']['data'])
        ), 
        price_raw['history']['data'])
    ]

    ## POWER
    power = {}
    for i in range(len(raw_data)-1):
        raw_fueltech = raw_data[i]

        #meta
        fueltech_meta = {x:raw_fueltech[x] for x in raw_fueltech if x!='history'}
        fueltech_meta['start'] = raw_fueltech['history']['start']
        fueltech_meta['last'] = raw_fueltech['history']['last']
        fueltech_meta['interval'] = raw_fueltech['history']['interval']
        
        #data
        fueltech_data = [x for x in zip(date_range(
        start=dateutil.parser.parse(raw_fueltech['history']['start']), 
        end=dateutil.parser.parse(raw_fueltech['history']['last']), 
        periods=len(raw_fueltech['history']['data'])),
        raw_fueltech['history']['data'])]

        #append fueltech i to power dict 
        power[fueltech_meta['code']] = {"meta":fueltech_meta,"data":fueltech_data}

    return (meta,price,power)