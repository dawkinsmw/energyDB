ZONE_KEY_TO_REGION = {
    'AUS-NSW': 'NSW1',
    'AUS-QLD': 'QLD1',
    'AUS-SA': 'SA1',
    'AUS-TAS': 'TAS1',
    'AUS-VIC': 'VIC1',
    'AUS-WA': 'WEM',
}
REGION_LONG_NAMES = {
    'NSW1':"New South Wales",
    'QLD1':"Queensland",
    'SA1':"South Australia",
    'TAS1':"Tasmania",
    'VIC1':"Victoria",
    'WEM':"Western Australia",
}
ZONE_KEY_TO_NETWORK = {
    'AUS-NSW': 'NEM',
    'AUS-QLD': 'NEM',
    'AUS-SA': 'NEM',
    'AUS-TAS': 'NEM',
    'AUS-VIC': 'NEM',
    'AUS-WA': 'WEM',
}
NETWORK_LONG_NAMES = {
    'NEM': 'National Energy Market',
    'WEM': 'Wholesale Electricity Market'
}
EXCHANGE_MAPPING_DICTIONARY = {
    'AUS-NSW->AUS-QLD': {
        'region_id': 'NSW1->QLD1',
        'direction': 1,
    },
    'AUS-NSW->AUS-VIC': {
        'region_id': 'NSW1->VIC1',
        'direction': 1,
    },
    'AUS-SA->AUS-VIC': {
        'region_id': 'SA1->VIC1',
        'direction': 1,
    },
    'AUS-TAS->AUS-VIC': {
        'region_id': 'TAS1->VIC1',
        'direction': 1,
    },
}
OPENNEM_PRODUCTION_CATEGORIES = {
    'coal': ['COAL_BLACK', 'COAL_BROWN'],
    'gas': ['GAS_CCGT', 'GAS_OCGT', 'GAS_RECIP', 'GAS_STEAM'],
    'oil': ['DISTILLATE'],
    'hydro': ['HYDRO'],
    'wind': ['WIND'],
    'biomass': ['BIOENERGY_BIOGAS', 'BIOENERGY_BIOMASS'],
    'solar': ['SOLAR_UTILITY', 'SOLAR_ROOFTOP'],
}
OPENNEM_STORAGE_CATEGORIES = {
    'battery': ['BATTERY_DISCHARGING', 'BATTERY_CHARGING'],
    'hydro': ['PUMPS'],
}
SOURCE = 'opennem.org.au'