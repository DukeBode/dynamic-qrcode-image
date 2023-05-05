# https://github.com/lincolnloop/python-qrcode
from qrcode import QRCode,constants
# https://pillow.readthedocs.io/
from PIL import Image,ImageDraw,ImageFont
from pyzbar.pyzbar import decode,ZBarSymbol
from zipfile import ZipFile
from io import BytesIO

class QRC:
    '''
    >>> qr = QRC()('content')
    >>> print(QRC.read(qr))
    content
    '''
    def __init__(self,border=4,box_size=10,color=(255,255,255),font='msyh.ttc',
        font_size=1,icon=False,icon_size=0.4,zip_name='',file_type='png',
        error_correction=constants.ERROR_CORRECT_M):
        # self.__d = locals()
        self.qr = QRCode(
            error_correction=error_correction,
            box_size=box_size,
            border=0
        )
        self.__icon = icon
        self.__code = None
        self.__icon_size = icon_size
        self.border = border*box_size
        self.__file_name = zip_name
        self.__file_type = file_type
        # self.__font = ImageFont.truetype(font, int(font_size*self.border))
    
    # 设置内容
    def content(self,content):
        self.qr.add_data(content)
        self.qr.make()
        self.__code = self.qr.make_image()
        self.__code = self.__code.convert("RGBA")
        self.__size = self.__code.size[0]

    # 设置图标
    def setIcon(self):
        w,h = self.__icon.size
        # 获取比例调整大小
        tmp=self.__size*self.__icon_size/max(w,h)
        w,h = int(w*tmp),int(h*tmp)
        icon = self.__icon.resize((w,h),Image.ANTIALIAS)
        # 确定位置
        p = (self.__size-w)//2,(self.__size-h)//2
        icon = icon.convert('RGBA')
        self.__code.paste(icon,p,icon)

    # 设置背景
    def background(self,size=0):
        length = self.__size + 2 * self.border
        bg_size = (length, length + size)
        bg = Image.new('RGB', bg_size, color=(255,255,255))
        bg.paste(self.__code, (self.border, self.border))
        return bg

    # 设置文字
    # def setFont(self,title):
    #     w, h = self.__font.getsize(title)
    #     bg = self.background(h)
    #     draw = ImageDraw.Draw(bg)
    #     p = (
    #         bg.size[0] // 2 - w // 2,
    #         bg.size[0] - self.border//2
    #     )
    #     draw.text(p, title,(0,0,0), font=self.__font)
    #     return bg
    
    # 生成二维码
    def __call__(self,content=False,font=False,icon=True):
        if content: self.content(content)
        elif self.__code is None: self.content('')
        if self.__icon and icon: self.setIcon()
        if font: return self.setFont(font)
        return self.background()
    
    # 生成zip压缩包
    def zip(self,name,**data):
        stream = BytesIO()
        name = f'{name}.{self.__file_type}'
        self(**data).save(stream,'PNG')
        with ZipFile(f'{self.__file_name}.zip', 'a') as myzip:
            myzip.writestr(name,stream.getvalue())
    
    # 读取二维码内容
    @staticmethod
    def read(code):
        data = decode(code,symbols=[ZBarSymbol.QRCODE])
        if len(data)>1:
            return len(data)
        return data[0].data.decode("utf-8")

if __name__=='__main__':
    import doctest
    doctest.testmod()