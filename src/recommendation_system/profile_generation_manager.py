from src.recommendation_system.preferences_primary import PrimaryPreferences

def generate_new_profile(user_id):
    primary_preferences = PrimaryPreferences()
    nuevo_perfil = primary_preferences.generate_profile(user_id)
    print(nuevo_perfil)
    # Devolver True si el proceso fue exitoso
    return True
