from flask import Flask, render_template, request, session, redirect
import cv2
import os
from main import recog

# from label_image import load_graph

app = Flask(__name__)
filename = 'upload'

# glaph = load_graph('retrained_graph.pb')

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    img = request.files.get('pic')
    typefile = img.filename.split('.')[-1]
    img.save(os.path.join(filename + '.' + typefile))
    text, output_file = recog(filename + '.' + typefile)
    print(os.path.join(output_file))
    return render_template("result.html", result_image = os.path.join(output_file), result_text = text)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)