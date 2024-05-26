"""
Aplicación Flask para Sistema de Recomendaciones

Esta aplicación Flask proporciona una interfaz de usuario para un sistema de recomendaciones,
permitiendo a los usuarios generar nuevos perfiles, dar like o dislike a recomendaciones, guardar preferencias,
y registrar/iniciar sesión/cerrar sesión.

Autores: [Juan Cruz, Nadissa Vela, Lingna Chen]
"""

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from src.recommendation_system.profile_generation_manager import generate_new_profile
from src.recommendation_system.recommendation_algorithm import SimilarUserFinder, UserLikesProcessor
from src.authentication import authenticate_user, get_user_id, get_username_by_id, obtener_nuevo_gusto_id, obtener_ultimo_user_id, register_user, save_gusto
from src.preferences import PreferencesDB
from src.like_dislike_handler import like_dislike_handler

app = Flask(__name__)

app.secret_key = 'HjbRlkNgrFNkmws'

# Crear una instancia de manejo de preferencias de usuario
preferences_db = PreferencesDB()

# Ruta para la página principal
@app.route('/')
def index():
    """Ruta principal para la página de inicio."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    current_user = get_username_by_id(user_id)
    nuevo_perfil = generate_new_profile(user_id)

    return render_template('index.html', current_user=current_user, nuevo_perfil=nuevo_perfil)

# Ruta para manejar acciones de like/dislike
@app.route('/handle_like_dislike', methods=['POST'])
def handle_like_dislike():
    """Maneja las acciones de like/dislike."""
    data = request.get_json()
    action = data.get('action')
    
    user_id = session.get('user_id')
    if user_id:
        success = False
        if action == 'like':
            success = like_dislike_handler.handle_like(user_id)
        elif action == 'dislike':
            success = like_dislike_handler.handle_dislike(user_id)
        
        if success:
            return jsonify(success=True, redirect_url=url_for('index'))
        else:
            return jsonify(success=False)
    else:
        return jsonify(success=False, message="Usuario no autenticado")

# Ruta para la versión Pro (pro_version.html)
@app.route('/pro_version')
def pro_version():
    """Ruta para la versión Pro de la aplicación."""
    user_id = session.get('user_id')
    current_user = get_username_by_id(user_id)
    nuevo_perfil = generate_new_profile(user_id)
    
    return render_template('pro_version.html', current_user=current_user, nuevo_perfil=nuevo_perfil)

# Ruta para generar un nuevo perfil
@app.route('/generate_new_profile')
def generate_new_profile_route():
    """Ruta para generar un nuevo perfil de usuario."""
    user_id = session.get('user_id')
    if user_id:
        result = generate_new_profile(user_id)
        if result:
            return "Nuevo perfil generado exitosamente"
        else:
            return "Error al generar el nuevo perfil"
    else:
        return "Usuario no autenticado"

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta para la página de inicio de sesión."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if authenticate_user(username, password):
            user_id = get_user_id(username, password)
            session['user_id'] = user_id
            return redirect(url_for('index'))

    return render_template('login.html')

# Ruta para la página de registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para la página de registro de usuarios."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username.strip() or not password.strip():
            return redirect(url_for('register'))
        
        register_user(username, password)
        
        return redirect(url_for('preferences'))
    
    return render_template('register.html')

# Ruta para la página de preferencias de usuario
@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    """Ruta para la página de preferencias de usuario."""
    return render_template('preferences_form.html')

# Ruta para guardar las preferencias del usuario
@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    """Ruta para guardar las preferencias del usuario."""
    user_id = obtener_ultimo_user_id()
    gender_preference = request.form.get('gender_preference')
    edad_minima = request.form.get('edad_minima')
    edad_maxima = request.form.get('edad_maxima')
    distancia_minima = request.form.get('distancia_minima')
    distancia_maxima = request.form.get('distancia_maxima')
    altura_minima = request.form.get('altura_minima')
    altura_maxima = request.form.get('altura_maxima')
    religion = request.form.get('religion')
    other_religion = request.form.get('other_religion') if religion == 'otro' else None
    relationship_status = request.form.get('relationship_status')
    deportes = request.form.getlist('deportes[]')
    musica = request.form.getlist('musica[]')
    peliculas = request.form.getlist('peliculas[]')
    pasatiempos = request.form.getlist('pasatiempos[]')
    tecnologia = request.form.getlist('tecnologia[]')
    cultura = request.form.getlist('cultura[]')
    estilo_vida = request.form.getlist('estilo_vida[]')
    relationship_type = request.form.get('relationship_type')
    other_relationship = request.form.get('other_relationship') if relationship_type == 'otras' else None
    smoker_preference = request.form.get('smoker_preference')
    drinker_preference = request.form.get('drinker_preference')
    education_level = request.form.get('education_level')

    intereses = deportes + musica + peliculas + pasatiempos + tecnologia + cultura + estilo_vida
    
    preferences_db.save_preferences(user_id, gender_preference, edad_minima, edad_maxima, distancia_minima, distancia_maxima, 
                                    altura_minima, altura_maxima, religion, other_religion, relationship_status, intereses, 
                                    relationship_type, other_relationship, smoker_preference, drinker_preference, education_level)
    
    id_usuario_similar = SimilarUserFinder().find_similar_user(user_id)

    if id_usuario_similar:
        gustos_usuario_similar = UserLikesProcessor().ejecutar_tecnicas_de_seleccion(id_usuario_similar, 15)
        
        nuevo_gusto_id = obtener_nuevo_gusto_id()  

        for gusto in gustos_usuario_similar:
            gusto['gusto_id'] = nuevo_gusto_id
            gusto['user_id'] = user_id
            gusto['veces_utilizado'] = 0
            gusto['likes'] = 0
            save_gusto(gusto)
            nuevo_gusto_id += 1
    
    return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    """Ruta para cerrar sesión."""
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
