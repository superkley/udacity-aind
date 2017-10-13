import base64
from io import BytesIO
from flask import Blueprint, jsonify, render_template, request

from backend.blueprints.look_alike_dog.ai import predict_breed

blueprint = Blueprint('look_alike_dog', __name__, static_folder='../../static')


@blueprint.route('/look_alike_dog')
def look_alike_dog():
    return render_template('index.html')


@blueprint.route('/')
def index():
    return render_template('index.html')


@blueprint.route('/process_img', methods=['POST'])
def process_img():
    data = request.get_json()
    img_src = data['imgSrc']
    b64str = img_src.partition(',')[2]
    binary_jpeg = base64.b64decode(b64str)
    img_file = BytesIO(binary_jpeg)
    return jsonify({'breed': predict_breed(img_file)})
