# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:12:58 2020

@author: Lopez
"""


from __future__ import absolute_import, division, print_function, unicode_literals

# TensorFlow y tf.keras
import tensorflow as tf
from tensorflow import keras

# Librerias de ayuda
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from numpy import* 

import pickle

print(tf.__version__)

# Cogemos el dataset de ropa

fashion_mnist = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# Definimos el nombre de la prenda conla posicion del array 

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images.shape

len(train_labels)

train_labels

test_images.shape

len(test_labels)

#Aqui pre-procesamos el set de datos , 

plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()

# Transformamos la imagen a blancos y negros

train_images = train_images / 255.0

test_images = test_images / 255.0

# Comprobamos que el set de datos esta bien y mostramos las 25 primeras imagenes

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

# Redimensionamos las imagenes a 28 x 28 pixeles

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
    # Aqui compilamos el modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
    
# Definimos cuantas veces queremos entrenar el modelo y lo entrenamos

model.fit(train_images, train_labels, epochs=10)
    
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

# Mostramos el nivel de acierto del entrenamiento

print('\nTest accuracy:', test_acc)

#Mostramos las predicciones

predictions = model.predict(test_images)
predictions[0]

#Esto define cual es el argumento con mas probabilidad de acierto,
# esto define que tipo de prenda cree que es

np.argmax(predictions[0])

test_labels[0]

#Aqui graficamos para ver el set de la prediccion  
  
def plot_image(i, predictions_array, true_label, img):
      predictions_array, true_label, img = predictions_array, true_label[i], img[i]
      plt.grid(False)
      plt.xticks([])
      plt.yticks([])

      plt.imshow(img, cmap=plt.cm.binary)

      predicted_label = np.argmax(predictions_array)
      if predicted_label == true_label:
          color = 'blue'
      else:
          color = 'red'

      plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)
    #############################
    # Aqui damos forma a la hora de mostrar los resltados al array

def plot_value_array(i, predictions_array, true_label):
      predictions_array, true_label = predictions_array, true_label[i]
      plt.grid(False)
      plt.xticks(range(10))
      plt.yticks([])
      thisplot = plt.bar(range(10), predictions_array, color="#777777")
      plt.ylim([0, 1])
      predicted_label = np.argmax(predictions_array)
      thisplot[predicted_label].set_color('red')
      thisplot[true_label].set_color('blue')
      i = 0
      plt.figure(figsize=(6,3))
      plt.subplot(1,2,1)
      plot_image(i, predictions[i], test_labels, test_images)
      plt.subplot(1,2,2)
      plot_value_array(i, predictions[i],  test_labels)
      plt.show()
      i = 12
      plt.figure(figsize=(6,3))
      plt.subplot(1,2,1)
      plot_image(i, predictions[i], test_labels, test_images)
      plt.subplot(1,2,2)
      plot_value_array(i, predictions[i],  test_labels)
      plt.show()
      num_rows = 5
      num_cols = 3
      num_images = num_rows*num_cols
      plt.figure(figsize=(2*2*num_cols, 2*num_rows))
      for i in range(num_images):
          plt.subplot(num_rows, 2*num_cols, 2*i+1)
          plot_image(i, predictions[i], test_labels, test_images)
          plt.subplot(num_rows, 2*num_cols, 2*i+2)
          plot_value_array(i, predictions[i], test_labels)
          plt.tight_layout()
          plt.show()
          
# Probamos el modelo entrenado

img = test_images[1]

print(img.shape)

img = (np.expand_dims(img,0))

print(img.shape)

img = (np.expand_dims(img,0))

print(img.shape)

img = (np.expand_dims(img,0))

predictions_single = model.predict(img)

print(predictions_single)

plot_value_array(1, predictions_single[0], test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)

np.argmax(predictions_single[0])

filename = 'ropa3.py'
pickle.dump(model, filename)