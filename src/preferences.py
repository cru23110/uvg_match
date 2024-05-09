from db.neo4j.neo4j_config import neo4j_connection

class PreferencesDB:
    def __init__(self):
        pass

    def save_preferences(self, user_id, gender_preference, min_age, max_age, min_distance, max_distance,
                         min_height, max_height, religion, relationship_status, interests,
                         relationship_type, smoker_preference, drinker_preference, education_level):
        # Guardar las preferencias en la base de datos
        with neo4j_connection.get_session() as session:
            session.run(
                """
                MERGE (u:Usuario {id_usuario: $user_id})
                SET u.genero_preferido = $gender_preference,
                    u.edad_minima = $min_age,
                    u.edad_maxima = $max_age,
                    u.distancia_minima = $min_distance,
                    u.distancia_maxima = $max_distance,
                    u.altura_minima = $min_height,
                    u.altura_maxima = $max_height,
                    u.religion = $religion,
                    u.estado_civil = $relationship_status,
                    u.intereses = $interests,
                    u.tipo_relacion_buscada = $relationship_type,
                    u.fumador = $smoker_preference,
                    u.bebedor = $drinker_preference,
                    u.nivel_educativo = $education_level
                """,
                user_id=user_id,
                gender_preference=gender_preference,
                min_age=min_age,
                max_age=max_age,
                min_distance=min_distance,
                max_distance=max_distance,
                min_height=min_height,
                max_height=max_height,
                religion=religion,
                relationship_status=relationship_status,
                interests=interests,
                relationship_type=relationship_type,
                smoker_preference=smoker_preference,
                drinker_preference=drinker_preference,
                education_level=education_level
            )
