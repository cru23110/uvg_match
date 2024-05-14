from db.neo4j_config import neo4j_connection
import random

class RecommendationAlgorithm:
    def __init__(self):
        pass

    def get_user_likes(self, user_id):
        user_likes = []
        max_likes = 0
        with neo4j_connection.get_session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {id_usuario: $user_id})-[:TIENE_GUSTO]->(gusto)
                RETURN gusto.gusto_id AS gusto_id, gusto.nombre AS nombre_gusto, gusto.clase AS clase_gusto, gusto.veces_utilizado AS veces_utilizado, gusto.likes AS likes
                """,
                user_id=user_id
            )
            for record in result:
                gusto_info = {
                    "gusto_id": record["gusto_id"],
                    "nombre": record["nombre_gusto"],
                    "clase": record["clase_gusto"],
                    "veces_utilizado": record["veces_utilizado"],
                    "likes": record["likes"]
                }
                user_likes.append(gusto_info)
                # Actualizar el máximo de likes
                if record["likes"] > max_likes:
                    max_likes = record["likes"]
        return user_likes, max_likes
    
    def get_random_user_likes(self):
        random_user_likes = []
        max_likes = 0
        with neo4j_connection.get_session() as session:
            result = session.run(
                """
                MATCH (u:Usuario)-[:TIENE_GUSTO]->(gusto)
                WITH u, COLLECT(gusto) AS gustos
                ORDER BY rand()
                LIMIT 1
                UNWIND gustos AS gusto
                RETURN gusto.gusto_id AS gusto_id, gusto.nombre AS nombre_gusto, gusto.clase AS clase_gusto, gusto.veces_utilizado AS veces_utilizado, gusto.likes AS likes
                """
            )
            for record in result:
                gusto_info = {
                    "gusto_id": record["gusto_id"],
                    "nombre": record["nombre_gusto"],
                    "clase": record["clase_gusto"],
                    "veces_utilizado": record["veces_utilizado"],
                    "likes": record["likes"]
                }
                random_user_likes.append(gusto_info)
                # Actualizar el máximo de likes
                if record["likes"] > max_likes:
                    max_likes = record["likes"]
        return random_user_likes, max_likes

    def calcular_puntaje(self, gusto, max_likes):
        # Normalización de datos
        likes_normalizado = gusto['likes'] / max_likes
        veces_utilizado_normalizado = gusto['veces_utilizado'] / max_likes
        
        # Asignación de pesos
        peso_likes = 0.7
        peso_veces_utilizado = 0.3
        
        # Cálculo del puntaje ponderado
        puntaje = (peso_likes * likes_normalizado) + (peso_veces_utilizado * veces_utilizado_normalizado)

        puntaje = round(puntaje, 3)
        
        return puntaje

    def ordenar_gustos(self, user_id):
        # Obtener gustos del usuario y el máximo de likes
        user_likes, max_likes = self.get_user_likes(user_id)
        
        # Calcular puntaje para cada gusto del usuario
        for gusto in user_likes:
            gusto["puntaje"] = self.calcular_puntaje(gusto, max_likes)
        
        # Ordenar gustos del usuario por puntaje descendente
        user_likes_sorted = sorted(user_likes, key=lambda x: x["puntaje"], reverse=True)
        
        # # Obtener gustos aleatorios y el máximo de likes
        # random_user_likes, max_likes_random = self.get_random_user_likes()
        
        # # Calcular puntaje para cada gusto aleatorio
        # for gusto in random_user_likes:
        #     gusto["puntaje"] = self.calcular_puntaje(gusto, max_likes_random)
        
        # # Ordenar gustos aleatorios por puntaje descendente
        # random_user_likes_sorted = sorted(random_user_likes, key=lambda x: x["puntaje"], reverse=True)
        
        return user_likes_sorted

    def seleccionar_gustos_ponderados(self, gustos, cantidad_gustos):
        # Calcular las probabilidades de selección basadas en los puntajes
        puntajes = [gusto['puntaje'] for gusto in gustos]
        total_puntajes = sum(puntajes)
        probabilidades = [puntaje / total_puntajes for puntaje in puntajes]

        # Realizar muestreo aleatorio ponderado
        seleccionados = random.choices(gustos, weights=probabilidades, k=cantidad_gustos)

        return seleccionados

    def seleccionar_gustos_cuartiles(self, gustos, cantidad_gustos):
        # Ordenar gustos por puntaje
        gustos_ordenados = sorted(gustos, key=lambda x: x['puntaje'], reverse=True)

        # Dividir gustos en cuartiles
        cuartiles = [gustos_ordenados[i::cantidad_gustos] for i in range(cantidad_gustos)]

        # Seleccionar un gusto de cada cuartil
        seleccionados = [random.choice(cuartil) for cuartil in cuartiles]

        return seleccionados

    def seleccionar_gustos_epsilon_greedy(self, gustos, cantidad_gustos, epsilon=0.1):
        # Ordenar gustos por puntaje
        gustos_ordenados = sorted(gustos, key=lambda x: x['puntaje'], reverse=True)

        # Elegir gustos con explotación (basado en puntajes más altos)
        explotacion = gustos_ordenados[:cantidad_gustos]

        # Elegir gustos con exploración (al azar)
        exploracion = random.choices(gustos, k=cantidad_gustos)

        # Aplicar técnica ε-greedy
        seleccionados = explotacion if random.random() > epsilon else exploracion

        return seleccionados

    def ejecutar_tecnicas_de_seleccion(self, user_id):
        # Obtener gustos ordenados del usuario
        gustos_ordenados = self.ordenar_gustos(user_id)

        # Seleccionar la cantidad de gustos
        cantidad_gustos = 5

        print(f"Cantidad de gustos: {cantidad_gustos}")

        print("Muestreo aleatorio ponderado:")
        seleccionados_ponderados = self.seleccionar_gustos_ponderados(gustos_ordenados, cantidad_gustos)
        print(seleccionados_ponderados)

        print("\nSelección basada en cuartiles:")
        seleccionados_cuartiles = self.seleccionar_gustos_cuartiles(gustos_ordenados, cantidad_gustos)
        print(seleccionados_cuartiles)

        print("\nTécnica ε-greedy:")
        seleccionados_epsilon_greedy = self.seleccionar_gustos_epsilon_greedy(gustos_ordenados, cantidad_gustos)
        print(seleccionados_epsilon_greedy)
        