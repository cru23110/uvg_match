from db.neo4j_config import neo4j_connection
from src.recommendation_system.preferences_primary import PrimaryPreferences
import random

class UserLikesProcessor:
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
        
        return user_likes_sorted

    def verificar_gusto_repetido(self, gusto, gustos_seleccionados):
        for gusto_seleccionado in gustos_seleccionados:
            if gusto['gusto_id'] == gusto_seleccionado['gusto_id'] \
                    or gusto['nombre'] == gusto_seleccionado['nombre'] \
                    or (gusto['clase'] in ['Color de ojos', 'Rasgo físico'] and gusto['clase'] == gusto_seleccionado['clase']):
                return True
        return False

    def seleccionar_gustos_ponderados(self, gustos, cantidad_gustos=5):
        # Calcular las probabilidades de selección basadas en los puntajes
        puntajes = [gusto['puntaje'] for gusto in gustos]
        total_puntajes = sum(puntajes)
        probabilidades = [puntaje / total_puntajes for puntaje in puntajes]

        # Realizar muestreo aleatorio ponderado
        seleccionados = random.choices(gustos, weights=probabilidades, k=cantidad_gustos)

        # Verificar si hay gustos repetidos y volver a seleccionar si es necesario
        seleccionados_uniq = []
        for gusto in seleccionados:
            while self.verificar_gusto_repetido(gusto, seleccionados_uniq):
                gusto = random.choice(gustos)
            seleccionados_uniq.append(gusto)

        return seleccionados_uniq

    def seleccionar_gustos_cuartiles(self, gustos, cantidad_gustos=5):
        # Ordenar gustos por puntaje
        gustos_ordenados = sorted(gustos, key=lambda x: x['puntaje'], reverse=True)

        # Dividir gustos en cuartiles
        cuartiles = [gustos_ordenados[i::cantidad_gustos] for i in range(cantidad_gustos)]

        # Seleccionar un gusto de cada cuartil
        seleccionados = [random.choice(cuartil) for cuartil in cuartiles]

        # Verificar si hay gustos repetidos y volver a seleccionar si es necesario
        seleccionados_uniq = []
        for gusto in seleccionados:
            while self.verificar_gusto_repetido(gusto, seleccionados_uniq):
                gusto = random.choice(gustos)
            seleccionados_uniq.append(gusto)

        return seleccionados_uniq

    def seleccionar_gustos_epsilon_greedy(self, gustos, cantidad_gustos=5, epsilon=0.1):
        # Ordenar gustos por puntaje
        gustos_ordenados = sorted(gustos, key=lambda x: x['puntaje'], reverse=True)

        # Elegir gustos con explotación (basado en puntajes más altos)
        explotacion = gustos_ordenados[:cantidad_gustos]

        # Elegir gustos con exploración (al azar)
        exploracion = random.choices(gustos, k=cantidad_gustos)

        # Aplicar técnica ε-greedy
        seleccionados = explotacion if random.random() > epsilon else exploracion

        # Verificar si hay gustos repetidos y volver a seleccionar si es necesario
        seleccionados_uniq = []
        for gusto in seleccionados:
            while self.verificar_gusto_repetido(gusto, seleccionados_uniq):
                gusto = random.choice(gustos)
            seleccionados_uniq.append(gusto)

        return seleccionados_uniq

    def ejecutar_tecnicas_de_seleccion(self, user_id, cantidad_gustos):
        # Obtener gustos ordenados del usuario
        gustos_ordenados = self.ordenar_gustos(user_id)

        # print("Muestreo aleatorio ponderado:")
        seleccionados_ponderados = self.seleccionar_gustos_ponderados(gustos_ordenados, cantidad_gustos)
        # print(seleccionados_ponderados)

        # print("\nSelección basada en cuartiles:")
        seleccionados_cuartiles = self.seleccionar_gustos_cuartiles(gustos_ordenados, cantidad_gustos)
        # print(seleccionados_cuartiles)

        # print("\nTécnica ε-greedy:")
        seleccionados_epsilon_greedy = self.seleccionar_gustos_epsilon_greedy(gustos_ordenados, cantidad_gustos)
        # print(seleccionados_epsilon_greedy)

        return(seleccionados_ponderados)
    
class SimilarUserFinder:
    def __init__(self):
        pass

    def find_similar_user(self, current_user_id):
        # Obtener preferencias primarias del usuario actual
        current_user_preferences = PrimaryPreferences().get_primary_preferences(current_user_id)

        # Buscar usuarios con preferencias primarias similares
        similar_users = {}
        for user_id in self.get_all_user_ids():
            if user_id != current_user_id:
                user_preferences = PrimaryPreferences().get_primary_preferences(user_id)
                similarity_score = self.calculate_similarity(current_user_preferences, user_preferences)
                similar_users[user_id] = similarity_score

        # Ordenar usuarios por similitud y devolver el más similar
        most_similar_user_id = max(similar_users, key=similar_users.get) if similar_users else None

        return most_similar_user_id

    def get_all_user_ids(self):
        # Consultar la base de datos para obtener todos los IDs de usuario
        all_user_ids = []
        with neo4j_connection.get_session() as session:
            result = session.run("MATCH (u:Usuario) RETURN u.id_usuario AS user_id")
            for record in result:
                all_user_ids.append(record['user_id'])

        return all_user_ids

    def calculate_similarity(self, preferences1, preferences2):
        # Calcular la similitud entre dos conjuntos de preferencias primarias
        similarity_count = 0
        for preference_key in preferences1:
            if preference_key in preferences2:
                preference_value1 = preferences1[preference_key]
                preference_value2 = preferences2[preference_key]
                if isinstance(preference_value1, list) and isinstance(preference_value2, list):
                    # Si ambas preferencias son listas, comparamos sus elementos uno a uno
                    common_interests = set(preference_value1) & set(preference_value2)
                    similarity_count += len(common_interests)

                elif preference_value1 == preference_value2:
                    # Si no son listas, comparamos los valores directamente
                    similarity_count += 1

        return similarity_count
    
class GustosCombiner:
    @staticmethod
    def obtener_gustos_combinados(user_id):
        # Ejecutar técnicas de selección para el usuario en sesión
        gustos_usuario_sesion = UserLikesProcessor().ejecutar_tecnicas_de_seleccion(user_id, 5)

        # Encontrar usuario más similar
        id_usuario_similar = SimilarUserFinder().find_similar_user(user_id)

        if id_usuario_similar:
            # Ejecutar técnicas de selección para el usuario más similar
            gustos_usuario_similar = UserLikesProcessor().ejecutar_tecnicas_de_seleccion(id_usuario_similar, 3)

            # Verificar si hay gustos repetidos
            gustos_totales = gustos_usuario_sesion + gustos_usuario_similar
            gustos_totales_uniq = []
            for gusto in gustos_totales:
                if not UserLikesProcessor().verificar_gusto_repetido(gusto, gustos_totales_uniq):
                    gustos_totales_uniq.append(gusto)

            # Sumar puntajes
            puntaje_total = GustosCombiner.sumar_puntajes(gustos_totales_uniq)
            print(puntaje_total)
            # Eliminar campos y guardar en la lista de propiedades
            gustos_totales_uniq = GustosCombiner.eliminar_propiedades(gustos_totales_uniq)
        else:
            # Sumar puntajes
            puntaje_total = GustosCombiner.sumar_puntajes(gustos_usuario_sesion)
            print(puntaje_total)

            # Si no hay usuario similar, solo eliminar campos del usuario en sesión
            gustos_usuario_sesion = GustosCombiner.eliminar_propiedades(gustos_usuario_sesion)
            gustos_totales_uniq = gustos_usuario_sesion

        return gustos_totales_uniq
    
    @staticmethod
    def sumar_puntajes(gustos):
        puntaje_total = sum(gusto.get('puntaje', 0) for gusto in gustos)
        puntaje_total = round(puntaje_total, 3)
        return puntaje_total

    @staticmethod
    def eliminar_propiedades(gustos):
        propiedades = ['veces_utilizado', 'likes', 'puntaje'] #Eliminar la categoria de esta lista que se desea que se muestre otra vez
        for gusto in gustos:
            for propiedad in propiedades:
                if propiedad in gusto:
                    del gusto[propiedad]
        return gustos
