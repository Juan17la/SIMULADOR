import numpy as np
from config import GRAVEDAD

def calcular_tiempo_vuelo_enemigo(altura):
    """
    Calcula el tiempo de vuelo del misil enemigo hasta el suelo
    usando la ecuación de caída libre: h = 1/2 * g * t²
    Despejando t 
    t = sqrt(2h/g)
    """
    return np.sqrt(2 * altura / GRAVEDAD)

def calcular_posicion_enemigo(altura_inicial, tiempo):
    """
    Calcula la posición Y del misil enemigo en caída libre
    
    y = h - 1/2 * g * t²  # Ecuación de caída libre
    """
    y = altura_inicial - 0.5 * GRAVEDAD * (tiempo ** 2)
    return max(0, y)  # No permitir posiciones negativas

def calcular_posicion_misil(angulo, velocidad, tiempo, delay):
    """
    Calcula la posición del misil antiaéreo según el movimiento parabólico
    """
    if tiempo < delay:
        return 0, 0
        
    # Asegurar que el ángulo sea float y convertir a radianes
    tiempo_efectivo = tiempo - delay
    angulo_rad = np.radians(float(angulo))
    
    # Asegurar que velocidad sea float
    velocidad = float(velocidad)
    
    # Calcular componentes de velocidad
    vx = velocidad * np.cos(angulo_rad)
    vy = velocidad * np.sin(angulo_rad)
    
    # Calcular posición
    x = vx * tiempo_efectivo
    y = vy * tiempo_efectivo - 0.5 * GRAVEDAD * (tiempo_efectivo ** 2)
    
    return x, max(0, y)

def calcular_distancia(x1, y1, x2, y2):
    """
    Calcula la distancia euclidiana entre dos puntos
    """
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)