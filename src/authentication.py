from db.neo4j.neo4j_config import neo4j_connection

def authenticate_user(username, password):
    # Consultar la base de datos para encontrar el usuario por su nombre de usuario
    with neo4j_connection.get_session() as session:
        result = session.run("MATCH (u:Usuario {nombre: $username}) RETURN u.password AS password", username=username)
        record = result.single()

        # Verificar si se encontró el usuario y si la contraseña coincide
        if record and record['password'] == password:
            return True
        else:
            return False

def get_user_id(username, password):
    # Consultar la base de datos para encontrar el usuario por su nombre de usuario
    with neo4j_connection.get_session() as session:
        result = session.run("MATCH (u:Usuario {nombre: $username}) RETURN u.id_usuario AS user_id, u.password AS password", username=username)
        record = result.single()

        # Verificar si se encontró el usuario y si la contraseña coincide
        if record and record['password'] == password:
            return record['user_id']  # Devolver el ID del usuario si las credenciales son correctas
        else:
            return None  # Devolver None si las credenciales son incorrectas