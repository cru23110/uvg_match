from src.recommendation_system.preferences_primary import PrimaryPreferences
from src.recommendation_system.recommendation_algorithm import GustosCombiner


def generate_new_profile(user_id):
    # Obtener las preferencias primarias del usuario
    primary_preferences = PrimaryPreferences().generate_profile(user_id)
    print("Caracteristicas primarias:", primary_preferences)

    gustos = GustosCombiner().obtener_gustos_combinados(user_id)
    print("gustos finales:", gustos)
    return True