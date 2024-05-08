from flask import Flask, jsonify, redirect, render_template, session, url_for
from src.recommendation_algorithm import ContentBasedRecommendation
from db.neo4j.neo4j_config import neo4j_connection

app = Flask(__name__)

app.secret_key = 'your_secret_key'
# Crear una instancia del algoritmo de recomendación
recommendation_system = ContentBasedRecommendation()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pro_version')
def pro_version():
    return render_template('pro_version.html')

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

@app.route('/login/<int:user_id>')
def login(user_id):
    # Simular el inicio de sesión asignando el ID de usuario a la sesión
    session['user_id'] = user_id
    return "Usuario {} logueado".format(user_id)

@app.route('/logout')
def logout():
    # Eliminar el ID de usuario de la sesión al salir
    session.pop('user_id', None)
    return "Sesión cerrada"


if __name__ == '__main__':
    app.run(debug=True)

