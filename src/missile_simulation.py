"""
Clase principal para la simulación de interceptación de misiles
.set_data
"""

import numpy as np
import matplotlib
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox
from config import (DEFAULT_ALTURA_ENEMIGA, DEFAULT_DISTANCIA_DEFENSA,
                   DEFAULT_VELOCIDAD_MISIL, DEFAULT_ANGULO_MISIL,
                   DEFAULT_DELAY_LANZAMIENTO, INCREMENTO_TIEMPO, INTERVALO_ANIMACION,
                   MIN_VELOCIDAD, MAX_VELOCIDAD,
                   UMBRAL_INTERCEPCION, MIN_ALTURA, MAX_ALTURA)
from physics import calcular_tiempo_vuelo_enemigo, calcular_posicion_enemigo, calcular_posicion_misil
from optimizer import encontrar_parametros_optimos, validar_impacto_suelo, validar_altura_intercepcion
from ui_components import crear_panel_control, crear_info_panel, crear_plot, mostrar_valores_optimos

# Configurar backend de matplotlib
matplotlib.use("TkAgg")

class SimuladorMisiles:
    def __init__(self, root):
        """Constructor de la clase SimuladorMisiles"""
        self.root = root
        self.root.title("Simulador de Interceptación de Misiles")
        self.root.geometry("1000x800")
        
        # Inicializar parámetros
        self.altura_enemigo = DEFAULT_ALTURA_ENEMIGA
        self.distancia_defensa = DEFAULT_DISTANCIA_DEFENSA
        self.velocidad_misil = DEFAULT_VELOCIDAD_MISIL
        self.angulo_misil = DEFAULT_ANGULO_MISIL
        self.delay_lanzamiento = DEFAULT_DELAY_LANZAMIENTO
        
        # Estado de simulación
        self.simulacion_activa = False
        self.intercepcion = False
        self.impacto_enemigo = False
        self.anim = None
        self.tiempo = 0
        self.incremento_tiempo = INCREMENTO_TIEMPO
        
        # Trayectorias
        self.enemigo_x = []
        self.enemigo_y = []
        self.misil_x = []
        self.misil_y = []
        
        # Calcular tiempo de vuelo del misil enemigo
        self.tiempo_vuelo_enemigo = calcular_tiempo_vuelo_enemigo(self.altura_enemigo)
        
        # Crear componentes de UI
        crear_panel_control(self.root, self)
        crear_info_panel(self.root, self)
        crear_plot(self.root, self)
        
        # Inicializar elementos gráficos
        self.reiniciar_simulacion()
    
    def actualizar_limites_plot(self):
        """Actualiza los límites del gráfico según los parámetros actuales"""
        self.ejes.set_xlim(-5, self.distancia_defensa + 5)
        self.ejes.set_ylim(-0.5, self.altura_enemigo + 2)
        self.lienzo.draw_idle()
    
    def actualizar_altura(self, valor):
        """Actualiza la altura del misil enemigo"""
        try:
            nuevo_valor = float(valor)
            if MIN_ALTURA <= nuevo_valor <= MAX_ALTURA:
                self.altura_enemigo = nuevo_valor
                self.entrada_altura.delete(0, tk.END)
                self.entrada_altura.insert(0, f"{self.altura_enemigo:.1f}")
                self.tiempo_vuelo_enemigo = calcular_tiempo_vuelo_enemigo(self.altura_enemigo)
                self.actualizar_limites_plot()
                self.reiniciar_simulacion()
        except ValueError:
            self.entrada_altura.delete(0, tk.END)
            self.entrada_altura.insert(0, f"{self.altura_enemigo:.1f}")
    
    def actualizar_distancia(self, valor):
        """Actualiza la distancia horizontal"""
        try:
            nuevo_valor = float(valor)
            if nuevo_valor > 0:
                self.distancia_defensa = nuevo_valor
                self.entrada_distancia.delete(0, tk.END)
                self.entrada_distancia.insert(0, f"{self.distancia_defensa:.1f}")
                self.actualizar_limites_plot()
                self.reiniciar_simulacion()
        except ValueError:
            self.entrada_distancia.delete(0, tk.END)
            self.entrada_distancia.insert(0, f"{self.distancia_defensa:.1f}")
    
    def actualizar_velocidad(self, valor):
        """Actualiza la velocidad del misil antiaéreo"""
        try:
            nuevo_valor = float(valor)
            if MIN_VELOCIDAD <= nuevo_valor <= MAX_VELOCIDAD:
                self.velocidad_misil = nuevo_valor
                self.entrada_velocidad.delete(0, tk.END)
                self.entrada_velocidad.insert(0, f"{self.velocidad_misil:.1f}")
                self.reiniciar_simulacion()
        except ValueError:
            self.entrada_velocidad.delete(0, tk.END)
            self.entrada_velocidad.insert(0, f"{self.velocidad_misil:.1f}")
    
    def actualizar_angulo(self, valor):
        """Actualiza el ángulo de lanzamiento del misil antiaéreo"""
        try:
            nuevo_valor = float(valor)
            if 0 <= nuevo_valor <= 90:
                self.angulo_misil = nuevo_valor
                self.entrada_angulo.delete(0, tk.END)
                self.entrada_angulo.insert(0, f"{self.angulo_misil:.1f}")
                self.reiniciar_simulacion()
        except ValueError:
            self.entrada_angulo.delete(0, tk.END)
            self.entrada_angulo.insert(0, f"{self.angulo_misil:.1f}")
    
    def actualizar_delay(self, valor):
        """Actualiza el delay de lanzamiento del misil antiaéreo"""
        try:
            nuevo_valor = float(valor)
            if nuevo_valor >= 0:
                self.delay_lanzamiento = nuevo_valor
                self.entrada_delay.delete(0, tk.END)
                self.entrada_delay.insert(0, f"{self.delay_lanzamiento:.1f}")
                self.reiniciar_simulacion()
        except ValueError:
            self.entrada_delay.delete(0, tk.END)
            self.entrada_delay.insert(0, f"{self.delay_lanzamiento:.1f}")
    
    def reiniciar_simulacion(self):
        """Reinicia la simulación a su estado inicial"""
        if self.anim and self.anim.event_source:
            self.anim.event_source.stop()
        
        # Reiniciar variables
        self.tiempo = 0
        self.enemigo_x = []
        self.enemigo_y = []
        self.misil_x = []
        self.misil_y = []
        self.simulacion_activa = False
        self.intercepcion = False
        self.impacto_enemigo = False
        
        # Limpiar gráfico
        self.linea_enemigo.set_data([], [])
        self.linea_misil.set_data([], [])
        self.punto_enemigo.set_data([], [])
        self.punto_misil.set_data([], [])
        
        # Dibujar posiciones estáticas
        self.inicio_enemigo.set_data([self.distancia_defensa], [self.altura_enemigo])
        self.defensa_posicion.set_data([0], [0])
        self.ciudad_posicion.set_data([self.distancia_defensa], [0])
        
        self.etiqueta_info.config(text="Simulación reiniciada")
        self.lienzo.draw_idle()
        
        # Configurar estado de los botones
        self.boton_iniciar.config(state=tk.NORMAL)
        self.boton_detener.config(state=tk.DISABLED)
    
    def iniciar_simulacion(self):
        """Inicia la simulación de la trayectoria de los misiles"""
        if not self.simulacion_activa:
            self.simulacion_activa = True
            self.boton_iniciar.config(state=tk.DISABLED)
            self.boton_detener.config(state=tk.NORMAL)
            
            # Configurar animación
            self.anim = FuncAnimation(
                self.figura, 
                self.animar, 
                frames=None,
                interval=INTERVALO_ANIMACION, 
                blit=False, 
                repeat=False,
                cache_frame_data=False  
            )
            self.lienzo.draw()
    
    def detener_simulacion(self):
        """Detiene la simulación en curso"""
        if self.simulacion_activa:
            self.simulacion_activa = False
            if self.anim and self.anim.event_source:
                self.anim.event_source.stop()
            self.boton_iniciar.config(state=tk.NORMAL)
            self.boton_detener.config(state=tk.DISABLED)
    
    def calcular_parametros_optimos(self):
        """Calcula los parámetros óptimos para interceptar el misil enemigo"""
        try:
            # Obtener resultado de la optimización usando el delay actual
            resultado = encontrar_parametros_optimos(
                self.altura_enemigo,
                self.distancia_defensa,
                MIN_VELOCIDAD,
                MAX_VELOCIDAD,
                self.delay_lanzamiento
            )
            
            if resultado.success and resultado.fun < UMBRAL_INTERCEPCION:
                # Extraer los valores optimizados
                angulo_opt, vel_opt, tiempo_opt = resultado.x
                
                # Actualizar los campos de entrada directamente
                self.entrada_angulo.delete(0, tk.END)
                self.entrada_angulo.insert(0, f"{angulo_opt:.1f}")
                
                self.entrada_velocidad.delete(0, tk.END)
                self.entrada_velocidad.insert(0, f"{vel_opt:.1f}")
                
                # Actualizar los valores internos
                self.angulo_misil = angulo_opt
                self.velocidad_misil = vel_opt
                
                # Calcular altura de interceptación
                altura_intercepcion = calcular_posicion_enemigo(self.altura_enemigo, tiempo_opt)
                
                # Mostrar resultados
                mostrar_valores_optimos(resultado, tiempo_opt, altura_intercepcion)
                
                self.etiqueta_info.config(
                    text=f"Parámetros óptimos calculados (delay={self.delay_lanzamiento:.1f}s)"
                )
                return True
            else:
                messagebox.showwarning(
                    "Optimización", 
                    "No se encontró una solución viable con los parámetros actuales"
                )
                return False
                
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Error al calcular parámetros óptimos: {str(e)}"
            )
            return False
    
    def animar(self, frame):
        """Función para animar la simulación frame por frame"""
        if not self.simulacion_activa:
            return
            
        # Incrementar tiempo
        self.tiempo += self.incremento_tiempo
        
        # Calcular posición del misil enemigo (caída libre)
        altura_enemigo = calcular_posicion_enemigo(self.altura_enemigo, self.tiempo)
        
        # Verificar si el misil enemigo impactó el suelo
        if validar_impacto_suelo(altura_enemigo) and not self.impacto_enemigo:
            self.impacto_enemigo = True
            self.etiqueta_info.config(text="¡El misil enemigo impactó en la ciudad!")
            self.detener_simulacion()
            return
                
        self.enemigo_x.append(self.distancia_defensa)
        self.enemigo_y.append(altura_enemigo)
        
        # Calcular posición del misil antiaéreo
        misil_x, misil_y = calcular_posicion_misil(
            self.angulo_misil, 
            self.velocidad_misil, 
            self.tiempo,
            self.delay_lanzamiento
        )
            
        self.misil_x.append(misil_x)
        self.misil_y.append(misil_y)
        
        # Verificar intercepción
        if not self.intercepcion and not self.impacto_enemigo:
            dx = self.misil_x[-1] - self.enemigo_x[-1]
            dy = self.misil_y[-1] - self.enemigo_y[-1]
            distancia = np.sqrt(dx**2 + dy**2)
            
            # Verificar umbral de intercepción y altura mínima
            if distancia < UMBRAL_INTERCEPCION:
                if validar_altura_intercepcion(self.enemigo_y[-1]):
                    self.intercepcion = True
                    self.etiqueta_info.config(
                        text=f"¡Intercepción exitosa a {self.enemigo_y[-1]:.2f} km de altura y {self.tiempo:.2f} segundos!"
                    )
                else:
                    self.etiqueta_info.config(
                        text="Intercepción fallida: altura demasiado baja (< 0.1 km)"
                    )
                    self.detener_simulacion()
        
        # Actualizar datos del gráfico
        self.linea_enemigo.set_data(self.enemigo_x, self.enemigo_y)
        self.linea_misil.set_data(self.misil_x, self.misil_y)
        self.punto_enemigo.set_data([self.enemigo_x[-1]], [self.enemigo_y[-1]])
        self.punto_misil.set_data([self.misil_x[-1]], [self.misil_y[-1]])
        
        # Detener simulación si ambos misiles están en el suelo o si hay intercepción
        if (self.impacto_enemigo and self.misil_y[-1] <= 0) or self.intercepcion:
            if not self.intercepcion and self.impacto_enemigo:
                self.etiqueta_info.config(text="Simulación terminada. La intercepción falló.")
            self.detener_simulacion()
        
        return (self.linea_enemigo, self.linea_misil, 
                self.punto_enemigo, self.punto_misil)