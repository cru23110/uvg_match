from flask import Flask, jsonify, render_template
from db.neo4j.neo4j_config import neo4j_connection

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)

