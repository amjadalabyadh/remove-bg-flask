from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 ميجا

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return "لا يوجد صورة"

    image_file = request.files['image']
    if image_file.filename == '':
        return "اختر صورة"

    input_data = image_file.read()
    output_data = remove(input_data)

    # فتح الصورة الناتجة وتحويلها إلى خلفية بيضاء
    no_bg_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
    white_bg = Image.new("RGB", no_bg_image.size, (255, 255, 255))
    white_bg.paste(no_bg_image, mask=no_bg_image.split()[3])  # استخدام الشفافية كـ mask

    # حفظ الصورة في الذاكرة
    img_io = io.BytesIO()
    white_bg.save(img_io, format='PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='white_bg.png')
app = Flask(__name__)

@app.route("/")
def home():
    return "هلا والله! موقعي شغال على Render ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
