from flask import Flask, request, send_file, render_template_string
from PIL import Image
import io, os, zipfile, webbrowser, sys

app = Flask(__name__)

def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容PyInstaller打包和源码运行"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

@app.route('/')
def index():
    html_path = resource_path('givedyy/all-to-jpg-helper.html')
    return render_template_string(open(html_path, encoding='utf-8').read())

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('images')
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for file in files:
            try:
                img = Image.open(file.stream)
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                else:
                    img = img.convert('RGB')
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='JPEG', quality=90)
                img_bytes.seek(0)
                new_name = os.path.splitext(file.filename)[0] + '.jpg'
                zf.writestr(new_name, img_bytes.read())
            except Exception as e:
                continue
    mem_zip.seek(0)
    return send_file(mem_zip, mimetype='application/zip', as_attachment=True, download_name='jpg_images.zip')

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run()