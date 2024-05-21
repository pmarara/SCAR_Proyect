import streamlit as st
import pandas as pd
import csv
import numpy as np
from scipy.stats import pearsonr

class User:
    def __init__(self, user_id, age, gender, occupation):
        self.user_id = user_id
        self.age = age
        self.gender = gender
        self.occupation = occupation

users_data = pd.read_csv("data/users.txt", sep='\t', names=['UserID', 'Age', 'Gender', 'Occupation'], encoding="utf-8")
users = {row['UserID']: User(row['UserID'], row['Age'], row['Gender'], row['Occupation']) for _, row in users_data.iterrows()}
user_id = len(users)+1

# Función para cargar tipos de usuario desde el archivo
def load_user_types(filepath):
    types = []
    with open(filepath, 'r', newline='') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            types.append({
                'tipo': row[0],
                'edad_min': int(row[1]),
                'edad_max': int(row[2]),
                'sexo': row[3].lower(),  # Asegurarse de que todo está en minúsculas para la comparación
                'profesion': row[4].lower()  # Asegurarse de que todo está en minúsculas para la comparación
            })
    return types

def calculate_new_user_neighbors(new_user_id, new_user_preferences):
    # Parámetros
    min_neighbors = 10
    max_neighbors = 30
    affinity_threshold = 0.85

    # Cargar los datos de VectoresColaborativos.txt
    data = pd.read_csv('data/VectoresColaborativos.txt', sep='\t', header=None)
    data.columns = ['UserID'] + [f'Genre_{i}' for i in range(1, 20)]

    # Obtener la lista de usuarios y las preferencias
    user_ids = data['UserID'].values
    preferences = data.iloc[:, 1:].values

    # Calcular el coeficiente de correlación de Pearson para el nuevo usuario
    new_user_neighbors = []
    
    for i, user_id in enumerate(user_ids):
        if user_id != new_user_id:
            other_user_pref = preferences[i]
            correlation, _ = pearsonr(new_user_preferences, other_user_pref)
            new_user_neighbors.append((user_id, correlation))
    
    # Ordenar los vecinos por afinidad (mayor correlación)
    new_user_neighbors.sort(key=lambda x: x[1], reverse=True)
    
    # Filtrar los vecinos según el umbral y el rango de número de vecinos
    filtered_neighbors = []
    for neighbor_id, correlation in new_user_neighbors:
        if len(filtered_neighbors) < min_neighbors or (len(filtered_neighbors) < max_neighbors and correlation >= affinity_threshold):
            filtered_neighbors.append((neighbor_id, correlation))
        else:
            break

    # Guardar los vecinos del nuevo usuario en el archivo Vecinos.txt
    with open('data/Vecinos.txt', 'a') as f:
        neighbors_str = '\t'.join([f"{neighbor_id}:{correlation:.4f}" for neighbor_id, correlation in filtered_neighbors])
        f.write(f"{new_user_id}\t{neighbors_str}\n")

def signupuser(id, age, sex, occupation, preferences):

    # Abrir el archivo en modo append
    with open("data/users.txt", "a") as file:
        file.write(f"\n{id}\t{age}\t{sex}\t{occupation}")
    
    # Calcular el tipo de usuario y agregarlo al archivo user_types_assigned.txt
    user_type = determine_user_type(age, sex.lower(), occupation.lower(), user_types)
    with open('data/user_types_assigned.txt', 'a', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow([id, user_type])

    # Cambiar 0 a 1 en preferences
    preferences_array = np.array(preferences)
    
    # Normalizar para que el máximo valor sea 100
    max_value = preferences_array.max()
    if max_value > 0:
        preferences_array = (preferences_array / max_value) * 100

    preferences_array = preferences_array.astype(int)
    preferences_array = np.where(preferences_array == 0, 1, preferences_array)

    # Guardar las preferencias en VectoresColaborativos.txt
    preferences_str = '\t'.join(map(str, preferences_array))
    with open('data/VectoresColaborativos.txt', 'a', newline='') as file:
        file.write(f"{id}\t{preferences_str}\n")

    # Guardar las preferencias en VectoresBasadosContenido.txt
    top_indices = preferences_array.argsort()[-6:][::-1]
    top_preferences = np.zeros(19)
    top_preferences[top_indices] = preferences_array[top_indices]
    preferences_str = '\t'.join(map(str, top_preferences.astype(int)))  # Convertir a enteros y luego a strings
    with open('data/VectoresBasadosContenido.txt', 'a', newline='') as file:
        file.write(f"{id}\t{preferences_str}\n")

    # Calcular vecinos del nuevo usuario
    calculate_new_user_neighbors(id, preferences_array)

    # Actualizar la lista de usuarios
    users_data = pd.read_csv("data/users.txt", sep='\t', names=['UserID', 'Age', 'Gender', 'Occupation'], encoding="utf-8")
    users = {row['UserID']: User(row['UserID'], row['Age'], row['Gender'], row['Occupation']) for _, row in users_data.iterrows()}
    user_id = len(users) + 1


# Profesiones agrupadas
professions = {
    'c': ['artist', 'writer', 'entertainment', 'educator', 'librarian'],
    'b': ['executive', 'administrator', 'salesman', 'marketing', 'lawyer'],
    'm': ['doctor', 'healthcare', 'scientist'],
    't': ['technician', 'programmer', 'engineer'],
    'o': ['student', 'none', 'other', 'homemaker', 'retired']
}

# Función para determinar el tipo de usuario
def determine_user_type(age, sex, profession, types):
    for type_info in types:
        # Verifica edad
        if type_info['edad_min'] <= age <= type_info['edad_max']:
            # Verifica sexo
            if type_info['sexo'] == 'x' or type_info['sexo'] == sex:
                # Verifica profesión
                if type_info['profesion'] == 'x' or profession in professions.get(type_info['profesion'], []):
                    return type_info['tipo']
    return 'No type found'

# Cargar tipos de usuario
user_types = load_user_types('data/user_types.txt')


st.title("Sign Up!")
 
st.number_input("ID", value=user_id, disabled=True)

age = st.slider("Age")

sex = st.selectbox("Sex", ["M", "F"])

occupation = st.selectbox("Occupation", ["none", "technician", "other", "writer", "executive", "administrator", "student", "lawyer", "educator", "scientist", "entertainment", "programmer", "librarian", "homemaker", "artist", "marketing", "healthcare", "retired", "salesman", "doctor"])

# Genre sliders
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("*Please let us know how much you like each of the following movie genres on a scale from 0 to 100*")
user_preferences = []
user_preferences.append(0)
user_preferences.append(st.slider("Action"))
user_preferences.append(st.slider("Adventure"))
user_preferences.append(st.slider("Animation"))
user_preferences.append(st.slider("Children's"))
user_preferences.append(st.slider("Comedy"))
user_preferences.append(st.slider("Crime"))
user_preferences.append(st.slider("Documentary"))
user_preferences.append(st.slider("Drama"))
user_preferences.append(st.slider("Fantasy"))
user_preferences.append(st.slider("Film-Noir"))
user_preferences.append(st.slider("Horror"))
user_preferences.append(st.slider("Musical"))
user_preferences.append(st.slider("Mystery"))
user_preferences.append(st.slider("Romance"))
user_preferences.append(st.slider("Sci-Fi"))
user_preferences.append(st.slider("Thriller"))
user_preferences.append(st.slider("War"))
user_preferences.append(st.slider("Western"))

if st.button("Sign up"):
    if np.any(np.array(user_preferences) != 0):
        signupuser(user_id, age, sex, occupation, user_preferences)
        st.success("User signed up successfully!")
    else:
        st.error("Please specify your movie preferences!")