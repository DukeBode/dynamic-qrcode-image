from flask import Flask, escape, request,make_response,redirect,render_template
from io import BytesIO
from PIL import Image
from .qrc import QRC
###############################
# from flask_wtf import FlaskForm
# from wtforms import StringField
# from wtforms.validators import DataRequired

# class MyForm(FlaskForm):
#     name = StringField('name', validators=[DataRequired()])

#################################
app = Flask(__name__)
# 保存至内存，返回 response
def tmp_qrcode(code):
    stream = BytesIO()
    code.save(stream,'PNG')
    response=make_response(stream.getvalue())
    response.headers['Content-Type']='image/png'
    return response

# @app.route('/',methods=('GET','POST'))
# def index():
#     if request.method=='POST':
#         pass
#     form = MyForm(csrf_enabled=False)
#     # if form.validate_on_submit():
#         # return redirect('/success')
#     return render_template('submit.html', form=form)
#     return request.headers.get('User-Agent')

# @app.route('/')
@app.route('/<path:path>')
def hello(path=''):
    qr = QRC()
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