from db.neo4j_config import neo4j_connection

class RecommendationAlgorithm:
    def __init__(self):
        pass

    def get_user_likes(self, user_id):
        user_likes = []
        with neo4j_connection.get_session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id_usuario: $user_id})-[:TIENE_GUSTO]->(gusto)
                RETURN gusto.gusto_id AS gusto_id, gusto.nombre AS nombre_gusto, gusto.clase AS clase_gusto, gusto.veces_utilizado AS veces_utilizado, gusto.likes AS likes
                """,
                user_id=user_id
            )
            for record in result:
                gusto_info = {
                    "gusto_id": record["gusto_id"],
                    "nombre": record["nombre_gusto"],
                    "clase": record["clase_gusto"],
                    "veces_utilizado": record["veces_utilizado"],
                    "likes": record["likes"]
                }
                user_likes.append(gusto_info)
        return user_likes
    
    def get_random_user_likes(self):
        random_user_likes = []
        with neo4j_connection.get_session() as session:
            result = session.run(
                """
                MATCH (u:Usuario)-[:TIENE_GUSTO]->(gusto)
                WITH u, COLLECT(gusto) AS gustos
                ORDER BY rand()
                LIMIT 1
                UNWIND gustos AS gusto
                RETURN gusto.gusto_id AS gusto_id, gusto.nombre AS nombre_gusto, gusto.clase AS clase_gusto, gusto.veces_utilizado AS veces_utilizado, gusto.likes AS likes
                """
            )
            for record in result:
                gusto_info = {
                    "gusto_id": record["gusto_id"],
                    "nombre": record["nombre_gusto"],
                    "clase": record["clase_gusto"],
                    "veces_utilizado": record["veces_utilizado"],
                    "likes": record["likes"]
                }
                random_user_likes.append(gusto_info)
        return random_user_likes

    