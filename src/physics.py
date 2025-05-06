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
    considerando un delay en el lanzamiento
    
    Parámetros:
    - angulo: ángulo de lanzamiento en grados
    - velocidad: velocidad inicial en km/s
    - tiempo: tiempo transcurrido desde inicio de simulación
    - delay: tiempo de espera antes del lanzamiento
    """
    # Si no ha pasado el tiempo de delay, el misil está en posición inicial
    if tiempo < delay:
        return 0, 0
        
    # Ajustar el tiempo considerando el delay
    tiempo_efectivo = tiempo - delay
    
    # Convertir ángulo a radianes
    angulo_rad = np.radians(angulo)
    
    # Componentes de velocidad inicial
    vx = velocidad * np.cos(angulo_rad)
    vy = velocidad * np.sin(angulo_rad)
    
    # Posición en función del tiempo efectivo
    x = vx * tiempo_efectivo
    y = vy * tiempo_efectivo - 0.5 * GRAVEDAD * (tiempo_efectivo ** 2)
    
    return x, max(0, y)  # No permitir posiciones negativas en Y

def calcular_distancia(x1, y1, x2, y2):
    """
    Calcula la distancia euclidiana entre dos puntos
    """
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)