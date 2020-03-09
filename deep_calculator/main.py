# importación de paquetes
from flask import Flask,render_template,request


import pandas as pd
import numpy as np
import base64


#Importamos librerías

import tensorflow as tf ##pip install tensorflow
from tensorflow import keras
from PIL import Image
from numpy import *
import PIL.ImageOps
import numpy as np
import os
from io import BytesIO


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=['POST'])
def predict():
        print('holaaaa')
        print('predict')
    #  Machine Learning

    # Cargamos el clasificador


        model = tf.keras.models.load_model('model_mnist.sav') # importar modelo


	
	#Cogemos los datos proporcionados para predecir
	
    #if request.method == 'POST':
        print('hola')
        img = request.form.get("imagen1")
        img2 = request.form.get("imagen2")
        ope = int(request.form.get("operacion"))
        print(ope)
        print(img2)
        print(img)
        #f = open(img, 'r')
        #data = img.read()
        #img.closed

        im = Image.open(BytesIO(base64.b64decode(img)))
        
        im.save('imagen.png', 'PNG')
        
        im2 = Image.open(BytesIO(base64.b64decode(img2)))
        
        im2.save('imagen2.png', 'PNG')
        
        
        #imagen1 = 
        #print("imagen1")
        #with open("imagen.png", "wb") as fh:
         #   fh.write(base64.decodebytes(imagen1))

        # IMAGEN 1
        #path a la imagen
        temp=Image.open('./imagen.png')
        #invertimos la imagen
        temp = PIL.ImageOps.invert(temp.convert("RGB"))
        
        #cambiamos tamano
        temp = temp.resize((28,28))
        
        #pasamos a escala de grises
        temp=temp.convert('L') # 'L' -> grayscale
        #normalizamos los colores entre 0 y 1
        temp=asarray(temp)/255
        
        
        #hacemos la prediccion usando el modelo con predict
        pred = model.predict(temp.reshape(1,28,28))
        
        #cogemos el indice o posicion con mayor probabilidad
        pred = np.argmax(pred)
        
        # IMAGEN 2
        temp=Image.open('./imagen2.png')
        #invertimos la imagen
        temp = PIL.ImageOps.invert(temp.convert("RGB"))
        
        #cambiamos tamano
        temp = temp.resize((28,28))
        
        #pasamos a escala de grises
        temp=temp.convert('L') # 'L' -> grayscale
        #normalizamos los colores entre 0 y 1
        temp=asarray(temp)/255
        
       
        
        #hacemos la prediccion usando el modelo con predict
        prediction = model.predict(temp.reshape(1,28,28))
        pred2 = np.argmax(prediction)
        
        #Calculo de la operacion
        resultado = 0;
        print(type(ope))
        if ope == 1:
            print("AAAAAA")
            resultado = pred + pred2
        if ope == 2:
            resultado = pred - pred2
        if ope == 3:
            resultado = pred * pred2
        if ope == 4:
            resultado = pred / pred2
        
        
        
        print(pred2)
        print(pred)
        print(resultado)
        return render_template('results.html',resultado = resultado, num1 = pred, num2 = pred2)



if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8080,debug=True)# importación de paquetes