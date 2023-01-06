from PIL import Image
from urllib.request import urlretrieve

# 图片的地址

def 图片格式转换(img_url,目标格式):
    imgn = img_url.split('.')[len(img_url.split('.'))-1]
    if('cn/gchatpic_new/' in imgn):
        urlretrieve(img_url, f'hmbb01.png')    # 两个参数，一个是图片地址；一个是图片名
        im = Image.open(f"hmbb01.png")
    else:
        urlretrieve(img_url, f'hmbb01.{imgn}')    # 两个参数，一个是图片地址；一个是图片名
        im = Image.open(f"hmbb01.{imgn}")
    #此时返回一个新的image对象，转换图片模式
    image=im.convert('RGB')
    #调用save()保存
    image.save(r'D:\xampp\htdocs\img\c.biancheng.net.'+目标格式)
    return r'D:\xampp\htdocs\img\c.biancheng.net.'+目标格式
#print(图片格式转换('https://gchat.qpic.cn/gchatpic_new/3192145045/870133394-2506389624-9EE43732BFF0958BE24E5CEE43132659/0?term','webp'))