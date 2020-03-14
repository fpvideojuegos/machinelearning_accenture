# importacion de paquetes
#Flask renderiza imagenes
from flask import Flask,render_template,request


import pandas as pd
import numpy as np


#Importamos libreriass
from sklearn.svm import SVC
import pickle
# tenemos que importar la libreria de tensorflow para usar la funcion load_model()
import tensorflow as tf
#PIL para preprocesar la imagen
from PIL import Image
#PIL numpy para preprocesar la imagen
from numpy import*


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/",methods=['POST'])
def predict():
    
    #  Machine Learning

    # Cargamos el clasificador
    # aqui cargamos el modelo que hemos exportado antes, cuando hicimos el entrenamiento
    loaded_model = tf.keras.models.load_model('model_mnist.sav') # importar modelo
#    
    #Cogemos los datos del formulario proporcionados para predecir
    
    if request.method == 'POST':
        
#         cargamos la imagen del formulario
        print("Antes de coger el archivo del formulario")
        archivo = request.files['archivo']
    
#    ToDo: Aqui tenemos que incluir la logica de para preprocesar la imagen y clasificarla:
        
#         Preprocesamos la imagen
        img = Image.open(archivo)
        #28 x 28 pixeles
        img = img.resize((28,28))
        #Transformamos a escala de grises
        img=img.convert('L') # 'L' -> grayscale
        
        img= asarray(img)/255
              
        my_prediction = loaded_model.predict(img.reshape(1,28,28)) ##predecimos con el modelo
        pred = np.argmax(my_prediction)

        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

        #Mostramos el resultado de la prediccion
    
        predicted_class = class_names[pred]
        print(my_prediction)
        return render_template('results.html',prediction = predicted_class)
        
    

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8081,debug=True)