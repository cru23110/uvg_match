from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from src.recommendation_algorithm import ContentBasedRecommendation
from src.authentication import authenticate_user, get_user_id, get_username_by_id, register_user
from db.neo4j.neo4j_config import neo4j_connection

app = Flask(__name__)

app.secret_key = 'HjbRlkNgrFNkmws'
# Crear una instancia del algoritmo de recomendación
recommendation_system = ContentBasedRecommendation()

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

    data = {
        'users': users,
        'profiles': profiles,
        'preferences': preferences
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
        
        # Redirigir al usuario a la página de inicio de sesión después de registrarse
        return redirect(url_for('login'))
    
    # Renderizar la página de registro de usuarios
    return render_template('register.html')

# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    # Eliminar la sesión del usuario al cerrar sesión
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)