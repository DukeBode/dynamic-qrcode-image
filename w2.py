from flask import Flask, escape, request,make_response
from io import BytesIO
import qrcode
from PIL import Image,ImageDraw,ImageFont

app = Flask(__name__)

# 生成二维码
def generate_qrcode(content,logo=False,name=False):
    img = qrcode.make(content)
    img = img.convert("RGBA")
    wImg,hImg=img.size
    if logo:
        # 获取比例调整大小
        tmp=max(img.size)*0.3/max(logo.size)
        wLogo,hLogo = logo.size
        wLogo = int(wLogo*tmp)
        hLogo = int(hLogo*tmp)
        logo = logo.resize((wLogo,hLogo),Image.ANTIALIAS)

        # 确定位置
        p = (wImg-wLogo)//2,(hImg-hLogo)//2
        logo = logo.convert('RGBA')
        img.paste(logo,p,logo)

    if not name: return img
    # 设置字体及大小
    font_size=int(hImg*0.07)
    font = ImageFont.truetype("msyh.ttc", font_size)
    (font_x,font_y)=font.getsize(name)

    # 为图片建立背景
    bg = Image.new('RGB', (wImg,hImg+20+font_y), color=(255,255,255))
    bg.paste(img,(0,0))

    draw = ImageDraw.Draw(bg)
    draw.text((wImg/2-font_x/2,hImg-10), name,(0,0,0), font=font)
    return bg

# 保存至内存，返回 response
def tmp_qrcode(code):
    stream = BytesIO()
    code.save(stream,'PNG')
    response=make_response(stream.getvalue())
    response.headers['Content-Type']='image/png'
    return response

@app.route('/')
@app.route('/<path:path>')
def hello(path=''):
    if request.query_string:
        if '/' in path:
            # 链接
            bg=generate_qrcode(request.full_path[1:])
        elif path == '':
            # 空名
            bg=generate_qrcode(request.query_string)
        else:
            bg=generate_qrcode(request.query_string,path)
    else:
        bg=generate_qrcode(path,logo=Image.open('Elogo.png'))
    return tmp_qrcode(bg)

if __name__=='__main__':
    app.run()