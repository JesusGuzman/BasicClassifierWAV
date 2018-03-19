from flask import Flask, render_template, json, request
from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import ast
import soundfile as sf
import shutil

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/classify')
def showClassify():
    return render_template('classify.html')

@app.route('/admin')
def showAdmin():
    return render_template('admin.html')

@app.route('/delete', methods=['GET'])
def delete_folders():
    os.system('rm -rf ./records/*')
    return "OK", 200

@app.route('/train', methods=['GET'])
def train_model():
    # MANDAMOS A LLAMAR A LA BILIOTECA CON LOS DIRECTORIOS
    #os.system('bash ./cnn/run_train.sh')
    return "OK", 200

@app.route('/upload_images', methods=['POST'] )
def test3():
  imgs = request.files
  name = request.form['inputName']
  name_folder = name+"/"
  data = dict(imgs)
  datas = data['file[]']
  create_folder = "mkdir ./records/"+name_folder
  os.system(create_folder)
  n = 1
  for key in datas:
    data, samplerate = sf.read(key)
    pwd = name+str(n)+".wav"
    org = "./"+pwd
    dst = "./records/"+name_folder
    sf.write(str(pwd), data, samplerate)
    shutil.copy2(str(org), str(dst))
    n=n+1

  os.system('rm ./*.wav')
  return "OK", 201

@app.route('/upload_image', methods=['POST'])
def new_image():
  img = Image.open(request.files['inputFile'])
  img.save("./cnn/final.jpg")
  os.system('bash ./cnn/run_cnn.sh')
  data  = get_results_classify()
  score = str(data['score']*100)
  name = data['Dog']
  pwd = './cnn/training_dataset/'+name+'/'+name+'1.jpg'
  print_image(pwd,score)
    
  ##############
  return "OK", 201

def print_image(pwd, prob):
  image = Image.open(pwd)
  draw = ImageDraw.Draw(image)
  font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf", 60)
  draw.text((50, 50), prob, font=font, fill="white")
  image.show()


def get_results_classify():
  file_results = open("./cnn/results_classify.txt", "r")
  contenido = file_results.read()
  array = ast.literal_eval(contenido)
  return array[0]

if __name__ == "__main__":
    app.run(port=5002)
