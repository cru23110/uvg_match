from src.recommendation_system.preferences_primary import PrimaryPreferences
from src.recommendation_system.recommendation_algorithm import RecommendationAlgorithm


def generate_new_profile(user_id):
    # Obtener las preferencias primarias del usuario
    primary_preferences = PrimaryPreferences().generate_profile(user_id)
    print("Caracteristicas primarias:", primary_preferences)

    # Generar el nuevo perfil
    # secondary_preferences = RecommendationAlgorithm().get_user_likes(user_id)
    # print("Caracteristicas secundarias:", secondary_preferences)

    # # Generar el nuevo perfil
    # secondary_preferences = RecommendationAlgorithm().get_random_user_likes()
    # print("random secundarias:", secondary_preferences)

    prueba = RecommendationAlgorithm().ordenar_gustos(user_id)
    print(prueba)
    return True