# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 10:15:10 2023

@authors: Arturo Alvarez & Marcelo Querevalú
"""
# Importamos las librerías
import tkinter as tk
from tkinter import ttk

import numpy as np
from numpy import pi, sin, cos, sqrt, arccos, arctan2

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D


# Función para actualizar el valor en los Label
def update_slider_value1(val):
    integer_val = int(float(val))  # Convertir el valor a entero
    value_label1.config(text=f"{integer_val} °")
    return(integer_val)

def update_slider_value2(val):
    try:
        integer_val = int(float(val))  # Convertir el valor a entero
        value_label2.config(text=f"{integer_val} °")
        gamma = obtener_gamma()
        L2 = obtener_entry()
        prop = obtener_combo()
        rotar(integer_val, L2, prop, gamma)
        return(integer_val)
    except:
        pass

# Funciones para obtener los valores en las entradas de la interfaz
def obtener_entry():
    integer_val = float(longitud_entry.get())  # Convertir el valor a entero
    return(integer_val)

def obtener_combo():
    integer_val = float(proporcion.get())  # Convertir el valor a entero
    return(integer_val)

def obtener_gamma():
    integer_val = int(slider1.get())  # Convertir el valor a entero
    return(integer_val)

def update():

    value_label2.config(text="0 °")
    gamma = obtener_gamma()
    L2 = obtener_entry()
    prop = obtener_combo()
    rotar(0, L2, prop, gamma)

def draw_trayect(L2, prop, gamma):
    
    increment = 0.035

    Theta = np.arange(0, 2*pi, increment)
    
    P = np.zeros((2, len(Theta)))
    
    for index, angle in enumerate(Theta, start=0):
        
        angle_rad = angle
        gamma_rad = gamma*pi/180
        L1 = 2 * L2
        L3 = prop * L2
        L4 = L3
        BP = prop * L2
        AP = sqrt(BP**2 + L3**2 - 2*L3*BP*cos(gamma_rad))
        
        # Puntos Fijos:
        O_4 = [L1, 0]
        
        a = [L2 * cos(angle_rad), L2 * sin(angle_rad)]
    
        beta = arccos((L2**2 + L1**2 - 2*L1*L2*cos(angle_rad) - L3**2 - L4**2)/(2*L3*L4))
        
        R = L2*(cos(angle_rad)*cos(beta) + sin(angle_rad)*sin(beta) + cos(angle_rad)) - L1*cos(beta) - L1
        Q = L2*(cos(angle_rad)*sin(beta) - sin(angle_rad)*cos(beta) - sin(angle_rad)) - L1*sin(beta)
        
        S = - Q
        T = 2*R
        U = Q
        
        alpha_1 = 2*arctan2((-T + sqrt(T**2 - 4*S*U)), (2*S))
        
        b = [O_4[0] - L4*cos(pi - alpha_1), L4*sin(pi - alpha_1)]
    
        phi = (pi - gamma_rad)/2
        delta = arctan2((b[1] - a[1]),(b[0] - a[0]))
        
        omega = phi + delta
        
        p = [a[0] + AP*cos(omega), a[1] + AP*sin(omega)]
        
        P[:, index] = p
        
    # Matriz de la trayectoria:
    tray = np.append(P, [[P[0, 0]], [P[1,0]]], axis=1)
    
    linea_trayectoria = Line2D(tray[0,:], tray[1, :], color='#bc4749')
    ax1.add_line(linea_trayectoria)
    
    canvas1.draw()

def update_canvas(O_4,a,b,p,L2,prop, gamma):
    # Borrar cualquier línea anterior en el canvas
    ax1.clear()
    ax1.set_xlim(-1.4*prop*L2, 2.6*prop*L2)
    ax1.set_ylim(-1.1*prop*L2, 2.1*prop*L2)
    
    # Dibujar L2
    ax1.plot(0, 0, 'go', color='white')
    ax1.plot([0, a[0]], [0, a[1]], color='white', lw=2)
    
    # Dibujar L3
    ax1.plot([a[0], b[0]], [a[1], b[1]], color='white', lw=2)
    
    # Dibujar L4
    ax1.plot(O_4[0], 0, 'go', color='white')
    ax1.plot([O_4[0], b[0]], [0, b[1]], color='white', lw=2)
    
    # Dibujar BP
    ax1.plot([p[0], b[0]], [p[1], b[1]], color='white', lw=2)
    
    # Dibujar AP
    ax1.plot([p[0], a[0]], [p[1], a[1]], color='white', lw=2)
    
    ax1.plot(p[0], p[1], 'go', color='#bc4749')
    draw_trayect(L2, prop, gamma)

    # Actualizar el canvas
    canvas1.draw()

def rotar(angle, L2, prop, gamma):
    
    angle_rad = angle*pi/180
    gamma_rad = gamma*pi/180
    L1 = 2 * L2
    L3 = prop * L2
    L4 = L3
    BP = prop * L2
    AP = sqrt(BP**2 + L3**2 - 2*L3*BP*cos(gamma_rad))
    
    # Puntos Fijos:
    O_4 = [L1, 0]

    a = [L2 * cos(angle_rad), L2 * sin(angle_rad)]

    beta = arccos((L2**2 + L1**2 - 2*L1*L2*cos(angle_rad) - L3**2 - L4**2)/(2*L3*L4))
    
    R = L2*(cos(angle_rad)*cos(beta) + sin(angle_rad)*sin(beta) + cos(angle_rad)) - L1*cos(beta) - L1
    Q = L2*(cos(angle_rad)*sin(beta) - sin(angle_rad)*cos(beta) - sin(angle_rad)) - L1*sin(beta)
    
    S = - Q
    T = 2*R
    U = Q
    
    alpha_1 = 2*arctan2((-T + sqrt(T**2 - 4*S*U)), (2*S))
    
    b = [O_4[0] - L4*cos(pi - alpha_1), L4*sin(pi - alpha_1)]

    phi = (pi - gamma_rad)/2
    delta = arctan2((b[1] - a[1]),(b[0] - a[0]))
    
    omega = phi + delta
    
    p = [a[0] + AP*cos(omega), a[1] + AP*sin(omega)]
        
    update_canvas(O_4,a,b,p,L2,prop, gamma)

animating = False

# Función para iniciar la animación
def start_animation():
    try:
        global animating, current_angle
        if animating:
            # Incrementar el ángulo actual (puedes ajustar la velocidad cambiando el valor 1)
            current_angle += 5
            if current_angle >= 360:
                current_angle = 0  # Reiniciar el ángulo cuando llegue a 360
            # Actualizar el slider2 y llamar a la función rotar con el nuevo ángulo
            rotar(current_angle, obtener_entry(), obtener_combo(), obtener_gamma())
            # Programar una llamada recursiva a start_animation después de un breve retraso
            root.after(10, start_animation)
    except:
        pass

# Función para detener la animación
def stop_animation():
    global animating
    animating = False

def toggle_animation():
    global animating, current_angle
    animating = not animating  # Cambiar el estado de animación
    if animating:
        # Si se está animando, inicia la animación
        current_angle = 0
        start_animation()
    else:
        # Si se está deteniendo, detén la animación
        stop_animation()

# Crear figura 1 de Matplotlib
fig1 = Figure(figsize=(5.625, 4.5), dpi=100)
fig1.patch.set_facecolor('#114045')

ax1 = fig1.add_subplot(111)
ax1.tick_params(axis='x', colors='#f0f7da')
ax1.tick_params(axis='y', colors='#f0f7da')

ax1.spines['bottom'].set_color('#f0f7da')
ax1.spines['top'].set_color('#f0f7da') 
ax1.spines['right'].set_color('#f0f7da')
ax1.spines['left'].set_color('#f0f7da')

ax1.set_xlim(-1.4, 2.6)
ax1.set_ylim(-1.1, 2.1)
ax1.set_aspect('equal')
ax1.set_facecolor("#0b1c24")
ax1.tick_params(axis='both', labelsize=7)

# Matriz de rotación inicial (0 grados)
rotation_matrix = np.array([[1, 0],
                             [0, 1]])

# Crear la ventana principal
root = tk.Tk()
root.iconbitmap(r'./icon.ico')
root.title("UNT - INGENIERÍA MECATRÓNICA - TEORÍA DE MAQUINAS Y MECANISMOS")
root.configure(bg="#0f373a")
root.option_add('*TButton*Font', 'CenturyGothic 12')
root.geometry("792x490")
root.resizable(False, False)

# Crear marcos para el lado izquierdo y derecho
left_frame = tk.Frame(root, bg="#114045")
left_frame.place(x=20, y=20)

right_frame = tk.Frame(root, bg="#547473")
right_frame.place(x=210, y=20)

# Configurar colores oscuros
dark_color = "#114045"

# Crear lienzo 1 de Matplotlib para tkinter
canvas1 = FigureCanvasTkAgg(fig1, master=right_frame)
canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Etiqueta "Longitud de manivela"
longitud_label = tk.Label(left_frame, text="Longitud de manivela", bg="#114045", fg="white")
longitud_label.grid(row=0, column=0, padx=10, pady=(10, 5))

# Cuadro de entrada para la longitud de manivela
longitud_entry = tk.Entry(left_frame, bg="white", fg="black", width=20)
longitud_entry.grid(row=1, column=0, padx=10, pady=(0, 10))

# Lista plegable "Proporción entre eslabones"
proporciones_label = tk.Label(left_frame, text="Proporción entre eslabones", bg="#114045", fg="white")
proporciones_label.grid(row=2, column=0, padx=10, pady=(10, 5))

proporcion = ttk.Combobox(left_frame, width=17, state="readonly")
proporcion['values']=["1.5", "2", "2.5", "3", "3.5","4", "4.5", "5"]
proporcion.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="n")

# Slider "Ángulo del acoplador"
slider_label1 = tk.Label(left_frame, text="Ángulo del acoplador", bg="#114045", fg="white")
slider_label1.grid(row=4, column=0, padx=10, pady=(10, 5))

style = ttk.Style()
style.configure("TScale", sliderrelief="flat", sliderthickness=20)

slider1 = ttk.Scale(left_frame, from_=0, to=360, orient="horizontal", style="TScale", command=update_slider_value1)
slider1.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="nsew")

# Label para mostrar el valor del slider
value_label1 = tk.Label(left_frame, text="0 °", bg="#114045", fg="white", width=6)
value_label1.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="nsew")

# Botón "Configurar"
configurar_button = tk.Button(left_frame, text="Configurar", bg="#2a808d", fg="white", width=15,
                              relief="flat", command=update)  # Diseño minimalista sin bordes
configurar_button.grid(row=7, column=0, padx=10, pady=(10, 0))

# Boton "Animar / Detener"
animar_button = tk.Button(left_frame, text="Animar / Detener", bg="#2a808d", fg="white", width=15, relief="flat", command=toggle_animation)
animar_button.grid(row=8, column=0, padx=10, pady=(20, 0))

# Slider "Ángulo de la manivela"
slider_label2 = tk.Label(left_frame, text="Ángulo de la manivela", bg="#114045", fg="white")
slider_label2.grid(row=9, column=0, padx=10, pady=(40, 5))

style = ttk.Style()
style.configure("TScale", sliderrelief="flat", sliderthickness=20)

slider2 = ttk.Scale(left_frame, from_=0, to=360, orient="horizontal", style="TScale", command=update_slider_value2)
slider2.grid(row=10, column=0, padx=10, pady=(0, 10), sticky="nsew")

# Label para mostrar el valor del slider
value_label2 = tk.Label(left_frame, text="0 °", bg="#114045", fg="white", width=6)
value_label2.grid(row=11, column=0, padx=10, pady=(0, 10), sticky="nsew")

# Ejecutar la ventana
root.mainloop()