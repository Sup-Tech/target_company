# 整理筛选结果可视化数据
import sqlite3


def get_datas():
    conn = sqlite3.connect('target_company.db')
    c = conn.cursor()

    sql = 'select possible, note, raw_id, map_id from final_datas;'
    # possible|note|raw_id|map_id [(x,x,x,x),(...),...]
    final_datas = c.execute(sql).fetchall()
    # [{coordinate:[lat,lng], company_name:, company_addr:, locate_addr:, precise:, possible:, note:},{}]
    jar = []
    for final_data in final_datas:
        datas = {}
        datas['possible'] = final_data[0]
        datas['note'] = final_data[1]
        sql = 'select company_id from raw_datas where id={};'.format(final_data[2])
        company_id = c.execute(sql).fetchone()
        try:
            sql = 'select company_name, company_address from companies where id={};'.format(company_id[0])
        except TypeError:
            print('数据缺失，可能是公司条目不存在, raw_id=', final_data[2])
            continue
        else:
            datas['company_name'], datas['company_addr'] = c.execute(sql).fetchone()
        sql = 'select * from map_datas where id={}'.format(final_data[3])
        map_data = c.execute(sql).fetchone()
        try:
            datas['locate_addr'] = map_data[1]
            datas['coordinate'] = [map_data[2], map_data[3]]
            datas['precise'] = map_data[4]
        except TypeError:
            print('数据缺失，可能是map条目不存在, map_id=', final_data[3])
            continue
        else:
            jar.append(datas)
    return jar


def get_plotly_datas():
    conn = sqlite3.connect('target_company.db')
    c = conn.cursor()

    sql = 'select possible, note, raw_id, map_id from final_datas;'
    # possible|note|raw_id|map_id [(x,x,x,x),(...),...]
    final_datas = c.execute(sql).fetchall()
    # [{coordinate:[lat,lng], company_name:, company_addr:, locate_addr:, precise:, possible:, note:},{}]
    jar = {}
    text = []
    lat_list = []
    lng_list = []
    opacity = []
    for final_data in final_datas:
        possible = final_data[0]
        note = final_data[1]
        sql = 'select company_id from raw_datas where id={};'.format(final_data[2])
        company_id = c.execute(sql).fetchone()
        try:
            sql = 'select company_name, company_address from companies where id={};'.format(company_id[0])
        except TypeError:
            print('数据缺失，可能是公司条目不存在, raw_id=', final_data[2])
            continue
        else:
            company_name, company_addr = c.execute(sql).fetchone()
        sql = 'select * from map_datas where id={}'.format(final_data[3])
        map_data = c.execute(sql).fetchone()
        try:
            locate_addr = map_data[1]
            lat, lng = map_data[2], map_data[3]
            precise = map_data[4]
        except TypeError:
            print('数据缺失，可能是map条目不存在, map_id=', final_data[3])
            continue
        else:
            tmp = '公司: {}<br>可能性: {}<br>备注: {}<br>定位可信度: {}<br>定位: {}<br>公司地址：{}'.format(
                company_name, possible, note, precise, locate_addr, company_addr)
            text.append(tmp)
            lat_list.append(lat)
            lng_list.append(lng)
            opacity.append(possible/100)
    jar['text'] = text
    jar['lats'] = lat_list
    jar['lngs'] = lng_list
    jar['opacity'] = opacity
    return jar
