from db.neo4j_config import neo4j_connection

class LikeDislikeHandler:
    @staticmethod
    def handle_like(user_id):
        # Obtener el último perfil generado
        last_profile = LikeDislikeHandler.get_last_profile(user_id)
        if not last_profile:
            return False

        # Obtener gustos secundarios del último perfil generado
        gustos_secundarios = last_profile['IDs_de_gustos']

        # Sumar uno al contador de likes de los gustos secundarios del usuario
        with neo4j_connection.get_session() as session:
            for gusto_id in gustos_secundarios:
                session.run(
                    """
                    MATCH (g:Gusto {gusto_id: $gusto_id})
                    SET g.likes = COALESCE(g.likes, 0) + 1
                    """,
                    gusto_id=gusto_id
                )
        return True

    @staticmethod
    def handle_dislike(user_id):
        # Obtener el último perfil generado
        last_profile = LikeDislikeHandler.get_last_profile(user_id)
        if not last_profile:
            return False

        # Obtener gustos secundarios del último perfil generado
        gustos_secundarios = last_profile['IDs_de_gustos']
        print(gustos_secundarios)

        # Restar uno al contador de likes de los gustos secundarios del usuario
        with neo4j_connection.get_session() as session:
            for gusto_id in gustos_secundarios:
                session.run(
                    """
                    MATCH (g:Gusto {gusto_id: $gusto_id})
                    SET g.likes = COALESCE(g.likes, 0) - 1
                    """,
                    gusto_id=gusto_id
                )
        return True

    @staticmethod
    def get_last_profile(user_id):
        with neo4j_connection.get_session() as session:
            result = session.run(
                """
                MATCH (p:Perfil {user_id: $user_id})
                WITH p ORDER BY p.profile_id DESC
                RETURN p LIMIT 1
                """,
                user_id=user_id
            )
            record = result.single()
            if record:
                profile_node = record['p']
                profile_properties = dict(profile_node.items())
                return profile_properties

            print("No se encontró ningún perfil para el user_id:", user_id)
            return None

like_dislike_handler = LikeDislikeHandler()
