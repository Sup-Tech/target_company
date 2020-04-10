import requests
addr = '武义县百花山工业区桂花路66号'
# http://api.map.baidu.com/geocoding/v3/?address=北京市海淀区上地十街10号&output=json&ak=您的ak&callback=showLocation //GET请求
ak = 'ysZHXY6AwYQYcXLuhTCkV2a1YvOk5Dm2'
url = 'http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak={}'.format(addr, ak)
res = requests.get(url=url)
print(res)
# <Response [200]>
print(type(res.text))
print(res.json()['result'])
# {"status":0,"result":{"location":{"lng":119.8538979994067,"lat":28.973137670009696},"precise":1,"confidence":80,"comprehension":100,"level":"门址"}}
# requests 返回的数据格式
# {"status":0,"result":{
#       "location":{"lng":119.8538979994067,"lat":28.973137670009696},
#       "precise":1,
#       "confidence":80,
#       "comprehension":100,
#       "level":"门址"
#       }
#       }
"""
status
返回结果状态值， 成功返回0，其他值请查看下方返回码状态表。

location
经纬度坐标	
lat	纬度值	
lng	经度值

precise
位置的附加信息，是否精确查找。1为精确查找，即准确打点；0为不精确，即模糊打点。	

confidence
描述打点绝对精度（即坐标点的误差范围）。
confidence=100，解析误差绝对精度小于20m；
confidence≥90，解析误差绝对精度小于50m；
confidence≥80，解析误差绝对精度小于100m；
confidence≥75，解析误差绝对精度小于200m；
confidence≥70，解析误差绝对精度小于300m；
confidence≥60，解析误差绝对精度小于500m；
confidence≥50，解析误差绝对精度小于1000m；
confidence≥40，解析误差绝对精度小于2000m；
confidence≥30，解析误差绝对精度小于5000m；
confidence≥25，解析误差绝对精度小于8000m；
confidence≥20，解析误差绝对精度小于10000m；

comprehension	描述地址理解程度。分值范围0-100，分值越大，服务对地址理解程度越高（建议以该字段作为解析结果判断标准）；
当comprehension值为以下值时，对应的准确率如下：
comprehension=100，解析误差100m内概率为91%，误差500m内概率为96%；
comprehension≥90，解析误差100m内概率为89%，误差500m内概率为96%；
comprehension≥80，解析误差100m内概率为88%，误差500m内概率为95%；
comprehension≥70，解析误差100m内概率为84%，误差500m内概率为93%；
comprehension≥60，解析误差100m内概率为81%，误差500m内概率为91%；
comprehension≥50，解析误差100m内概率为79%，误差500m内概率为90%；
//解析误差：地理编码服务解析地址得到的坐标位置，与地址对应的真实位置间的距离。	

level
能精确理解的地址类型，包含：UNKNOWN、国家、省、城市、区县、乡镇、村庄、道路、地产小区、商务大厦、政府机构、交叉路口、商圈、生活服务、
休闲娱乐、餐饮、宾馆、购物、金融、教育、医疗 、工业园区 、旅游景点 、汽车服务、火车站、长途汽车站、桥 、停车场/停车区、港口/码头、收费区/收费站、
飞机场 、机场 、收费处/收费站 、加油站、绿地、门址	string
"""