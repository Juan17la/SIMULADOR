"""
Optimización de parámetros para la interceptación de misiles
"""

import numpy as np
from scipy.optimize import minimize
from physics import calcular_tiempo_vuelo_enemigo, calcular_posicion_enemigo, calcular_posicion_misil

def encontrar_parametros_optimos(altura_enemigo, distancia_enemigo, min_velocidad, max_velocidad, delay):
    """
    Calcula los parámetros óptimos (ángulo y velocidad) para interceptar el misil enemigo
    considerando un delay fijo de lanzamiento
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
        if enemigo_y <= 0:
            return float('inf')
            
        # Posición del misil defensor considerando el delay
        misil_x, misil_y = calcular_posicion_misil(
            angulo, velocidad, tiempo_intercepcion, delay
        )
        
        # Calcular distancia entre misiles
        distancia = np.sqrt(
            (misil_x - distancia_enemigo)**2 + 
            (misil_y - enemigo_y)**2
        )
        
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
        options={'ftol': 1e-6, 'maxiter': 1000}
    )
    
    return resultado
