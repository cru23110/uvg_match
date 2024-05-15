from flask import json
from src.recommendation_system.preferences_primary import PrimaryPreferences
from src.recommendation_system.recommendation_algorithm import GustosCombiner
from db.neo4j_config import neo4j_connection

def generate_new_profile(user_id):
    # Generar el perfil completo
    primary_preferences = PrimaryPreferences().generate_profile(user_id)
    gustos, puntuacion_perfil = GustosCombiner().obtener_gustos_combinados(user_id)

    # Reemplazar los guiones bajos por espacios en las cadenas del diccionario
    for key, value in primary_preferences.items():
        if isinstance(value, str):
            primary_preferences[key] = value.replace('_', ' ')

    # Organizar gustos por categoría
    categorias_gustos = {}
    for gusto in gustos:
        categoria = gusto['clase']
        if categoria not in categorias_gustos:
            categorias_gustos[categoria] = []
        categorias_gustos[categoria].append(gusto['nombre'])

    # Convertir el diccionario de categorías a una cadena JSON
    gustos_json = json.dumps(categorias_gustos)

    # Deserializar la cadena JSON a un diccionario
    # gustos_dict = json.loads(gustos_json)

    # Imprimir el diccionario para verificar su contenido
    # print(gustos_dict)

    # Obtener solo los IDs de los gustos
    ids_gustos = [gusto['gusto_id'] for gusto in gustos]

    # Generar la descripción
    descripcion = generate_description(
        primary_preferences['Nombre'],
        primary_preferences['Género'],
        primary_preferences['Edad'],
        primary_preferences['Intereses'],
        primary_preferences['Tipo de relación']
    )

    # Obtener el máximo profile_id actual y calcular el nuevo
    max_profile_id = get_max_profile_id()
    new_profile_id = max_profile_id + 1

    # Construir el diccionario del perfil completo
    nuevo_perfil = {
        'user_id': user_id,
        'profile_id': new_profile_id,
        'Nombre': primary_preferences['Nombre'],
        'Descripcion': descripcion,
        'Genero': primary_preferences['Género'],
        'Edad': primary_preferences['Edad'],
        'Altura': primary_preferences['Altura'],
        'Distancia': primary_preferences['Distancia'],
        'Intereses': primary_preferences['Intereses'],
        'Religion': primary_preferences['Religión'],
        'Tipo de relacion que busca': primary_preferences['Tipo de relación'],
        'Estado civil': primary_preferences['Estado civil'],
        'Preferencia de fumador': primary_preferences['Preferencia de fumador'],
        'Preferencia de bebedor': primary_preferences['Preferencia de bebedor'],
        'Nivel educativo': primary_preferences['Nivel educativo'],
        'Gustos': gustos_json,
        'IDs de gustos': ids_gustos,
        'Puntuacion del perfil': puntuacion_perfil,
        'Path de la imagen': '/path/to/image'  # Reemplaza con el path real
    }
    print(nuevo_perfil)
    # Guardar el perfil en la base de datos
    save_new_profile(nuevo_perfil, user_id)

    return True

def generate_description(nombre, genero, edad, intereses, tipo_relacion):
    # Construir la descripción basada en las características proporcionadas
    descripcion = f"¡Hola! Soy {nombre}, "
    if genero == "Hombre":
        descripcion += "un hombre "
    elif genero == "Mujer":
        descripcion += "una mujer "
    else:
        descripcion += "una persona "

    descripcion += f"de {edad} años que disfruta de "
    if len(intereses) == 1:
        descripcion += f"{intereses[0]}. "
    elif len(intereses) == 2:
        descripcion += f"{intereses[0]} y {intereses[1]}. "
    else:
        descripcion += ', '.join(intereses[:-1]) + f" y {intereses[-1]}. "

    descripcion += f"Busco {tipo_relacion}."

    return descripcion

def get_max_profile_id():
    with neo4j_connection.get_session() as session:
        result = session.run(
            """
            MATCH (p:Perfil)
            RETURN MAX(p.profile_id) AS max_profile_id
            """
        )
        record = result.single()
        max_profile_id = record["max_profile_id"] if record["max_profile_id"] is not None else 0
    return max_profile_id

def save_new_profile(nuevo_perfil, user_id):
    with neo4j_connection.get_session() as session:
        session.run(
            """
            MATCH (u:Usuario {id_usuario: $user_id})
            CREATE (p:Perfil {
                user_id: $user_id,
                profile_id: $profile_id,
                Nombre: $Nombre,
                Descripcion: $Descripcion,
                Genero: $Genero,
                Edad: $Edad,
                Altura: $Altura,
                Distancia: $Distancia,
                Intereses: $Intereses,
                Religion: $Religion,
                `Tipo de relacion que busca`: $Tipo_de_relacion,
                `Estado civil`: $Estado_civil,
                `Preferencia de fumador`: $Preferencia_de_fumador,
                `Preferencia de bebedor`: $Preferencia_de_bebedor,
                `Nivel educativo`: $Nivel_educativo,
                Gustos: $Gustos,
                IDs_de_gustos: $IDs_de_gustos,
                `Puntuacion del perfil`: $Puntuacion_del_perfil,
                `Path de la imagen`: $Path_de_la_imagen
            })
            CREATE (u)-[:TIENE_PERFIL]->(p)
            """,
            user_id=user_id,
            profile_id=nuevo_perfil['profile_id'],
            Nombre=nuevo_perfil['Nombre'],
            Descripcion=nuevo_perfil['Descripcion'],
            Genero=nuevo_perfil['Genero'],
            Edad=nuevo_perfil['Edad'],
            Altura=nuevo_perfil['Altura'],
            Distancia=nuevo_perfil['Distancia'],
            Intereses=nuevo_perfil['Intereses'],
            Religion=nuevo_perfil['Religion'],
            Tipo_de_relacion=nuevo_perfil['Tipo de relacion que busca'],
            Estado_civil=nuevo_perfil['Estado civil'],
            Preferencia_de_fumador=nuevo_perfil['Preferencia de fumador'],
            Preferencia_de_bebedor=nuevo_perfil['Preferencia de bebedor'],
            Nivel_educativo=nuevo_perfil['Nivel educativo'],
            Gustos=nuevo_perfil['Gustos'],
            IDs_de_gustos=nuevo_perfil['IDs de gustos'],
            Puntuacion_del_perfil=nuevo_perfil['Puntuacion del perfil'],
            Path_de_la_imagen=nuevo_perfil['Path de la imagen']
        )
    return True

