# recommendation_algorithm.py

def generate_profile(user_preferences):
    """
    Genera un perfil de usuario basado en sus preferencias.
    
    Args:
        user_preferences (dict): Diccionario con las preferencias del usuario.
            Ejemplo: {'gustos': ['deporte', 'música'], 'disgustos': ['política']}
    
    Returns:
        dict: Perfil generado con características aleatorias y las preferencias del usuario.
    """
    # Aquí puedes implementar la lógica para generar un perfil de usuario
    # combinando las preferencias del usuario con otras características aleatorias.
    # Por ejemplo, podrías seleccionar intereses aleatorios de una lista predefinida
    # y combinarlos con los gustos y disgustos del usuario.
    
    # En este ejemplo simple, simplemente agregamos algunas características aleatorias
    # junto con las preferencias del usuario para formar el perfil.
    profile = {
        'nombre': 'Perfil Generado',
        'edad': 25,
        'genero': 'masculino',
        'intereses': ['deporte', 'música', 'viajes']
    }
    
    return profile

def update_preferences(user_preferences, profile_feedback):
    """
    Actualiza las preferencias del usuario basadas en el feedback del perfil.
    
    Args:
        user_preferences (dict): Diccionario con las preferencias del usuario.
            Ejemplo: {'gustos': ['deporte', 'música'], 'disgustos': ['política']}
        profile_feedback (str): Feedback del usuario sobre el perfil recomendado ('like' o 'dislike').
    
    Returns:
        dict: Preferencias actualizadas del usuario.
    """
    # Actualiza las preferencias del usuario según el feedback del perfil.
    # Por ejemplo, si el usuario indicó que le gustó el perfil, se pueden agregar
    # las características del perfil a la lista de gustos del usuario.
    if profile_feedback == 'like':
        for interest in profile_feedback['intereses']:
            if interest not in user_preferences['gustos']:
                user_preferences['gustos'].append(interest)
    elif profile_feedback == 'dislike':
        # Aquí podrías implementar la lógica para manejar los disgustos del usuario
        pass
    
    return user_preferences
