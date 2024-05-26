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
        'Path de la imagen': ''
    }

    # Generar y guardar la imagen del perfil
    # image_path = generate_and_save_profile_image(user_id, new_profile_id, nuevo_perfil)
    # nuevo_perfil['Path de la imagen'] = image_path

    # Guardar el perfil en la base de datos
    save_new_profile(nuevo_perfil, user_id)

    # Incrementar el contador de veces utilizado para cada gusto
    increment_gusto_usage(ids_gustos, user_id)

    # Deserializar el JSON de 'Gustos'
    nuevo_perfil['Gustos'] = json.loads(nuevo_perfil['Gustos'])
    return nuevo_perfil

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

def increment_gusto_usage(ids_gustos, user_id):
    # Incrementar el contador de veces utilizado para cada gusto
    with neo4j_connection.get_session() as session:
        for gusto_id in ids_gustos:
            session.run(
                """
                MATCH (g:Gusto {gusto_id: $gusto_id})
                SET g.veces_utilizado = COALESCE(g.veces_utilizado, 0) + 1
                """,
                gusto_id=gusto_id
            )

# -------Generacion de imagen----------
def construct_image_prompt(nuevo_perfil):
    # Construir el prompt para la imagen basado en los datos del nuevo perfil
    prompt = f"Genera una imagen para {nuevo_perfil['Nombre']}"

    # Género
    if nuevo_perfil['Genero'] == "Hombre":
        prompt += " masculina"
    elif nuevo_perfil['Genero'] == "Mujer":
        prompt += " femenina"
    else:
        prompt += " persona"

    # Edad
    prompt += f" de {nuevo_perfil['Edad']} años"

    # Altura (opcional)
    if nuevo_perfil['Altura']:
        prompt += f" y {nuevo_perfil['Altura']} de altura"

    # Intereses (opcional)
    if nuevo_perfil['Intereses']:
        prompt += f", interesada en {', '.join(nuevo_perfil['Intereses'])}"

    # Finalizar el prompt
    prompt += "."
    
    return prompt

def generate_image_filename(user_id, profile_id):
    # Generar el nombre de archivo para la imagen
    return f"{user_id}s{profile_id}.png"

# def generate_and_save_image(prompt, filename):            #Esta comentado pues aun no se usara, usa demasiados recursos de la computadora que lo este corriendo, asi que aun no esta lista esta funcionalidad
#     # Configurar el modelo
#     model_id = "CompVis/stable-diffusion-v1-4"
#     device = "cuda" if torch.cuda.is_available() else "cpu"

#     # Cargar el pipeline de Stable Diffusion
#     pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
#     pipe = pipe.to(device)
#     pipe.enable_attention_slicing()

#     # Generar la imagen
#     image = pipe(prompt).images[0]

#     # Asegurarse de que el directorio de destino existe
#     output_dir = os.path.abspath("./static/img/profile_photo/")
#     os.makedirs(output_dir, exist_ok=True)

#     # Guardar la imagen en la ubicación deseada
#     image_path = os.path.join(output_dir, filename)
#     image.save(image_path)

#     return image_path

# def generate_and_save_profile_image(user_id, profile_id, nuevo_perfil):
#     # Construir el prompt para la imagen
#     prompt = construct_image_prompt(nuevo_perfil)

#     # Generar el nombre de archivo para la imagen
#     filename = generate_image_filename(user_id, profile_id)

#     # Generar y guardar la imagen
#     image_path = generate_and_save_image(prompt, filename)

#     # Retornar la ruta completa del archivo de imagen generado
#     return image_path