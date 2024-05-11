from src.recommendation_system.preferences_primary import PrimaryPreferences, obtener_nombre

def generate_new_profile(user_id):
    # Obtener las preferencias primarias del usuario
    primary_preferences = PrimaryPreferences().get_primary_preferences(user_id)
    print("Preferencias primarias del usuario:", primary_preferences)

    # Obtener el género del usuario
    genero = primary_preferences.get('Preferencia de género')

    # Generar el nombre de usuario basado en el género
    print(genero)
    if genero:
        nombre_usuario = obtener_nombre(genero)
        if nombre_usuario:
            print("Nombre de usuario generado:", nombre_usuario)
            # Lógica para generar el nuevo perfil...
            # Devolver True si el proceso fue exitoso
            return True
        else:
            print("No se pudo obtener el nombre de usuario.")
            return False
    else:
        print("No se pudo obtener la preferencia de género del usuario.")
        return False
    
    # Devolver True si el proceso fue exitoso
    return True
