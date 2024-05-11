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
                print(user_id,nombre,valor)
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

def obtener_nombre(genero):
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
