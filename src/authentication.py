from db.neo4j_config import neo4j_connection

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

def register_user(username, password):
    # Obtener el último ID de usuario
    with neo4j_connection.get_session() as session:
        result = session.run("MATCH (u:Usuario) RETURN max(u.id_usuario) AS last_id")
        last_id = result.single().get('last_id', 0)

        # Generar un nuevo ID para el usuario
        # Si last_id es None, significa que no hay usuarios en la base de datos
        if last_id is None:
            new_id = 1
        else:
            new_id = last_id + 1

        # Insertar el nuevo usuario en la base de datos
        session.run("CREATE (u:Usuario {id_usuario: $new_id, nombre: $username, password: $password})", 
                    new_id=new_id, username=username, password=password)

def get_username_by_id(user_id):
    # Consultar la base de datos para obtener el nombre de usuario por su ID
    with neo4j_connection.get_session() as session:
        result = session.run("MATCH (u:Usuario {id_usuario: $user_id}) RETURN u.nombre AS username", user_id=user_id)
        record = result.single()
        if record:
            return record["username"]
        else:
            return None

def obtener_ultimo_user_id():
    with neo4j_connection.get_session() as session:
        result = session.run(
            """
            MATCH (u:Usuario)
            RETURN max(u.id_usuario) as user_id
            """
        )
        record = result.single()
        if record:
            return record['user_id']
        else:
            return None
        
def obtener_nuevo_gusto_id():
    with neo4j_connection.get_session() as session:
        result = session.run("MATCH (g:Gusto) RETURN MAX(g.gusto_id) AS max_id")
        record = result.single()
        max_id = record['max_id'] if record['max_id'] else 0
        return max_id + 1
        
def save_gusto(gusto):
    with neo4j_connection.get_session() as session:
        session.run(
            """
            CREATE (g:Gusto {gusto_id: $gusto_id, user_id: $user_id, nombre: $nombre, clase: $clase, veces_utilizado: $veces_utilizado, likes: $likes})
            """,
            gusto_id=gusto['gusto_id'],
            user_id=gusto['user_id'],
            nombre=gusto['nombre'],
            clase=gusto['clase'],
            veces_utilizado=gusto['veces_utilizado'],
            likes=gusto['likes']
        )
        session.run(
            """
            MATCH (u:Usuario {id_usuario: $user_id}), (g:Gusto {gusto_id: $gusto_id})
            CREATE (u)-[:TIENE_GUSTO]->(g)
            """,
            user_id=gusto['user_id'],
            gusto_id=gusto['gusto_id']
        )
