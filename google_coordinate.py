# google基于WGS-84坐标系,但在国内是使用GCJ-02坐标系
import requests
import re


def store_data(item, result, precise):
    item['locate_addr'] = result['formatted_address']
    item['precise'] = precise
    item['lat'] = result['geometry']['location']['lat']
    item['lng'] = result['geometry']['location']['lng']


def get_coordinate(address):
    pattern = re.compile(r'\d+')
    door_num = pattern.findall(address)
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = dict(address=address, key='AIzaSyCqqcCYWYsNPjxgne900z5CGMmO0FF7iIM', language='zh')
    response = requests.get(url, params=params)
    item = {}
    for result in response.json()['results']:
        print(result)
        # types : subpremise premise street_number route 准确性降序
        types_1th = result['address_components'][0]['types'][0]
        types_2sd = result['address_components'][1]['types'][0]
        first_kw = result['address_components'][0]['long_name']
        second_kw = result['address_components'][1]['long_name']
        location_type = result['geometry']['location_type']
        if types_1th == 'subpremise':
            if first_kw in address:
                if location_type == 'ROOFTOP':
                    store_data(item, result, 10)
                # 这种可能性是否存在？
                elif location_type == 'GEOMETRIC_CENTER':
                    store_data(item, result, 9)
            elif types_2sd == 'street_number':
                if door_num:
                    if second_kw in door_num:
                        if location_type == 'ROOFTOP':
                            store_data(item, result, 9)
                        elif location_type == 'GEOMETRIC_CENTER':
                            store_data(item, result, 8)
                    elif location_type == 'ROOFTOP':
                        store_data(item, result, 6)
                    elif location_type == 'GEOMETRIC_CENTER':
                        store_data(item, result, 5)
                elif second_kw in address:
                    if location_type == 'ROOFTOP':
                        store_data(item, result, 9)
                    elif location_type == 'GEOMETRIC_CENTER':
                        store_data(item, result, 8)
                elif location_type == 'ROOFTOP':
                    store_data(item, result, 6)
                elif location_type == 'GEOMETRIC_CENTER':
                    store_data(item, result, 5)
            elif location_type == 'ROOFTOP':
                store_data(item, result, 8)
            elif location_type == 'GEOMETRIC_CENTER':
                store_data(item, result, 7)
        elif types_1th == 'premise':
            if first_kw in address:
                if location_type == 'ROOFTOP':
                    store_data(item, result, 9)
                elif location_type == 'GEOMETRIC_CENTER':
                    store_data(item, result, 8)
            elif location_type == 'ROOFTOP':
                store_data(item, result, 7)
            elif location_type == 'GEOMETRIC_CENTER':
                store_data(item, result, 6)
        elif types_1th == 'street_number':
            if door_num:
                if first_kw in door_num:
                    if location_type == 'ROOFTOP':
                        store_data(item, result, 9)
                    elif location_type == 'GEOMETRIC_CENTER':
                        store_data(item, result, 8)
                elif location_type == 'ROOFTOP':
                    store_data(item, result, 6)
                elif location_type == 'GEOMETRIC_CENTER':
                    store_data(item, result, 5)
            elif first_kw in address:
                if location_type == 'ROOFTOP':
                    store_data(item, result, 9)
                elif location_type == 'GEOMETRIC_CENTER':
                    store_data(item, result, 8)
            elif types_2sd == 'route':
                if second_kw in address:
                    if location_type == 'ROOFTOP':
                        store_data(item, result, 7)
                    elif location_type == 'GEOMETRIC_CENTER':
                        store_data(item, result, 6)
                elif location_type == 'ROOFTOP':
                    store_data(item, result, 5)
                elif location_type == 'GEOMETRIC_CENTER':
                    store_data(item, result, 4)
            elif location_type == 'ROOFTOP':
                store_data(item, result, 5)
            elif location_type == 'GEOMETRIC_CENTER':
                store_data(item, result, 4)
        elif types_1th == 'route':
            if first_kw in address:
                if location_type == 'ROOFTOP':
                    store_data(item, result, 7)
                elif location_type == 'GEOMETRIC_CENTER':
                    store_data(item, result, 6)
            elif location_type == 'ROOFTOP':
                store_data(item, result, 5)
            elif location_type == 'GEOMETRIC_CENTER':
                store_data(item, result, 4)
        elif location_type == 'GEOMETRIC_CENTER':
            store_data(item, result, 2)
        elif location_type == 'ROOFTOP':
            store_data(item, result, 4)
        else:
            store_data(item, result, 0)
    return item


