# importación de paquetes
from flask import Flask,render_template,request


import pandas as pd
import numpy as np


#Importamos librerías
from sklearn.svm import SVC
import pickle



app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/",methods=['POST'])
def predict():
	
    #  Machine Learning
	
	# Cargamos el clasificador
	
	loaded_model = pickle.load(open('clf_pokemon_model.sav', 'rb'))

	
	#Cogemos los datos proporcionados para predecir
	
	if request.method == 'POST':
		HP = request.form['HP']

		attack = request.form['attack']

		defense = request.form['defense']

		speed = request.form['speed']

		egg_group = request.form['egg_group']

		catch_rate = request.form['catch_rate']
		
		
		data = {'HP':[HP], 'attack':[attack],'defense':[defense],'speed':[speed], 'egg_group':[egg_group],'catch_rate':[catch_rate]} 
		given_data = pd.DataFrame(data) 
		given_data.apply(pd.to_numeric)

		print(given_data)

		my_prediction = loaded_model.predict(given_data) ##predecimos con el modelo
	return render_template('index.html',prediction = my_prediction)
	


if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8080,debug=True)