from aip import AipOcr

"""
OCR 识别58的公司联系人手机号
图片格式是gif
识别失败
百度 腾讯 都不支持gif格式
通过截图 来转换图片格式可能可以解决"""
""" 你的 APPID AK SK """
APP_ID = '19305797'
API_KEY = 'PBoStMF9pLMfqYgKElAKeOm7'
SECRET_KEY = 'v4s9CEV3Rf4dXcepU2xUcPEQBqwi8Or9'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

url = "/Users/Zuban/Desktop/showphone.jpg"
""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content(url)

""" 调用通用文字识别, 图片参数为本地图片 """
result = client.basicGeneral(image)
print(result)

# 调用失败