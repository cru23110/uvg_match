import random
import requests
from bs4 import BeautifulSoup
from db.neo4j_config import neo4j_connection

class PrimaryPreferences:
    def __init__(self):
        pass

    def get_primary_preferences(self, user_id):
        primary_preferences = {}
        with neo4j_connection.get_session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id_usuario: $user_id})-[:TIENE_PREFERENCIA_PRINCIPAL]->(pp:PreferenciaPrincipal)
                RETURN pp
                """,
                user_id=user_id
            )
            for record in result:
                pp_node = record["pp"]
                nombre = pp_node["nombre"]
                valor = pp_node["valor"]
                # Mapear nombres de preferencias a nombres más descriptivos
                preference_name = self.map_preference_name(nombre)
                
                primary_preferences[preference_name] = valor
        return primary_preferences
    
    def map_preference_name(self, nombre):
        # Mapear nombres de preferencias a nombres más descriptivos
        mapping = {
            'gender_preference': 'Preferencia de género',
            'edad_minima': 'Edad mínima',
            'edad_maxima': 'Edad máxima',
            'distancia_minima': 'Distancia mínima',
            'distancia_maxima': 'Distancia máxima',
            'altura_minima': 'Altura mínima',
            'altura_maxima': 'Altura máxima',
            'religion': 'Religión',
            'other_religion': 'Otra religión',
            'relationship_status': 'Estado civil',
            'intereses': 'Intereses',
            'relationship_type': 'Tipo de relación',
            'other_relationship': 'Otro tipo de relación',
            'smoker_preference': 'Preferencia de fumador',
            'drinker_preference': 'Preferencia de bebedor',
            'education_level': 'Nivel educativo'
        }
        return mapping.get(nombre, nombre)

    def obtener_nombre(self, genero):
        if genero.lower() == 'hombres':
            url = "https://generadordenombres.online/hombre/"
        elif genero.lower() == 'mujeres':
            url = "https://generadordenombres.online/mujer/"
        else:
            print("Género no válido.")
            return None

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            nombre = soup.find('span', class_='svelte-6735sq').text
            return nombre
        else:
            print("Error al obtener la página:", response.status_code)
            return None

    def generate_profile(self, user_id):
        new_profile = {}

        primary_preferences = PrimaryPreferences().get_primary_preferences(user_id)
        # print(primary_preferences)
        
        # Generar nombre de usuario basado en el género
        genero = primary_preferences.get('Preferencia de género')
        if genero:
            new_profile['Nombre'] = self.obtener_nombre(genero)
        else:
            new_profile['Nombre'] = None

        # Asignar género del nuevo perfil
        new_profile['Género'] = 'Mujer' if genero == 'mujeres' else 'Hombre'

        # Generar valores aleatorios para edad, altura y distancia dentro de los rangos dados
        new_profile['Edad'] = random.randint(int(primary_preferences.get('Edad mínima')), int(primary_preferences.get('Edad máxima')))
        new_profile['Altura'] = random.randint(int(primary_preferences.get('Altura mínima')), int(primary_preferences.get('Altura máxima')))
        new_profile['Distancia'] = random.randint(int(primary_preferences.get('Distancia mínima')), int(primary_preferences.get('Distancia máxima')))

        # Obtener intereses y elegir dos al azar
        intereses_usuario = primary_preferences.get('Intereses', [])
        if intereses_usuario:
            intereses_elegidos = random.sample(intereses_usuario, min(len(intereses_usuario), 2))
            new_profile['Intereses'] = intereses_elegidos
        else:
            new_profile['Intereses'] = []

        # Asignar religión y otro tipo de religión según lo especificado
        religion = primary_preferences.get('Religión')
        other_religion = primary_preferences.get('Otra religión')
        if religion == 'otro':
            new_profile['Religión'] = other_religion
        else:
            new_profile['Religión'] = religion

        # Asignar tipo de relación según lo especificado
        relationship_type = primary_preferences.get('Tipo de relación')
        other_relationship = primary_preferences.get('Otro tipo de relación')
        if relationship_type == 'otras':
            new_profile['Tipo de relación'] = other_relationship
        else:
            new_profile['Tipo de relación'] = relationship_type

        # Asignar estado civil
        estado_civil = primary_preferences.get('Estado civil')
        if estado_civil:
            if genero == 'mujeres':
                if 'a' in estado_civil:
                    estado_civil = estado_civil[:-2]
            else:
                if 'a' not in estado_civil:
                    estado_civil += 'o'
            new_profile['Estado civil'] = estado_civil
        else:
            new_profile['Estado civil'] = None

        # Asignar preferencia de fumador y bebedor
        new_profile['Preferencia de fumador'] = 'No fumador' if primary_preferences.get('Preferencia de fumador') == 'no' else 'Fumador'
        new_profile['Preferencia de bebedor'] = 'No bebedor' if primary_preferences.get('Preferencia de bebedor') == 'no' else 'Bebedor'

        # Asignar nivel educativo
        new_profile['Nivel educativo'] = primary_preferences.get('Nivel educativo')

        return new_profile