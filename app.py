from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from src.recommendation_algorithm import ContentBasedRecommendation
from src.authentication import authenticate_user, get_user_id, get_username_by_id, obtener_ultimo_user_id, register_user
from db.neo4j.neo4j_config import neo4j_connection
from src.preferences import PreferencesDB

app = Flask(__name__)

app.secret_key = 'HjbRlkNgrFNkmws'
# Crear una instancia del algoritmo de recomendación
recommendation_system = ContentBasedRecommendation()
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
    
    # Renderizar la página principal
    return render_template('index.html', current_user=current_user)


@app.route('/pro_version')
def pro_version():
    # Obtener el ID del usuario activo en la sesión
    user_id = session.get('user_id')

    # Obtener el nombre de usuario correspondiente al ID del usuario
    current_user = get_username_by_id(user_id)
    
    # Renderizar la página principal
    return render_template('pro_version.html', current_user=current_user)

@app.route('/test')
def test_connection():
    with neo4j_connection.get_session() as session:
        users_result = session.run("MATCH (u:Usuario) RETURN u.id_usuario AS id, u.nombre AS nombre")
        users = [record for record in users_result]

        profiles_result = session.run("MATCH (p:Perfil) RETURN p.id_perfil AS id, p.nombre AS nombre, p.caracteristicas AS caracteristicas")
        profiles = [record for record in profiles_result]

        preferences_result = session.run("MATCH (u:Usuario)-[:LE_GUSTA]->(g:Gusto) RETURN u.id_usuario AS user_id, g.nombre AS gusto")
        preferences = [record for record in preferences_result]

        users_preferences_result = session.run("""
            MATCH (u:Usuario)-[:TIENE_PREFERENCIA_PRINCIPAL]->(pp:PreferenciaPrincipal)
            RETURN u.id_usuario AS user_id, u.nombre AS nombre, pp.tipo AS tipo_preferencia, pp.valor AS valor_preferencia
        """)

        users_preferences = [record for record in users_preferences_result]
        print("preferencias:", users_preferences)
        
    data = {
        'users': users,
        'profiles': profiles,
        'preferences': preferences,
        'users_preferences': users_preferences
    }
    return jsonify(data)

@app.route('/recommendation')
def recommendation():
    if 'user_id' not in session:
        # Si no hay un usuario logueado, redirigir a la página de login
        return redirect(url_for('login'))

    # Recomendar un perfil para el usuario logueado
    user_id = session['user_id']
    recommended_profile = recommendation_system.recommend_profiles(user_id)

    # Imprimir el perfil recomendado
    return "Perfil recomendado: {}".format(recommended_profile)

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
                         altura_minima, altura_maxima, religion, relationship_status, intereses,
                         relationship_type, smoker_preference, drinker_preference, education_level)
    
    # Imprimir los datos recibidos
    # print("id:", user_id)
    # print("Preferencia de género:", gender_preference)
    # print("Edad mínima:", edad_minima)
    # print("Edad máxima:", edad_maxima)
    # print("Distancia mínima:", distancia_minima)
    # print("Distancia máxima:", distancia_maxima)
    # print("Altura mínima:", altura_minima)
    # print("Altura máxima:", altura_maxima)
    # print("Religión:", religion)
    # print("Otra religión especificada:", other_religion)
    # print("Estado civil:", relationship_status)
    # print("Deportes:", deportes)
    # print("Música:", musica)
    # print("Películas:", peliculas)
    # print("Pasatiempos:", pasatiempos)
    # print("Tecnología:", tecnologia)
    # print("Cultura:", cultura)
    # print("Estilo de vida:", estilo_vida)
    # print("Intereses:", intereses)
    # print("Tipo de relación buscada:", relationship_type)
    # print("Otro tipo de relación especificado:", other_relationship)
    # print("Fumador:", smoker_preference)
    # print("Bebedor:", drinker_preference)
    # print("Nivel educativo:", education_level)
    
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