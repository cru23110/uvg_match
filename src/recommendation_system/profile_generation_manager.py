from src.recommendation_system.preferences_primary import PrimaryPreferences
from src.recommendation_system.recommendation_algorithm import GustosCombiner

def generate_new_profile(user_id):
    # Obtener las preferencias primarias del usuario
    primary_preferences = PrimaryPreferences().generate_profile(user_id)
    gustos, puntuacion_perfil = GustosCombiner().obtener_gustos_combinados(user_id)

    # Organizar gustos por categoría
    categorias_gustos = {}
    for gusto in gustos:
        categoria = gusto['clase']
        if categoria not in categorias_gustos:
            categorias_gustos[categoria] = []
        categorias_gustos[categoria].append(gusto['nombre'])

    # Obtener solo los IDs de los gustos
    ids_gustos = [gusto['gusto_id'] for gusto in gustos]

    # Generar la descripción (aquí puedes implementar tu lógica de generación de descripción)
    descripcion = generate_description(primary_preferences['Nombre'], primary_preferences['Género'], primary_preferences['Edad'], primary_preferences['Intereses'], primary_preferences['Tipo de relación'])

    # Construir el diccionario del perfil completo
    nuevo_perfil = {
        'user_id': user_id,
        'profile_id': 'ID_del_perfil_generado',
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
        'Gustos': categorias_gustos,
        'IDs de gustos': ids_gustos,
        'Puntuacion del perfil': puntuacion_perfil,
        'Path de la imagen': '/path/to/image'
    }

    print(nuevo_perfil)
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