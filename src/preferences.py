from db.neo4j_config import neo4j_connection

class PreferencesDB:
    def __init__(self):
        pass

    def save_preferences(self, user_id, gender_preference, edad_minima, edad_maxima, distancia_minima, distancia_maxima,
                         altura_minima, altura_maxima, religion, other_religion, relationship_status, intereses,
                         relationship_type, other_relationship, smoker_preference, drinker_preference, education_level):
        preferences = [
            {'tipo': 'Genero', 'nombre': 'gender_preference', 'valor': gender_preference},
            {'tipo': 'Edad', 'nombre': 'edad_minima', 'valor': edad_minima},
            {'tipo': 'Edad', 'nombre': 'edad_maxima', 'valor': edad_maxima},
            {'tipo': 'Distancia', 'nombre': 'distancia_minima', 'valor': distancia_minima},
            {'tipo': 'Distancia', 'nombre': 'distancia_maxima', 'valor': distancia_maxima},
            {'tipo': 'Altura', 'nombre': 'altura_minima', 'valor': altura_minima},
            {'tipo': 'Altura', 'nombre': 'altura_maxima', 'valor': altura_maxima},
            {'tipo': 'Religion', 'nombre': 'religion', 'valor': religion},
            {'tipo': 'Otra Religion', 'nombre': 'other_religion', 'valor': other_religion},
            {'tipo': 'Estado Civil', 'nombre': 'relationship_status', 'valor': relationship_status},
            {'tipo': 'Otra Relacion', 'nombre': 'other_relationship', 'valor': other_relationship},
            {'tipo': 'Intereses', 'nombre': 'intereses', 'valor': intereses},
            {'tipo': 'Tipo de Relacion', 'nombre': 'relationship_type', 'valor': relationship_type},
            {'tipo': 'Fumador', 'nombre': 'smoker_preference', 'valor': smoker_preference},
            {'tipo': 'Bebedor', 'nombre': 'drinker_preference', 'valor': drinker_preference},
            {'tipo': 'Nivel Educativo', 'nombre': 'education_level', 'valor': education_level}
        ]

        # print("preferences:", preferences)

        with neo4j_connection.get_session() as session:
            for preference in preferences:
                # Verificar si el valor no es nulo
                if preference['valor'] is not None:
                    session.run(
                        """
                        MATCH (u:Usuario {id_usuario: $user_id})
                        MERGE (u)-[:TIENE_PREFERENCIA_PRINCIPAL {tipo: $tipo}]->(pp:PreferenciaPrincipal {nombre: $nombre, valor: $valor})
                        """,
                        user_id=user_id,
                        tipo=preference['tipo'],
                        nombre=preference['nombre'],
                        valor=preference['valor']
                    )

