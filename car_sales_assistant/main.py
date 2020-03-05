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
	

	# Cargamos el modelo
	
    loaded_model = pickle.load(open('svc_concessionaire_assistant_model.sav', 'rb'))
    
    if request.method == 'POST':
        buying = int(request.form['buying'])

        maint = int(request.form['maint'])

        doors = int(request.form['doors'])

        persons = int(request.form['persons'])

        lug_boot = int(request.form['lug_boot'])

        safety = int(request.form['safety'])

    data = {'buying':[buying], 
            'maint':[maint],
            'doors':[doors],
            'persons':[persons],
            'lug_boot':[lug_boot],
            'safety':[safety]}

    given_data = pd.DataFrame(data=data)

    dict_buying=  {"Bajo":1, "Medio":2, "Alto":3,"Muy Alto":4}
    dict_maint= {"Bajo":1,  "Medio":2,  "Alto":3,  "Muy Alto":4}
    dict_doors= {"2":2, "3":3,  "4":4, "5 o más":5}
    dict_persons= {"2":2, "3":3, "4 o más":6}
    dict_lug_boot= {"Pequeño":1, "Medio":2,  "Grande":3}
    dict_safety= { "Baja":1, "Media":2,  "Alta":3}
    

    # Generamos la predicción
    my_prediction = loaded_model.predict(given_data) 

    given_data['buying'].map(dict_buying) 
    given_data['maint'].map(dict_maint)
    given_data['doors'].map(dict_doors)
    given_data['persons'].map(dict_persons)
    given_data['lug_boot'].map(dict_lug_boot) 
    given_data['safety'].map(dict_safety) 


    given_data.apply(pd.to_numeric)
    # print("mapped dataframe")
    # print(given_data)
    

    #invertimos diccionarios
    inv_dict_buying = {v: k for k, v in dict_buying.items()}
    inv_dict_maint = {v: k for k, v in dict_maint.items()}
    inv_dict_doors = {v: k for k, v in dict_doors.items()}
    inv_dict_persons = {v: k for k, v in dict_persons.items()}
    inv_dict_lug_boot = {v: k for k, v in dict_lug_boot.items()}
    inv_dict_safety = {v: k for k, v in dict_safety.items()}

    #usamos los diccionarios invertidos para deshacer el mapeo
    given_data['buying'] = given_data['buying'].map(inv_dict_buying) 
    given_data['maint'] = given_data['maint'].map(inv_dict_maint) 
    given_data['lug_boot'] = given_data['lug_boot'].map(inv_dict_lug_boot) 
    given_data['safety'] = given_data['safety'].map(inv_dict_safety) 

    print("inverted dataframe")
    print(given_data)

    data_es = {
        'buying'  : "Precio",
        'maint'   : "Mantenimiento",
        'doors'   : "Número de puertas",
        'persons' : "Número de plazas",
        'lug_boot': "Capacidad maletero",
        'safety'  : "Seguridad"
    }

    if my_prediction == 'acc' :
        my_prediction = 'success'
    else:
        my_prediction = 'danger'

    return render_template('results.html',prediction = my_prediction, data = given_data, nombreCol = data_es)

    # Especificamos ruta y puerto
if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8080,debug=True)