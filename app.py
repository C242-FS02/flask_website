import os
from flask import Flask, request, render_template, send_from_directory
from model.sam_model import SAMModel
import matplotlib.pyplot as plt
from PIL import Image
import rasterio
import base64
import numpy as np
import io


def save_image_as_png(image, output_png_path):
    # Convert image to PNG
    pil_image = Image.fromarray(image)
    pil_image.save(output_png_path, format="PNG")
    return output_png_path

app = Flask(__name__)

# Inisialisasi model SAM
checkpoint_path = "models/sam_vit_b_01ec64.pth"
sam_model = SAMModel(checkpoint_path)

@app.route('/sign-up.html')
def sign_up():
    return render_template('sign-up.html')

@app.route('/sign-in.html')
def sign_in():
    return render_template('sign-in.html')

@app.route('/segmentation.html')
def segmentation():
    return render_template('segmentation.html')


@app.route('/about-us.html')
def about_us():
    return render_template('about-us.html')

# Halaman utama dan upload form
@app.route('/index.html')
def index_route():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')    

# Route untuk menerima gambar dan memprosesnya
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No file part", 400
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    
    if file and (file.filename.endswith('.tif') or file.filename.endswith('.tiff')):
        filename = os.path.join('static/images', file.filename)
        file.save(filename)
    
        # Segmentasi gambar menggunakan model SAM
        masks = sam_model.segment_image(filename)
        
        # Mendapatkan latitude dan longitude dari titik tengah gambar
        image = sam_model.read_multiband_tiff(filename)
        print(image)
        row, col = image.shape[0] // 2, image.shape[1] // 2
        lat, lon = sam_model.get_lat_lon(filename, row, col)

        # Menyimpan hasil segmentasi
        result_image_path = os.path.join('static/results', f"segmented_{file.filename}")
        plt.imshow(masks[0], alpha=0.5, cmap='viridis')
        plt.savefig(result_image_path)
        
        # Mengganti nama file ke PNG
        base_name = os.path.splitext(file.filename)[0]
        output_png_path_original = os.path.join('static/jpg', f"{base_name}.png")
        save_image_as_png(image, output_png_path_original)
        output_png_path_original = os.path.join('static/jpg', f"segmented_{base_name}.png")        
        save_image_as_png(masks[0], output_png_path_original)
        
        # rmg_jpg = convert_tif_to_jpeg(f'static/results/segmented_{file.filename}', f'static/jpg/segmented_{file.filename}')        
        return render_template('segmentation_results.html', original_image=f'static/jpg/{base_name}.png', result_image=f'static/jpg/segmented_{base_name}.png', latitude=lat, longitude=lon)
    return "Invalid file format", 400

# Menyajikan gambar statis
@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
