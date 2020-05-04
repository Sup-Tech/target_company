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
