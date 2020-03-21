import os
import sys
import subprocess
import requests
import ssl
import random
import string
import json

from flask import jsonify
from flask import Flask
from flask import request
from flask import send_file
import traceback

from app_utils import blur
from app_utils import download
from app_utils import generate_random_filename
from app_utils import clean_me
from app_utils import clean_all
from app_utils import create_directory
from app_utils import get_model_bin
from app_utils import get_multi_model_bin

import shutil

from neural_style import render_single_image
from multiprocessing import Pool

try:  # Python 3.5+
    from http import HTTPStatus
except ImportError:
    try:  # Python 3
        from http import client as HTTPStatus
    except ImportError:  # Python 2
        import httplib as HTTPStatus


app = Flask(__name__)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Args:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


@app.route("/process", methods=["POST"])
def process():

    input_path = generate_random_filename(upload_directory,"jpg")
    output_path = generate_random_filename(upload_directory,"png")

    try:
        if 'file' in request.files:
            file = request.files['file']
            if allowed_file(file.filename):
                file.save(input_path)

            style = request.form.getlist('style')[0]

        else:
            url = request.json["url"]
            download(url, input_path)
            style = request.json["style"]


        img_output_dir, img_name = os.path.split(output_path)
        content_img_dir, content_img = os.path.split(input_path)
        args = Args(
                content_img=content_img,
                content_img_dir=content_img_dir,
                img_output_dir=img_output_dir,
                img_name=os.path.splitext(img_name)[0],
                style_imgs_dir="/src/styles/",
                style_imgs=[style+'.jpg'],
                max_size=1000,
                max_iterations=100,
                original_colors=False,
                device="/gpu:0",
                verbose=True,
                init_img_type='content',
                model_weights=weight_file,
                pooling_type='avg',
                style_mask=False,
                style_imgs_weights=[1.0],
                content_weight=5e0,
                style_weight=1e4,
                content_loss_function=1,
                content_layers=['conv4_2'],
                style_layers=['relu1_1', 'relu2_1', 'relu3_1', 'relu4_1', 'relu5_1'],
                style_mask_imgs=None,
                style_layer_weights=[0.2, 0.2, 0.2, 0.2, 0.2],
                content_layer_weights=[1.0],
                tv_weight=1e-3,
                temporal_weight=2e2,
                video=False,
                print_iterations=50,
                optimizer='lbfgs',
                color_convert_type='yuv'
                )
        #TF I hate the way you manage GPU memory !!!
        with Pool(1) as p:
          p.apply(render_single_image, (args,))

        callback = send_file(os.path.join(img_output_dir, args.img_name, img_name), mimetype='image/png')


        return callback, 200


    except:
        traceback.print_exc()
        return {'message': 'input error'}, 400

    finally:
        clean_all([
            input_path
            ])

        shutil.rmtree(os.path.join(img_output_dir, args.img_name))

if __name__ == '__main__':
    global upload_directory, weight_file
    global ALLOWED_EXTENSIONS
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    upload_directory = '/src/upload/'
    create_directory(upload_directory)

    weight_directory = '/src/'
    weight_file = 'imagenet-vgg-verydeep-19.mat'

    url_prefix = 'http://pretrained-models.auth-18b62333a540498882ff446ab602528b.storage.gra.cloud.ovh.net/image/neural-style-tf/'

    get_model_bin(url_prefix + weight_file , weight_directory + weight_file)

    port = 5000
    host = '0.0.0.0'

    app.run(host=host, port=port, threaded=True)

