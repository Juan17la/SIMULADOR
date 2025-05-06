# Valores iniciales para la simulación
DEFAULT_ALTURA_ENEMIGA = 2.0  # km
DEFAULT_DISTANCIA_DEFENSA = 5.0  # km
DEFAULT_VELOCIDAD_MISIL = 0.3  # km/s
DEFAULT_ANGULO_MISIL = 45.0  # grados
DEFAULT_DELAY_LANZAMIENTO = 0.0  # segundos
GRAVEDAD = 9.8 / 1000  # km/s²

# Parámetros de simulación
INCREMENTO_TIEMPO = 0.1  # segundos
INTERVALO_ANIMACION = 50  # milisegundos
UMBRAL_INTERCEPCION = 0.1  # km

# Límites de los controles
MIN_ALTURA = 5  # km
MAX_ALTURA = 20.0  # km
MIN_DISTANCIA = 0.5  # km
MAX_DISTANCIA = 150.0  # km
MIN_VELOCIDAD = 0.6  # km/s
MAX_VELOCIDAD = 2.5  # km/s
MIN_ANGULO = 5  # grados
MAX_ANGULO = 90  # grados
MIN_DELAY = 0.0  # segundos
MAX_DELAY = 10.0  # segundos

# Configuración del historial de simulaciones
MAX_HISTORIAL_SIMULACIONES = 50
COLUMNAS_HISTORIAL = [
    "Tiempo (s)", "Altura (km)", "Distancia (km)", 
    "Velocidad (km/s)", "Ángulo (°)", "Delay (s)", "Resultado"
]