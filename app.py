from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from src.recommendation_system.profile_generation_manager import generate_new_profile
from src.authentication import authenticate_user, get_user_id, get_username_by_id, obtener_ultimo_user_id, register_user
from db.neo4j_config import neo4j_connection
from src.preferences import PreferencesDB

app = Flask(__name__)

app.secret_key = 'HjbRlkNgrFNkmws'

# Crear una instancia del manejo de preferencias de usuario
preferences_db = PreferencesDB()

# Ruta para la página principal
@app.route('/')
def index():
    # Verificar si el usuario está logueado
    if 'user_id' not in session:
        # Si no hay un usuario logueado, redirigir a la página de inicio de sesión
        return redirect(url_for('login'))
    
    # Obtener el ID del usuario activo en la sesión
    user_id = session.get('user_id')

    # Obtener el nombre de usuario correspondiente al ID del usuario
    current_user = get_username_by_id(user_id)
    
    # Obtener los datos del nuevo perfil
    nuevo_perfil = generate_new_profile(user_id)
    
    # Renderizar la página principal con los datos del usuario y del perfil
    return render_template('index.html', current_user=current_user, nuevo_perfil=nuevo_perfil)

@app.route('/handle_like_dislike', methods=['POST'])
def handle_like_dislike():
    data = request.get_json()
    action = data.get('action')
    
    # Obtener el ID del usuario activo
    user_id = session.get('user_id')
    if user_id:
        # Aquí puedes manejar la lógica para "like" y "dislike"
        if action == 'like':
            # Lógica para "like"
            pass
        elif action == 'dislike':
            # Lógica para "dislike"
            pass
        
        # Generar un nuevo perfil
        result = generate_new_profile(user_id)
        if result:
            return jsonify(success=True)
        else:
            return jsonify(success=False)
    else:
        return jsonify(success=False, message="Usuario no autenticado")

@app.route('/pro_version')
def pro_version():
    # Obtener el ID del usuario activo en la sesión
    user_id = session.get('user_id')

    # Obtener el nombre de usuario correspondiente al ID del usuario
    current_user = get_username_by_id(user_id)

    # Obtener los datos del nuevo perfil
    nuevo_perfil = generate_new_profile(user_id)
    
    # Renderizar la página principal
    return render_template('pro_version.html', current_user=current_user, nuevo_perfil=nuevo_perfil)

# Ruta para generar un nuevo perfil
@app.route('/generate_new_profile')
def generate_new_profile_route():
    # Obtener el ID del usuario activo
    user_id = session.get('user_id')
    if user_id:
        # Llamar a la función para generar el nuevo perfil
        result = generate_new_profile(user_id)
        if result:
            return "Nuevo perfil generado exitosamente"
        else:
            return "Error al generar el nuevo perfil"
    else:
        return "Usuario no autenticado"

# Función para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener las credenciales del formulario de inicio de sesión
        username = request.form['username']
        password = request.form['password']
        
        # Verificar las credenciales con la función de autenticación
        if authenticate_user(username, password):
            # Si las credenciales son válidas, establecer la sesión del usuario con su ID y redirigirlo a la página principal
            user_id = get_user_id(username, password)
            session['user_id'] = user_id
            return redirect(url_for('index'))

    # Si el método es GET o las credenciales son incorrectas, renderizar la página de inicio de sesión
    return render_template('login.html')

# Ruta para la página de registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener las credenciales del formulario de registro
        username = request.form['username']
        password = request.form['password']
        
        # Verificar si tanto el nombre de usuario como la contraseña no están vacíos
        if not username.strip() or not password.strip():
            # Redirigir al usuario nuevamente a la página de registro
            return redirect(url_for('register'))
        
        # Registrar al nuevo usuario en la base de datos
        register_user(username, password)
        
        # Redirigir al usuario a la página de preferencias después de registrarse
        return redirect(url_for('preferences'))
    
    # Renderizar la página de registro de usuarios
    return render_template('register.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    return render_template('preferences_form.html')

# Ruta para guardar las preferencias del usuario
@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    
    user_id = obtener_ultimo_user_id()
    # Recuperar los datos del formulario
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

    # Combinar todas las listas de intereses en una sola lista
    intereses = deportes + musica + peliculas + pasatiempos + tecnologia + cultura + estilo_vida
    
    # Guardar las preferencias en la base de datos
    preferences_db.save_preferences(user_id, gender_preference, edad_minima, edad_maxima, distancia_minima, distancia_maxima, 
                                    altura_minima, altura_maxima, religion, other_religion, relationship_status, intereses, 
                                    relationship_type, other_relationship, smoker_preference, drinker_preference, education_level)
    
    # Redirigir al usuario a la página de inicio de sesión después de guardar las preferencias
    return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    # Eliminar la sesión del usuario al cerrar sesión
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)