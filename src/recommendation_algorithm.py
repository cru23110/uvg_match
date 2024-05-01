from db.neo4j.neo4j_config import neo4j_connection

class ContentBasedRecommendation:
    def __init__(self):
        self.profiles = self.get_profiles_from_database()
        self.preferences = self.get_preferences_from_database()

    def get_profiles_from_database(self):
        with neo4j_connection.get_session() as session:
            result = session.run("MATCH (p:Perfil) RETURN p")
            profiles = [record["p"] for record in result]
        return profiles

    def get_preferences_from_database(self):
        with neo4j_connection.get_session() as session:
            result = session.run("MATCH (u:Usuario)-[:LE_GUSTA]->(g:Gusto) RETURN u, g")
            preferences = [{"user_id": record["u"]["id_usuario"], "preference": record["g"]["nombre"]} for record in result]
        return preferences

    def generate_recommendations(self, user_id):
        user_preferences = self.get_user_preferences(user_id)
        recommendations = {}
        for profile in self.profiles:
            similarity = self.calculate_similarity(user_preferences, profile['preferences'])
            recommendations[profile['id_perfil']] = similarity
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return sorted_recommendations

    def get_user_preferences(self, user_id):
        user_preferences = []
        for preference in self.preferences:
            if preference['user_id'] == user_id:
                user_preferences.append(preference['preference'])
        return user_preferences

    def calculate_similarity(self, preferences1, preferences2):
        intersection = set(preferences1) & set(preferences2)
        similarity = len(intersection) / (len(preferences1) * len(preferences2))
        return similarity