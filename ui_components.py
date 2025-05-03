"""
Componentes de la interfaz de usuario para la simulación de misiles
"""

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import (MIN_ALTURA, MAX_ALTURA, MIN_DISTANCIA, MAX_DISTANCIA,
                   MIN_VELOCIDAD, MAX_VELOCIDAD, MIN_ANGULO, MAX_ANGULO, MIN_DELAY, MAX_DELAY)

def crear_panel_control(parent, simulacion):
    """
    Crea el panel de control con los ajustes de la simulación
    """
    # Marco para controles
    panel_controles = ttk.LabelFrame(parent, text="Parámetros de Simulación")
    panel_controles.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    
    # Controles para altura del misil enemigo
    ttk.Label(panel_controles, text="Altura del misil enemigo (km):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    escala_altura = ttk.Scale(panel_controles, from_=MIN_ALTURA, to=MAX_ALTURA, 
                           length=200, value=simulacion.altura_enemigo, command=simulacion.actualizar_altura)
    escala_altura.grid(row=0, column=1, padx=5, pady=5)
    valor_altura = ttk.Label(panel_controles, text=f"{simulacion.altura_enemigo:.1f}")
    valor_altura.grid(row=0, column=2, padx=5, pady=5)
    simulacion.etiqueta_altura = valor_altura
    
    # Controles para la distancia de defensa
    ttk.Label(panel_controles, text="Distancia horizontal (km):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    escala_distancia = ttk.Scale(panel_controles, from_=MIN_DISTANCIA, to=MAX_DISTANCIA, 
                             length=200, value=simulacion.distancia_defensa, command=simulacion.actualizar_distancia)
    escala_distancia.grid(row=1, column=1, padx=5, pady=5)
    valor_distancia = ttk.Label(panel_controles, text=f"{simulacion.distancia_defensa:.1f}")
    valor_distancia.grid(row=1, column=2, padx=5, pady=5)
    simulacion.etiqueta_distancia = valor_distancia
    
    # Controles para la velocidad del misil
    ttk.Label(panel_controles, text="Velocidad del misil (km/s):").grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
    escala_velocidad = ttk.Scale(panel_controles, from_=MIN_VELOCIDAD, to=MAX_VELOCIDAD, 
                          length=200, value=simulacion.velocidad_misil, command=simulacion.actualizar_velocidad)
    escala_velocidad.grid(row=0, column=4, padx=5, pady=5)
    valor_velocidad = ttk.Label(panel_controles, text=f"{simulacion.velocidad_misil:.1f}")
    valor_velocidad.grid(row=0, column=5, padx=5, pady=5)
    simulacion.etiqueta_velocidad = valor_velocidad
    
    # Controles para el ángulo del misil
    ttk.Label(panel_controles, text="Ángulo de lanzamiento (°):").grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
    escala_angulo = ttk.Scale(panel_controles, from_=MIN_ANGULO, to=MAX_ANGULO, 
                          length=200, value=simulacion.angulo_misil, command=simulacion.actualizar_angulo)
    escala_angulo.grid(row=1, column=4, padx=5, pady=5)
    valor_angulo = ttk.Label(panel_controles, text=f"{simulacion.angulo_misil:.1f}")
    valor_angulo.grid(row=1, column=5, padx=5, pady=5)
    simulacion.etiqueta_angulo = valor_angulo
    
    # Controles para el delay de lanzamiento
    ttk.Label(panel_controles, text="Delay de lanzamiento (s):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    escala_delay = ttk.Scale(panel_controles, from_=MIN_DELAY, to=MAX_DELAY, 
                          length=200, value=simulacion.delay_lanzamiento, command=simulacion.actualizar_delay)
    escala_delay.grid(row=2, column=1, padx=5, pady=5)
    valor_delay = ttk.Label(panel_controles, text=f"{simulacion.delay_lanzamiento:.1f}")
    valor_delay.grid(row=2, column=2, padx=5, pady=5)
    simulacion.etiqueta_delay = valor_delay
    
    # Guardar referencias a las escalas
    simulacion.escala_angulo = escala_angulo
    simulacion.escala_velocidad = escala_velocidad
    simulacion.escala_altura = escala_altura
    simulacion.escala_distancia = escala_distancia
    simulacion.escala_delay = escala_delay
    
    # Panel de botones
    panel_botones = ttk.Frame(panel_controles)
    panel_botones.grid(row=3, column=0, columnspan=6, pady=10)
    
    boton_calcular = ttk.Button(panel_botones, text="Calcular Interceptación Óptima", 
                                command=simulacion.calcular_parametros_optimos)
    boton_calcular.pack(side=tk.LEFT, padx=5)
    
    boton_iniciar = ttk.Button(panel_botones, text="Iniciar Simulación", 
                            command=simulacion.iniciar_simulacion)
    boton_iniciar.pack(side=tk.LEFT, padx=5)
    
    boton_detener = ttk.Button(panel_botones, text="Detener", 
                           command=simulacion.detener_simulacion)
    boton_detener.pack(side=tk.LEFT, padx=5)
    boton_detener.config(state=tk.DISABLED)
    
    boton_reiniciar = ttk.Button(panel_botones, text="Reiniciar", 
                            command=simulacion.reiniciar_simulacion)
    boton_reiniciar.pack(side=tk.LEFT, padx=5)
    
    # Guardar referencias a los botones
    simulacion.boton_calcular = boton_calcular
    simulacion.boton_iniciar = boton_iniciar
    simulacion.boton_detener = boton_detener
    simulacion.boton_reiniciar = boton_reiniciar
    
    return panel_controles

def crear_info_panel(parent, simulacion):
    """
    Crea el panel de información para mostrar datos de la simulación
    """
    panel_info = ttk.LabelFrame(parent, text="Información")
    panel_info.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    
    etiqueta_info = ttk.Label(panel_info, text="Presiona 'Iniciar Simulación' para comenzar")
    etiqueta_info.pack(pady=5)
    
    simulacion.etiqueta_info = etiqueta_info  # Guardar referencia
    
    return panel_info

def crear_plot(parent, simulacion):
    """
    Crea el gráfico de simulación
    """
    # Crear figura y subplots
    figura = Figure(figsize=(10, 6))
    ejes = figura.add_subplot(111)
    figura.subplots_adjust(bottom=0.15)
    
    # Configurar el gráfico
    ejes.set_xlabel('Distancia Horizontal (km)')
    ejes.set_ylabel('Altura (km)')
    ejes.set_title('Simulación de Interceptación de Misiles')
    ejes.grid(True)
    
    # Crear líneas para las trayectorias
    linea_enemigo, = ejes.plot([], [], 'ro-', lw=2, label='Misil Enemigo')
    linea_misil, = ejes.plot([], [], 'bo-', lw=2, label='Misil Antiaéreo')
    
    # Crear marcadores para las posiciones
    punto_enemigo, = ejes.plot([], [], 'ro', markersize=10)
    punto_misil, = ejes.plot([], [], 'bo', markersize=10)
    inicio_enemigo, = ejes.plot([], [], 'kx', markersize=10, label='Inicio Misil Enemigo')
    defensa_posicion, = ejes.plot([], [], 'gs', markersize=10, label='Posición Defensa')
    ciudad_posicion, = ejes.plot([], [], 'r^', markersize=10, label='Ciudad')
    
    # Añadir leyenda
    ejes.legend(loc='upper right')
    
    # Incorporar el gráfico en la interfaz
    lienzo = FigureCanvasTkAgg(figura, master=parent)
    widget_lienzo = lienzo.get_tk_widget()
    widget_lienzo.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Guardar referencias
    simulacion.figura = figura
    simulacion.ejes = ejes
    simulacion.lienzo = lienzo
    simulacion.linea_enemigo = linea_enemigo
    simulacion.linea_misil = linea_misil
    simulacion.punto_enemigo = punto_enemigo
    simulacion.punto_misil = punto_misil
    simulacion.inicio_enemigo = inicio_enemigo
    simulacion.defensa_posicion = defensa_posicion
    simulacion.ciudad_posicion = ciudad_posicion
    
    # Actualizar límites iniciales
    ejes.set_xlim(-5, simulacion.distancia_defensa + 5)
    ejes.set_ylim(-0.5, simulacion.altura_enemigo + 2)
    lienzo.draw_idle()
    
    return lienzo

def mostrar_valores_optimos(resultado, tiempo, altura):
    """
    Muestra el resultado de la optimización en un cuadro de diálogo
    """
    angulo_optimo, velocidad_optima, tiempo_optimo = resultado.x
    
    mensaje = (
        f"Parámetros óptimos calculados:\n\n"
        f"Ángulo: {angulo_optimo:.1f}°\n"
        f"Velocidad: {velocidad_optima:.1f} km/s\n"
        f"Tiempo estimado de interceptación: {tiempo_optimo:.1f} s\n"
        f"Altura de interceptación: {altura:.1f} km\n"
        f"Tiempo de vuelo del misil enemigo: {tiempo:.1f} s\n")
    
    messagebox.showinfo("Resultados de la Optimización", mensaje)