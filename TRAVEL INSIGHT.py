import pandas as pd
from typing import List, Dict, Any, Optional
from fuzzywuzzy import fuzz 

FUZZY_THRESHOLD = 65 


# Los datos (simulated_tourism_data, simulated_user_behavior_data) que se usan aqui
# son SOLO para que tu puedas desarrollar y probar tu logica de forma independiente.
# En la aplicacion real con microservicios:
# 1. El microservicio de Backend de Alexander sera quien OBTENGA estos datos
#    de la base de datos MySQL (gestionada por Alejandro).
# 2. Alexander luego PASARA estos datos (o los resultados de consultas especificas)
#    a las funciones de tu clase TravelInsightLogic.
# Tu codigo Python se enfoca en PROCESAR los datos que recibe y DEVOLVER resultados.

# Ejemplo de datos de destinos turisticos (simulacion de lo que vendria de MySQL via Backend)
simulated_tourism_data: List[Dict[str, Any]] = [
    {"id": "D001", "nombre": "Villa de Leyva", "departamento": "Boyacá", "municipio": "Villa de Leyva", "tipo": "Pueblo historico", "actividades": ["Caminata", "Museos", "Gastronomia"], "servicios": ["Hotel", "Restaurante", "Transporte"]},
    {"id": "D002", "nombre": "Laguna de Tota", "departamento": "Boyacá", "municipio": "Tota", "tipo": "Naturaleza", "actividades": ["Deportes acuaticos", "Pesca", "Camping"], "servicios": ["Glamping", "Restaurante"]},
    {"id": "D003", "nombre": "Zipaquira", "departamento": "Cundinamarca", "municipio": "Zipaquirá", "tipo": "Cultural", "actividades": ["Catedral de Sal", "Mineria", "Gastronomia"], "servicios": ["Hotel", "Restaurante"]},
    {"id": "D004", "nombre": "Guatavita", "departamento": "Cundinamarca", "municipio": "Guatavita", "tipo": "Naturaleza/Cultural", "actividades": ["Laguna", "Arqueologia", "Artesanias"], "servicios": ["Hotel", "Restaurante"]},
    {"id": "D005", "nombre": "Paipa", "departamento": "Boyacá", "municipio": "Paipa", "tipo": "Termales", "actividades": ["Aguas termales", "Relax", "Deportes"], "servicios": ["Hotel", "Spa", "Restaurante", "Hotel Termales"]},
    {"id": "D006", "nombre": "Suesca", "departamento": "Cundinamarca", "municipio": "Suesca", "tipo": "Aventura", "actividades": ["Escalada", "Senderismo", "Camping"], "servicios": ["Glamping", "Restaurante"]},
    {"id": "D007", "nombre": "Mongui", "departamento": "Boyacá", "municipio": "Monguí", "tipo": "Pueblo historico", "actividades": ["Balones", "Artesanias", "Caminata"], "servicios": ["Hotel", "Restaurante"]},
    {"id": "D008", "nombre": "Choconta", "departamento": "Cundinamarca", "municipio": "Chocontá", "tipo": "Naturaleza", "actividades": ["Embalse", "Pesca", "Observacion de aves"], "servicios": ["Camping", "Restaurante"]},
    # NUEVOS DATOS DE HOTELES PARA LA SIMULACION (con campo municipio y categoria)
    {"id": "H001", "nombre": "Hotel Campestre La Posada", "departamento": "Boyacá", "municipio": "Paipa", "tipo": "Alojamiento", "categoria": "Campestre", "actividades": [], "servicios": ["Hotel", "Piscina", "Restaurante", "Wi-Fi"]},
    {"id": "H002", "nombre": "Hotel Boutique La Casona", "departamento": "Cundinamarca", "municipio": "Zipaquirá", "tipo": "Alojamiento", "categoria": "Boutique", "actividades": [], "servicios": ["Hotel", "Spa", "Restaurante", "Desayuno"]},
    {"id": "H003", "nombre": "Hostal El Viajero", "departamento": "Boyacá", "municipio": "Villa de Leyva", "tipo": "Alojamiento", "categoria": "Hostal", "actividades": [], "servicios": ["Hostal", "Wi-Fi"]},
    {"id": "H004", "nombre": "Hotel Termales Paipa Resort", "departamento": "Boyacá", "municipio": "Paipa", "tipo": "Alojamiento", "categoria": "Resort", "actividades": ["Aguas termales", "Relax"], "servicios": ["Hotel", "Spa", "Piscina termal", "Restaurante"]},
    {"id": "H005", "nombre": "Hotel Colonial Villa", "departamento": "Boyacá", "municipio": "Villa de Leyva", "tipo": "Alojamiento", "categoria": "Lujo", "actividades": [], "servicios": ["Hotel", "Jardines", "Desayuno"]},
    {"id": "H006", "nombre": "Hotel Económico Bogotá", "departamento": "Cundinamarca", "municipio": "Bogotá", "tipo": "Alojamiento", "categoria": "Económico", "actividades": [], "servicios": ["Hotel", "Wi-Fi"]},
]

# Ejemplo de datos de preferencias y comportamiento de usuarios (simulacion)
simulated_user_behavior_data: List[Dict[str, Any]] = [
    {"user_id": "Oscar", "accion": "consulta", "destino": "Villa de Leyva", "timestamp": "2025-01-10T10:00:00"}, # Enero
    {"user_id": "Oscar", "accion": "interes", "interes": "Historia", "timestamp": "2025-01-10T10:05:00"},
    {"user_id": "Valentina", "accion": "consulta", "destino": "Laguna de Tota", "timestamp": "2025-02-15T11:15:00"}, # Febrero
    {"user_id": "Oscar", "accion": "consulta", "destino": "Zipaquira", "timestamp": "2025-03-20T12:30:00"}, # Marzo
    {"user_id": "Alexander", "accion": "consulta", "destino": "Villa de Leyva", "timestamp": "2025-04-05T13:00:00"}, # Abril
    {"user_id": "Valentina", "accion": "interes", "interes": "Naturaleza", "timestamp": "2025-05-01T14:00:00"}, # Mayo
    {"user_id": "Oscar", "accion": "consulta", "destino": "Villa de Leyva", "timestamp": "2025-06-12T15:00:00"}, # Junio
    {"user_id": "Oscar", "accion": "consulta", "destino": "Laguna de Tota", "timestamp": "2025-07-24T16:00:00"}, # Julio
    {"user_id": "Valentina", "accion": "consulta", "destino": "Zipaquira", "timestamp": "2025-08-01T17:00:00"}, # Agosto
    {"user_id": "Alexander", "accion": "consulta", "destino": "Paipa", "timestamp": "2025-09-10T18:00:00"}, # Septiembre
    {"user_id": "Oscar", "accion": "interes", "interes": "Termales", "timestamp": "2025-10-02T19:00:00"}, # Octubre
    {"user_id": "Alejandro", "accion": "consulta", "destino": "Suesca", "timestamp": "2024-11-05T09:00:00"},
    {"user_id": "Alejandro", "accion": "consulta", "destino": "Mongui", "timestamp": "2024-12-25T14:00:00"},
    {"user_id": "Oscar", "accion": "consulta", "destino": "Hotel Campestre La Posada", "timestamp": "2025-07-25T10:00:00"}, # Nueva consulta de hotel
]

class TravelInsightLogic:
    """
    Clase que encapsula la logica de negocio para la aplicacion Travel Insight.
    Esta clase esta diseñada para ser un componente de logica de un microservicio.
    NO maneja la conexion a la base de datos directamente ni es un servidor web.
    Asume que los datos son proporcionados por el microservicio de Backend.
    """

    def __init__(self, tourism_data: List[Dict[str, Any]], user_behavior_data: List[Dict[str, Any]]):
        """
        Inicializa la logica con los datos turisticos y de comportamiento de usuario.
        Estos datos serian pasados por el microservicio de Backend.
        Args:
            tourism_data (List[Dict[str, Any]]): Lista de diccionarios con la informacion de destinos, actividades, etc.
            user_behavior_data (List[Dict[str, Any]]): Lista de diccionarios con el historial de preferencias y acciones de los usuarios.
        """
        # Convertimos a DataFrame para facilitar el manejo y analisis de datos
        # Esto es una decision de implementacion interna de tu logica.
        self.df_tourism = pd.DataFrame(tourism_data)
        self.df_user_behavior = pd.DataFrame(user_behavior_data)
        print("TravelInsightLogic: Datos cargados en DataFrames internos.")
        print(f"TravelInsightLogic: Columnas de df_tourism: {self.df_tourism.columns.tolist()}")
        print(f"TravelInsightLogic: Columnas de df_user_behavior: {self.df_user_behavior.columns.tolist()}")

    # --- Funcionalidad: Consulta de Información Turística ---
    def buscar_destinos(self, query: str = "", municipio: str = "", tipo: str = "", ubicacion: str = "") -> List[Dict[str, Any]]:
        """
        Busca destinos turisticos basados en una consulta, municipio, tipo o ubicacion general,
        utilizando busqueda difusa para los campos 'query' y 'ubicacion'.
        Args:
            query (str): Texto a buscar en el nombre del destino o actividades (busqueda difusa).
            municipio (str): Municipio a filtrar (filtro exacto).
            tipo (str): Tipo de destino (ej. 'Pueblo historico', 'Naturaleza') (filtro exacto/parcial).
            ubicacion (str): Termino general de ubicacion a buscar en nombre, departamento o municipio (busqueda difusa).
        Returns:
            List[Dict[str, Any]]: Lista de destinos que coinciden con los criterios.
        """
        print(f"TravelInsightLogic: Ejecutando buscar_destinos con query='{query}', municipio='{municipio}', tipo='{tipo}', ubicacion='{ubicacion}'...")
        # Excluir explicitamente los que son solo "Alojamiento" para esta busqueda de destinos generales
        filtered_df = self.df_tourism[self.df_tourism['tipo'] != 'Alojamiento'].copy()

        if query:
            # Aplicar busqueda difusa al nombre y actividades
            def fuzzy_match_query_row(row, search_query):
                name_ratio = fuzz.token_set_ratio(search_query, row['nombre'])
                if name_ratio >= FUZZY_THRESHOLD:
                    return True
                if isinstance(row['actividades'], list):
                    for activity in row['actividades']:
                        activity_ratio = fuzz.token_set_ratio(search_query, activity)
                        if activity_ratio >= FUZZY_THRESHOLD:
                            return True
                return False
            filtered_df = filtered_df[filtered_df.apply(fuzzy_match_query_row, args=(query,), axis=1)]

        if municipio:
            # Filtro exacto por municipio
            filtered_df = filtered_df[filtered_df['municipio'].str.contains(municipio, case=False, na=False)]
        if tipo:
            # Filtro exacto/parcial por tipo
            filtered_df = filtered_df[filtered_df['tipo'].str.contains(tipo, case=False, na=False)]
        
        if ubicacion:
            # Busqueda difusa en nombre, departamento y municipio para ubicacion general
            def fuzzy_match_ubicacion_row(row, search_ubicacion):
                name_match = fuzz.token_set_ratio(search_ubicacion, row['nombre']) >= FUZZY_THRESHOLD
                dept_match = fuzz.token_set_ratio(search_ubicacion, row['departamento']) >= FUZZY_THRESHOLD
                mun_match = fuzz.token_set_ratio(search_ubicacion, row['municipio']) >= FUZZY_THRESHOLD if 'municipio' in row and pd.notna(row['municipio']) else False
                return name_match or dept_match or mun_match
            filtered_df = filtered_df[filtered_df.apply(fuzzy_match_ubicacion_row, args=(ubicacion,), axis=1)]

        return filtered_df.to_dict(orient='records')

    # --- NUEVA FUNCIONALIDAD: Búsqueda de Hoteles ---
    def buscar_hoteles(self, query: str = "", municipio: str = "", categoria: str = "") -> List[Dict[str, Any]]:
        """
        Busca hoteles basados en una consulta, municipio o categoria,
        utilizando busqueda difusa para el campo 'query'.
        Args:
            query (str): Texto a buscar en el nombre del hotel o servicios (busqueda difusa).
            municipio (str): Municipio a filtrar (filtro exacto).
            categoria (str): Categoria del hotel (ej. 'Lujo', 'Campestre') (filtro exacto/parcial).
        Returns:
            List[Dict[str, Any]]: Lista de hoteles que coinciden con los criterios.
        """
        print(f"TravelInsightLogic: Ejecutando buscar_hoteles con query='{query}', municipio='{municipio}', categoria='{categoria}'...")
        # Filtrar inicialmente por aquellos que ofrecen servicio de "Hotel" o son de tipo "Alojamiento"
        filtered_hotels = self.df_tourism[
            (self.df_tourism['servicios'].apply(lambda x: isinstance(x, list) and any('hotel' in str(s).lower() for s in x))) |
            (self.df_tourism['tipo'].str.contains('alojamiento', case=False, na=False))
        ].copy()

        if query:
            def fuzzy_match_hotel_query_row(row, search_query):
                # Comprobar nombre del hotel
                name_ratio = fuzz.token_set_ratio(search_query, row['nombre'])
                if name_ratio >= FUZZY_THRESHOLD:
                    return True
                # Comprobar servicios del hotel
                if isinstance(row['servicios'], list):
                    for servicio in row['servicios']:
                        servicio_ratio = fuzz.token_set_ratio(search_query, servicio)
                        if servicio_ratio >= FUZZY_THRESHOLD:
                            return True
                return False
            filtered_hotels = filtered_hotels[filtered_hotels.apply(fuzzy_match_hotel_query_row, args=(query,), axis=1)]

        if municipio:
            # Filtro exacto por municipio
            filtered_hotels = filtered_hotels[filtered_hotels['municipio'].str.contains(municipio, case=False, na=False)]
        if categoria:
            # Filtro exacto/parcial por categoria
            filtered_hotels = filtered_hotels[filtered_hotels['categoria'].str.contains(categoria, case=False, na=False)]

        return filtered_hotels.to_dict(orient='records')


    # --- Funcionalidad: Registro de Preferencias del Usuario (Simulado para logica) ---
    def registrar_preferencia(self, user_name: str, interes: str) -> Dict[str, Any]:
        """
        Simula el registro de una preferencia de usuario.
        Args:
            user_name (str): Nombre del usuario.
            interes (str): Interes turistico del usuario.
        Returns:
            Dict[str, Any]: Diccionario con los datos de la preferencia registrada.
        """
        new_entry_data = {
            "user_id": user_name,
            "accion": "interes",
            "interes": interes,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        new_entry_df = pd.DataFrame([new_entry_data])
        self.df_user_behavior = pd.concat([self.df_user_behavior, new_entry_df], ignore_index=True)
        print(f"TravelInsightLogic: Preferencia '{interes}' registrada para el usuario '{user_name}' (simulado).")
        return new_entry_data

    def registrar_comportamiento(self, user_name: str, accion: str, destino: Optional[str] = None) -> Dict[str, Any]:
        """
        Simula el registro de un comportamiento de usuario.
        Args:
            user_name (str): Nombre del usuario.
            accion (str): Tipo de accion (ej. 'consulta', 'click').
            destino (str, optional): Destino asociado a la accion, si aplica.
        Returns:
            Dict[str, Any]: Diccionario con los datos del comportamiento registrado.
        """
        new_entry_data = {
            "user_id": user_name,
            "accion": accion,
            "destino": destino,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        new_entry_df = pd.DataFrame([new_entry_data])
        self.df_user_behavior = pd.concat([self.df_user_behavior, new_entry_df], ignore_index=True)
        print(f"TravelInsightLogic: Comportamiento '{accion}' registrado para el usuario '{user_name}' en el destino '{destino}' (simulado).")
        return new_entry_data

    # --- Funcionalidad: Visualización de Patrones Básicos ---
    def obtener_destinos_mas_consultados(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Identifica y devuelve los destinos turisticos mas consultados.
        Args:
            top_n (int): Numero de destinos principales a devolver.
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con 'destino' y 'consultas'.
        """
        print(f"TravelInsightLogic: Obteniendo top {top_n} destinos mas consultados...")
        consultas = self.df_user_behavior[self.df_user_behavior['accion'] == 'consulta']['destino'].value_counts().head(top_n)
        result = [{"destino": dest, "consultas": count} for dest, count in consultas.items()]
        return result

    # --- Funcionalidad: Sistema de Recomendaciones Iniciales ---
    def obtener_recomendaciones_basicas(self, user_name: str, num_recomendaciones: int = 3) -> List[Dict[str, Any]]:
        """
        Ofrece recomendaciones basicas a un usuario.
        Args:
            user_name (str): Nombre del usuario para quien generar recomendaciones.
            num_recomendaciones (int): Numero de recomendaciones a generar.
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los destinos recomendados.
        """
        print(f"TravelInsightLogic: Generando recomendaciones para el usuario '{user_name}'...")
        user_consultas = self.df_user_behavior[(self.df_user_behavior['user_id'] == user_name) & (self.df_user_behavior['accion'] == 'consulta')]['destino'].tolist()
        user_intereses = self.df_user_behavior[(self.df_user_behavior['user_id'] == user_name) & (self.df_user_behavior['accion'] == 'interes')]['interes'].tolist()

        if not user_consultas and not user_intereses:
            print("TravelInsightLogic: Usuario sin historial, recomendando los mas populares.")
            top_destinos = self.obtener_destinos_mas_consultados(top_n=num_recomendaciones)
            recommended_ids = [item['destino'] for item in top_destinos]
            return self.df_tourism[self.df_tourism['nombre'].isin(recommended_ids)].to_dict(orient='records')

        recommended_destinations = set()
        for interes in user_intereses:
            matching_destinos = self.df_tourism[
                self.df_tourism['actividades'].apply(lambda x: any(fuzz.token_set_ratio(interes, str(item)) >= FUZZY_THRESHOLD for item in x) if isinstance(x, list) else False) |
                self.df_tourism['tipo'].apply(lambda x: fuzz.token_set_ratio(interes, str(x)) >= FUZZY_THRESHOLD if x else False)
            ]['nombre'].tolist()
            recommended_destinations.update(matching_destinos)

        if len(recommended_destinations) < num_recomendaciones:
            popular_destinos = self.obtener_destinos_mas_consultados(top_n=num_recomendaciones * 2)
            for item in popular_destinos:
                if item['destino'] not in user_consultas:
                    recommended_destinations.add(item['destino'])
                if len(recommended_destinations) >= num_recomendaciones:
                    break

        final_recommendations = self.df_tourism[self.df_tourism['nombre'].isin(list(recommended_destinations))].head(num_recomendaciones).to_dict(orient='records')
        return final_recommendations


    # --- Funcionalidad: Reporte de Tendencias ---
    def generar_reporte_tendencias(self) -> Dict[str, Any]:
        """
        Genera un reporte basico de tendencias para administradores.
        Incluye destinos mas buscados, periodos de mayor afluencia (hora, dia, mes, semestre, año).
        Returns:
            Dict[str, Any]: Diccionario con las tendencias.
        """
        print("TravelInsightLogic: Generando reporte de tendencias...")
        reporte = {}

        # Destinos mas buscados
        reporte['destinos_mas_buscados'] = self.obtener_destinos_mas_consultados(top_n=10)

        # Analisis de afluencia por tiempo
        if not self.df_user_behavior.empty and 'timestamp' in self.df_user_behavior.columns:
            df_consultas = self.df_user_behavior[self.df_user_behavior['accion'] == 'consulta'].copy()
            if not df_consultas.empty:
                df_consultas['timestamp_dt'] = pd.to_datetime(df_consultas['timestamp'])
                df_consultas['hora_del_dia'] = df_consultas['timestamp_dt'].dt.hour
                df_consultas['dia_de_la_semana'] = df_consultas['timestamp_dt'].dt.day_name(locale='es')
                df_consultas['mes'] = df_consultas['timestamp_dt'].dt.month_name(locale='es')
                df_consultas['semestre'] = df_consultas['timestamp_dt'].dt.quarter.apply(lambda x: f"Semestre {1 if x <= 2 else 2}")
                df_consultas['año'] = df_consultas['timestamp_dt'].dt.year

                reporte['periodos_afluencia_hora'] = df_consultas['hora_del_dia'].value_counts().sort_index().to_dict()
                reporte['periodos_afluencia_dia'] = df_consultas['dia_de_la_semana'].value_counts().to_dict()

                meses_orden = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                afluencia_por_mes_raw = df_consultas['mes'].value_counts()
                reporte['periodos_afluencia_mes'] = {mes: afluencia_por_mes_raw.get(mes, 0) for mes in meses_orden if mes in afluencia_por_mes_raw.index or afluencia_por_mes_raw.get(mes, 0) > 0}
                reporte['periodos_afluencia_mes'] = {k: v for k, v in reporte['periodos_afluencia_mes'].items() if v > 0}


                reporte['periodos_afluencia_semestre'] = df_consultas['semestre'].value_counts().sort_index().to_dict()

                reporte['periodos_afluencia_año'] = df_consultas['año'].value_counts().sort_index().to_dict()
            else:
                print("TravelInsightLogic: No hay consultas en los datos de comportamiento para generar afluencia por tiempo.")
                reporte['periodos_afluencia_hora'] = {}
                reporte['periodos_afluencia_dia'] = {}
                reporte['periodos_afluencia_mes'] = {}
                reporte['periodos_afluencia_semestre'] = {}
                reporte['periodos_afluencia_año'] = {}
        else:
            print("TravelInsightLogic: No hay datos de comportamiento para generar periodos de afluencia.")
            reporte['periodos_afluencia_hora'] = {}
            reporte['periodos_afluencia_dia'] = {}
            reporte['periodos_afluencia_mes'] = {}
            reporte['periodos_afluencia_semestre'] = {}
            reporte['periodos_afluencia_año'] = {}


        print("TravelInsightLogic: Reporte de tendencias generado.")
        return reporte

# --- Ejemplo de Uso (para que puedas probar tu codigo de forma independiente) ---
# Este bloque NO se ejecutara cuando tu codigo sea importado por el microservicio de Backend.
# Es tu entorno de desarrollo y pruebas.
if __name__ == "__main__":
    print("Iniciando pruebas de la logica de Travel Insight (modo standalone)...")

    logic = TravelInsightLogic(simulated_tourism_data, simulated_user_behavior_data)

    print("\n--- Probando Consulta de Información Turística (con nuevos filtros) ---")
    # Buscar por municipio
    destinos_villa = logic.buscar_destinos(municipio="Villa de Leyva")
    print(f"Destinos en Villa de Leyva: {len(destinos_villa)} encontrados")
    for d in destinos_villa:
        print(f"  - {d['nombre']} ({d['municipio']})")

    # Buscar por ubicación general (departamento o municipio)
    destinos_cundinamarca_ubicacion = logic.buscar_destinos(ubicacion="Cundinamarca")
    print(f"\nDestinos con ubicación 'Cundinamarca': {len(destinos_cundinamarca_ubicacion)} encontrados")
    for d in destinos_cundinamarca_ubicacion:
        print(f"  - {d['nombre']} ({d['departamento']}, {d['municipio']})")

    destinos_pueblo_historico_ubicacion = logic.buscar_destinos(ubicacion="pueblo historico")
    print(f"\nDestinos con ubicación 'pueblo historico': {len(destinos_pueblo_historico_ubicacion)} encontrados")
    for d in destinos_pueblo_historico_ubicacion:
        print(f"  - {d['nombre']} ({d['departamento']}, {d['municipio']})")

    # Buscar por nombre/actividad (fuzzy)
    destinos_escalada = logic.buscar_destinos(query="Escaladar") # Con typo
    print(f"\nDestinos para 'Escaladar': {len(destinos_escalada)} encontrados")
    for d in destinos_escalada:
        print(f"  - {d['nombre']} ({d['actividades']})")


    print("\n--- Probando Búsqueda de Hoteles (con nuevos filtros) ---")
    # Buscar por municipio
    hoteles_zipaquira = logic.buscar_hoteles(municipio="Zipaquirá")
    print(f"Hoteles en Zipaquirá: {len(hoteles_zipaquira)} encontrados")
    for h in hoteles_zipaquira:
        print(f"  - {h['nombre']} ({h['municipio']})")

    # Buscar por categoría
    hoteles_boutique = logic.buscar_hoteles(categoria="Boutique")
    print(f"\nHoteles de categoría 'Boutique': {len(hoteles_boutique)} encontrados")
    for h in hoteles_boutique:
        print(f"  - {h['nombre']} ({h['categoria']})")

    # Buscar por nombre (fuzzy)
    hoteles_posada = logic.buscar_hoteles(query="Posada")
    print(f"\nHoteles con 'Posada' en el nombre: {len(hoteles_posada)} encontrados")
    for h in hoteles_posada:
        print(f"  - {h['nombre']}")

    # Combinación de filtros
    hoteles_paipa_resort = logic.buscar_hoteles(municipio="Paipa", categoria="Resort")
    print(f"\nHoteles Resort en Paipa: {len(hoteles_paipa_resort)} encontrados")
    for h in hoteles_paipa_resort:
        print(f"  - {h['nombre']}")


    print("\n--- Probando Registro de Preferencias y Comportamiento ---")
    new_pref = logic.registrar_preferencia("Oscar", "Aventura")
    print(f"Datos de nueva preferencia a guardar por Backend: {new_pref}")
    new_comp = logic.registrar_comportamiento("Oscar", "consulta", "Suesca")
    print(f"Datos de nuevo comportamiento a guardar por Backend: {new_comp}")
    logic.registrar_comportamiento("Valentina", "click", "Laguna de Tota")

    print("\n--- Probando Visualización de Patrones Básicos ---")
    top_consultados = logic.obtener_destinos_mas_consultados(top_n=3)
    print(f"Top 3 destinos mas consultados: {top_consultados}")

    print("\n--- Probando Sistema de Recomendaciones Iniciales ---")
    recomendaciones_oscar = logic.obtener_recomendaciones_basicas("Oscar")
    print(f"Recomendaciones para Oscar: {len(recomendaciones_oscar)} encontradas")
    for r in recomendaciones_oscar:
        print(f"  - {r['nombre']}")

    recomendaciones_nuevo = logic.obtener_recomendaciones_basicas("NuevoUsuario")
    print(f"Recomendaciones para NuevoUsuario: {len(recomendaciones_nuevo)} encontradas")
    for r in recomendaciones_nuevo:
        print(f"  - {r['nombre']}")

    print("\n--- Probando Reporte de Tendencias ---")
    reporte_tendencias = logic.generar_reporte_tendencias()
    print("Reporte Generado:")
    for key, value in reporte_tendencias.items():
        print(f"  {key}: {value}")

    print("\nPruebas de la logica de Travel Insight finalizadas.")