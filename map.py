import folium
import plotly.graph_objects as go
import plotly.io as io

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


def save_plotly_map(datas, mapCenter='杭州'):
    """
    用plotly创建并保存地图为html文件
    :param datas: 所有要可视化的数据
                  格式为 [{coordinate:[lat,lng], company_name:, company_addr:, locate_addr:, precise:, possible:, note:}, {}]
                  {'possible': , 'note': '', 'company_name': '', 'company_addr': '', 'locate_addr': '', 'coordinate': [,], 'precise': }
    :param mapCenter: 地图中心
    :return: 无
    """
    map_center = {'杭州': [30.251356678317297, 120.20484924316406]}
    mapbox_access_token = 'pk.eyJ1IjoianViYW4iLCJhIjoiY2s5YWV2eG95MXFvdDNkbzU5MTFzeDFzYSJ9.yBVm0jEmZGDhhZvt3C8eUQ'
    fig = go.Figure(go.Scattermapbox(
            lat=datas['lats'],
            lon=datas['lngs'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9,
                color=datas['opacity'],
                colorscale=[[0, '#F6AEA7'], [1, '#FF0000']]
            ),
            text=datas['text'],
            hoverinfo='text',
            hoverlabel=dict(bgcolor='#EBE7E8', font=dict(color='#44524E'))
        ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=map_center[mapCenter][0],
                lon=map_center[mapCenter][1]
            ),
            style='mapbox://styles/juban/ck9af90m802p61iqs71jb3y7g',
            pitch=0,
            zoom=10
        ),
    )

    fig.show()
