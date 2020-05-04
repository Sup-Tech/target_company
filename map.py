import folium


def save_map(datas, mapCenter='杭州'):
    """
    创建并保存地图为html文件
    :param datas: 所有要可视化的数据
                  格式为 [{coordinate:[lat,lng], company_name:, company_addr:, locate_addr:, precise:, possible:, note:}, {}]
                  {'possible': , 'note': '', 'company_name': '', 'company_addr': '', 'locate_addr': '', 'coordinate': [,], 'precise': }
    :param mapCenter: 地图中心
    :return: 无
    """
    map_center = {'杭州': [30.251356678317297, 120.20484924316406]}
    # create map obj
    m = folium.Map(location=map_center[mapCenter], zoom_start=11)
    # [{coordinate:[lat,lng], company_name:, company_addr:, locate_addr:, precise:, possible:, note:},{}]
    # create custom marker icon
    # logoIcon = folium.features.CustomIcon('./img/QL_Icon.png', icon_size=(50, 50))
    # create markers
    for data in datas:
        # make popup tip
        print(data)
        popup_str = '<p>可能性: {}<br>备注: {}<br>定位可信度: {}<br>定位: {}<br>公司地址：{}</p>'.format(
            data['possible'], data['note'] if data['note'] else '无',
            data['precise'], data['locate_addr'], data['company_addr'])
        # create Marker
        folium.Marker(data['coordinate'],
                      popup=folium.Popup(popup_str,
                                         max_width=500),
                      tooltip=data['company_name']
                      ).add_to(m)

    m.save('map.html')
