from flask import Flask, escape, request,make_response
from io import BytesIO
from PIL import Image
from qrc import QRC

app = Flask(__name__)

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
    qr = QRC(icon=Image.open('Elogo.png'))
    if request.query_string:
        if '/' in path:
            # 链接
            bg = qr(request.full_path[1:])
        elif path == '':
            # 空名
            bg=qr(request.query_string)
        else:
            bg = qr(request.query_string,path)
    else:
        bg = qr(path)
    return tmp_qrcode(bg)

if __name__=='__main__':
    app.run()