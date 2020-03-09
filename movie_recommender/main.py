# importación de paquetes
from flask import Flask,render_template,request
# Importamos las librerias necesarias
import jinja2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
import pickle
from sklearn.cluster import KMeans
from random import randrange


N_PELIS = 10
kmeans = pickle.load(open('kmeans.sav', 'rb'))
movies = pd.read_excel(r'data/movies_min.xlsx')
movies = movies.drop(['user'], axis=1)

# =============================================================================
# 1. Carga el modelo de clustering
# 2. Agrupa los usuarios en clusters (clustered_users) usando las votaciones de cada a las peliculas 
# 3. Concatena a cada usuario/fila el grupo al que pertenece ese usuario
# =============================================================================
def inicializar(movies):
     #Cargar modelo y clusterizar usuarios
    #kmeans = pickle.load(open('kmeans.sav', 'rb'))
    predictions  = kmeans.predict(movies.fillna(0)) # Esto nos devuelve, para cada usuario, el grupo al que pertenece
    #Concatenar el grupo de cada usuario al dataset inicial.
    clustered_users = pd.concat([movies.reset_index(), pd.DataFrame({'group':predictions})], axis=1)
    return clustered_users    

# =============================================================================
# # Seleccionar 'n' peliculas aleatoriamente del dataset 'movies'
#    Devuelve: Una lista con los nombres de las peliculas. Esta lista se renderizara en el HTML
# =============================================================================
def selectRandomMovies(movies, n):
    max_pelis = movies.shape[1]
    lista_pelis = []
    for i in range(n):
        random_column = randrange(max_pelis) # num aleatorio entre 0 y max_pelis
        lista_pelis.append(movies.iloc[:,random_column].name) # seleccionar columna
    return lista_pelis


# =============================================================================
# A partir de una lista de votaciones y una lista de pelis (deben ser del mismo tamanio),
# determina el grupo al que pertenece el usuario segun sus votaciones y 
# devuelve una lista de peliculas que no ha visto
# =============================================================================
def recomendarPeli(lista_votaciones, lista_pelis, clustered_users):
    #Crear lista de pelis con votaciones vacias para ir rellenandola con la 'lsta_votaciones'
    votaciones_usuario = pd.DataFrame(columns = movies.columns).append(pd.Series(name='ToPredict'))
    # Aniadir votaciones a la votacion vacia
    for i in range(len(lista_pelis)):
        votaciones_usuario.loc['ToPredict'][lista_pelis[i]] = lista_votaciones[i]
    '''
    los valores vacios que quedan (pelis que no ha votado/no ha visto) las rellenamos con
    el valor medio de las posibles votaciones -> 2.5, para que no impacte demasiado al hacer el predict
    '''
    votaciones_usuario = votaciones_usuario.fillna(2.5)
    
    '''
    hacemos el predict para que nos devuelva un grupo de usuarios al que pertenece nuestro usuario
    '''
    predicted_group = kmeans.predict(votaciones_usuario.iloc[0:1])
    # de todos los clusters, filtramos para quedarnos con el cluster de nuestro usuario
    cluster = clustered_users[clustered_users['group']==int(predicted_group)]
    #filtramos el cluster y nos quedamos solo con las pelis que no ha visto nuestro usuario
    pelis_no_vistas = cluster.loc[:, ~cluster.columns.isin(lista_pelis)]
    
    #Obtenemos la lista de peliculas, ordenadas de mayor a menor, segun la media de votaciones que ha obtenido en ese cluster
    recomendaciones = pelis_no_vistas.fillna(2.5).drop(['group'],axis=1).mean().sort_values(ascending=False).head(6)
    return list(recomendaciones.keys())
    

clustered_users = inicializar(movies)
lista_pelis = selectRandomMovies(movies, N_PELIS)
LISTA_PELIS = lista_pelis


app = Flask(__name__)

@app.route("/")
def index():
    '''Este metodo se ejecutara al cargar la vista principal.
    Inicializara el modelo y devolvera la lista de pelis para que las vote el usuario
    '''
    
    return render_template("index.html", pelis = LISTA_PELIS)

@app.route("/",methods=['POST'])
def recomendarPelis():
    '''Este metodo se ejecutara cuando el usuario envie el formulario con las votaciones
    '''
    
    if request.method == 'POST':
    #Obtener datos proporcionados por el usuario 
            
            data = []
            for i in range(0, 10):
                data.append(request.form['rating' + str(i)])
            
    
        
    recomendacion_pelis = recomendarPeli(data, LISTA_PELIS, clustered_users)  
    return render_template('resultado.html',resultado = recomendacion_pelis)
	


if __name__ == '__main__':
	app.run(host="127.0.0.1",port=8081,debug=True)