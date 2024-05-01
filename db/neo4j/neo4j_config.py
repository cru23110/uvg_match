from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def get_session(self):
        return self._driver.session()

# Configuración de la conexión
neo4j_uri = "neo4j+s://9ec1c257.databases.neo4j.io"
neo4j_user = "neo4j"
neo4j_password = "kq7EDim_YAZ_FhLmBYJCrIeb0jbApSanoR0fzF5s3_E"

# Creación de la conexión
neo4j_connection = Neo4jConnection(neo4j_uri, neo4j_user, neo4j_password)
