"""
Optimización de parámetros para la interceptación de misiles
"""

import numpy as np
from scipy.optimize import minimize
from physics import calcular_tiempo_vuelo_enemigo, calcular_posicion_enemigo, calcular_posicion_misil, calcular_distancia
from config import GRAVEDAD

def validar_punto_intercepcion(misil_x, misil_y):
    """
    Valida que el punto de intercepción esté en coordenadas positivas
    """
    return misil_x >= 0 and misil_y >= 0

def validar_altura_intercepcion(altura):
    """
    Valida que la altura de intercepción sea mayor a 0.1km
    """
    return altura >= 0.1

def validar_impacto_suelo(altura):
    """
    Valida si el misil enemigo ha impactado en el suelo
    """
    return altura <= 0

def encontrar_parametros_optimos(altura_enemigo, distancia_enemigo, min_velocidad, max_velocidad, delay):
    """
    Calcula los parámetros óptimos (ángulo y velocidad) para interceptar el misil enemigo
    considerando un delay fijo de lanzamiento y asegurando intercepción en coordenadas positivas
    """
    tiempo_vuelo_enemigo = calcular_tiempo_vuelo_enemigo(altura_enemigo)
    
    def objetivo_funcion(params):
        angulo, velocidad, tiempo_intercepcion = params
        
        # Validaciones básicas
        if (tiempo_intercepcion <= delay or 
            tiempo_intercepcion > tiempo_vuelo_enemigo or
            velocidad < min_velocidad or 
            velocidad > max_velocidad):
            return float('inf')
        
        # Posición del misil enemigo en el tiempo de intercepción
        enemigo_y = calcular_posicion_enemigo(altura_enemigo, tiempo_intercepcion)
        
        # Validar si el misil enemigo impactó el suelo
        if validar_impacto_suelo(enemigo_y):
            return float('inf')
            
        # Validar altura mínima de intercepción
        if not validar_altura_intercepcion(enemigo_y):
            return float('inf')
            
        # Posición del misil defensor considerando el delay
        misil_x, misil_y = calcular_posicion_misil(
            angulo, velocidad, tiempo_intercepcion, delay
        )
        
        # Validar que el punto de intercepción esté en coordenadas positivas
        if not validar_punto_intercepcion(misil_x, misil_y):
            return float('inf')
        
        # Verificar que la trayectoria no pase por coordenadas negativas
        # Calculamos algunos puntos intermedios para verificar
        tiempos_intermedios = np.linspace(delay, tiempo_intercepcion, 10)
        for t in tiempos_intermedios:
            x_temp, y_temp = calcular_posicion_misil(angulo, velocidad, t, delay)
            if not validar_punto_intercepcion(x_temp, y_temp):
                return float('inf')
        
        # Calcular distancia entre misiles
        distancia = np.sqrt(
            (misil_x - distancia_enemigo)**2 + 
            (misil_y - enemigo_y)**2
        )
        
        # Penalizar soluciones cercanas a los límites del espacio positivo
        if misil_x < 0.1 or misil_y < 0.1:
            distancia += 100  # Penalización para evitar soluciones muy cercanas a 0
        
        return distancia
    
    # Valores iniciales y límites
    x0 = [45.0, (min_velocidad + max_velocidad)/2, tiempo_vuelo_enemigo/2]
    bounds = [
        (0, 90),                    # ángulo
        (min_velocidad, max_velocidad),  # velocidad
        (delay, tiempo_vuelo_enemigo)    # tiempo de intercepción
    ]
    
    # Realizar optimización
    resultado = minimize(
        objetivo_funcion, 
        x0,
        method='SLSQP',
        bounds=bounds,
        options={'ftol': 1e-6, 'maxiter': 10000}
    )
    
    return resultado
