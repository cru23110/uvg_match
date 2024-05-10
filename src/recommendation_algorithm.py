from flask import Flask
from db.neo4j_config import neo4j_connection
import random

app = Flask(__name__)
app.secret_key = 'HjbRlkNgrFNkmws'

class ContentBasedRecommendation:
    def __init__(self):
        pass

    def recommend_profiles(self, user_id):
        # Obtener los gustos básicos del usuario desde la base de datos
        user_preferences = self.get_user_interests(user_id)

        # Generar un nuevo perfil basado en los gustos básicos del usuario
        new_profile = self.generate_profile(user_preferences)

        # Guardar el nuevo perfil en la base de datos de perfiles generados
        self.save_generated_profile(new_profile)

        return new_profile

    def get_user_interests(self, user_id):
        # Obtener los gustos básicos del usuario desde la base de datos Neo4j
        with neo4j_connection.get_session() as session:
            result = session.run("MATCH (u:Usuario {id_usuario: $user_id})-[:LE_GUSTA]->(g:Gusto) RETURN g.nombre AS nombre", user_id=user_id)
            user_interests = [record["nombre"] for record in result]
        return user_interests

    def generate_profile(self, user_interests):
        # Simulamos generar un perfil basado en los gustos básicos del usuario
        random_interests = self.generate_random_interests()
        new_profile = user_interests + random_interests
        return new_profile

    def generate_random_interests(self):
        # Simulamos generar algunas características aleatorias para el perfil
        random_interests = random.sample(["Interes1", "Interes2", "Interes3", "Interes4", "Interes5"], 3)
        return random_interests

    def save_generated_profile(self, new_profile):
    # Guardar el perfil generado en la base de datos de perfiles generados en Neo4j
        with neo4j_connection.get_session() as session:
            # Obtener el último ID de perfil
            result = session.run("MATCH (p:Perfil) RETURN max(p.id_perfil) AS last_id")
            last_id = result.single().get('last_id', 0)

            # Crear un nodo para representar el perfil con un ID único creciente
            new_id = last_id + 1
            session.run("CREATE (p:Perfil {id_perfil: $new_id, nombre: 'prueba', caracteristicas: $profile})", new_id=new_id, profile=new_profile)

# Crear una instancia del algoritmo de recomendación
recommendation_system = ContentBasedRecommendation()