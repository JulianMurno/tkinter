import tkinter as tk
from tkinter import messagebox, ttk


def generar_recibo():
    recibo = ""
    total = 0

    # Agregar datos del cliente al recibo
    nombre_cliente = entry_nombre_cliente.get().strip()
    dato_numerico = entry_dato_numerico.get().strip()

    if not nombre_cliente or not dato_numerico.isdigit():
        messagebox.showerror("Error", "Por favor, ingrese un nombre y un dato numérico válidos.")
        return

    recibo += f"{'Recibo de Facturación':^50}\n"
    recibo += "-" * 50 + "\n"
    recibo += f"Cliente: {nombre_cliente}\n"
    recibo += f"CUIL: {dato_numerico}\n"
    recibo += "-" * 50 + "\n"
    recibo += f"{'Servicio':<30}{'Cantidad':<10}{'Subtotal':>10}\n"
    recibo += "-" * 50 + "\n"

    # Agregar detalles de la factura
    for x, item in enumerate(variables_basico):
        if item.get() > 0:
            subtotal = int(item.get()) * precios_basico[x]
            recibo += f'{lista_basico[x]:<30}{item.get():<10}{f"$ {subtotal}":>10}\n'
            total += subtotal

    for x, item in enumerate(variables_standard):
        if item.get() > 0:
            subtotal = int(item.get()) * precios_standard[x]
            recibo += f'{lista_standard[x]:<30}{item.get():<10}{f"$ {subtotal}":>10}\n'
            total += subtotal

    for x, item in enumerate(variables_premium):
        if item.get() > 0:
            subtotal = int(item.get()) * precios_premium[x]
            recibo += f'{lista_premium[x]:<30}{item.get():<10}{f"$ {subtotal}":>10}\n'
            total += subtotal

    for x, item in enumerate(variables_personalizados):
        if item.get() > 0:
            subtotal = int(item.get()) * precios_personalizados[x]
            recibo += f'{lista_personalizados[x]:<30}{item.get():<10}{f"$ {subtotal}":>10}\n'
            total += subtotal

    recibo += "-" * 50 + "\n"
    recibo += f'{"Total:":<30}{"":<10}{f"$ {total}":>10}\n'

    # Mostrar el recibo en el widget de texto
    texto_recibo.delete(1.0, tk.END)
    texto_recibo.insert(tk.END, recibo)

    recibo = ""
    total = 0

    # Agregar datos del cliente al recibo
    nombre_cliente = entry_nombre_cliente.get().strip()
    dato_numerico = entry_dato_numerico.get().strip()

    if not nombre_cliente or not dato_numerico.isdigit():
        messagebox.showerror("Error", "Por favor, ingrese un nombre y un dato numérico válidos.")
        return

    recibo += f"Cliente: {nombre_cliente}\n"
    recibo += f"CUIL: {dato_numerico}\n"
    recibo += "-" * 50 + "\n"

    # Agregar detalles de la factura
    for x, item in enumerate(variables_basico):
        if item.get() > 0:
            recibo += f'{lista_basico[x].ljust(25)}{str(item.get()).rjust(5)}{f"$ {int(item.get()) * precios_basico[x]}".rjust(15)}\n'
            total += item.get() * precios_basico[x]

    for x, item in enumerate(variables_standard):
        if item.get() > 0:
            recibo += f'{lista_standard[x].ljust(25)}{str(item.get()).rjust(5)}{f"$ {int(item.get()) * precios_standard[x]}".rjust(15)}\n'
            total += item.get() * precios_standard[x]

    for x, item in enumerate(variables_premium):
        if item.get() > 0:
            recibo += f'{lista_premium[x].ljust(25)}{str(item.get()).rjust(5)}{f"$ {int(item.get()) * precios_premium[x]}".rjust(15)}\n'
            total += item.get() * precios_premium[x]

    for x, item in enumerate(variables_personalizados):
        if item.get() > 0:
            recibo += f'{lista_personalizados[x].ljust(25)}{str(item.get()).rjust(5)}{f"$ {int(item.get()) * precios_personalizados[x]}".rjust(15)}\n'
            total += item.get() * precios_personalizados[x]

    recibo += "-" * 50 + "\n"
    recibo += f'Total:{"$" + str(total).rjust(2)}'

    texto_recibo.delete(1.0, tk.END)
    texto_recibo.insert(tk.END, recibo)


def guardar():
    with open("recibo.txt", "w") as archivo:
        archivo.write(texto_recibo.get(1.0, tk.END))
    messagebox.showinfo("Guardado", "Recibo guardado correctamente.")


def resetear():
    for var in variables_basico + variables_standard + variables_premium + variables_personalizados:
        var.set(0)
    texto_recibo.delete(1.0, tk.END)
    entry_nombre_cliente.delete(0, tk.END)
    entry_dato_numerico.delete(0, tk.END)


def habilitar_columnas():
    seleccion = variable_paquete.get()

    if seleccion == "Personalizado":
        for btn in checkbuttons_basico + checkbuttons_standard + checkbuttons_premium:
            btn.config(state="normal")
        for btn in checkbuttons_personalizado:
            btn.config(state="normal")
    elif seleccion == "Básico":
        deshabilitar_columnas()
        for btn in checkbuttons_basico:
            btn.config(state="normal")
    elif seleccion == "Standard":
        deshabilitar_columnas()
        for btn in checkbuttons_basico + checkbuttons_standard:
            btn.config(state="normal")
    elif seleccion == "Premium":
        deshabilitar_columnas()
        for btn in checkbuttons_basico + checkbuttons_standard + checkbuttons_premium:
            btn.config(state="normal")
    else:
        deshabilitar_columnas()


def deshabilitar_columnas():
    for btn in checkbuttons_basico + checkbuttons_standard + checkbuttons_premium + checkbuttons_personalizado:
        btn.config(state="disabled")


# Configuración de la ventana principal
aplicacion = tk.Tk()
aplicacion.title("Facturación Global Dream")
aplicacion.config(bg="#e35165")
aplicacion.resizable(False, False)

# Establecer el ícono de la aplicación
aplicacion.iconbitmap("logo.ico")

# Estilos
estilo_label = {"font": ("Arial", 12, "bold"), "bg": "#e35165"}
estilo_checkbutton = {"bg": "#e35165", "activebackground": "#ffffff"}
estilo_boton = {"bg": "#0984e3", "fg": "white", "font": ("Arial", 10, "bold"), "relief": "raised"}

# Línea superior para el cliente
frame_cliente = tk.Frame(aplicacion, bg="#ffffff")
frame_cliente.grid(row=0, column=0, columnspan=6, pady=10, sticky="w")

icono = tk.PhotoImage(file="logo.png")
icono = icono.subsample(2, 2)
label_icono = tk.Label(frame_cliente, image=icono, bg="#ffffff")
label_icono.pack(side="left", padx=10)

tk.Label(frame_cliente, text="Cliente:", **estilo_label).pack(side="left", padx=5)
entry_nombre_cliente = tk.Entry(frame_cliente, font=("Arial", 12), width=20)
entry_nombre_cliente.pack(side="left", padx=5)

tk.Label(frame_cliente, text="CUIL:", **estilo_label).pack(side="left", padx=5)
entry_dato_numerico = tk.Entry(frame_cliente, font=("Arial", 12), width=20)
entry_dato_numerico.pack(side="left", padx=5)

# Listas de ítems del menú y precios
lista_basico = ["Diseño de hasta 3 páginas", "Plantilla Prediseñada", "Hosting básico"]
lista_standard = ["Diseño de hasta 6 páginas", "Maquetado Responsive", "Capacitación básica CMS", "Hosting con BackUp semanales", "1 revisión p/año de diseño."]
lista_premium = ["Diseño de hasta 10 páginas", "Diseño customizado y único", "Capacitación completa CMS", "Hosting con BackUp diarios", "Implementación de ChatBots", "3 revisiones p/año de diseño"]
lista_personalizados = ["Diseño gráfico", "Branding"]

# Precios
precios_basico = [400000, 193000, 193000]
precios_standard = [400000, 159000, 159000, 400000, 159000]
precios_premium = [500000, 600000, 200000, 200000, 200000, 200000]
precios_personalizados = [70000, 70000]

# Asignacion de precio al item correspondiente
variables_basico = [tk.IntVar() for _ in lista_basico]
variables_standard = [tk.IntVar() for _ in lista_standard]
variables_premium = [tk.IntVar() for _ in lista_premium]
variables_personalizados = [tk.IntVar() for _ in lista_personalizados]

# Configurar encabezados
encabezados = ["Básico", "Standard", "Premium", "Adicionales"]
for col, texto in enumerate(encabezados):
    tk.Label(aplicacion, text=texto, **estilo_label).grid(row=1, column=col, pady=5)

# Configurar checkbuttons
def configurar_checkbuttons(lista, variables, columna):
    checkbuttons = []
    for i, texto in enumerate(lista):
        cb = tk.Checkbutton(aplicacion, text=texto, variable=variables[i], **estilo_checkbutton)
        cb.grid(row=i + 2, column=columna, sticky="w")
        checkbuttons.append(cb)
    return checkbuttons

checkbuttons_basico = configurar_checkbuttons(lista_basico, variables_basico, 0)
checkbuttons_standard = configurar_checkbuttons(lista_standard, variables_standard, 1)
checkbuttons_premium = configurar_checkbuttons(lista_premium, variables_premium, 2)
checkbuttons_personalizado = configurar_checkbuttons(lista_personalizados, variables_personalizados, 3)

# Selección de paquetes
variable_paquete = tk.StringVar()
opciones_paquete = ["-----", "Básico", "Standard", "Premium", "Personalizado"]
variable_paquete.set(opciones_paquete[0])
menu_paquete = ttk.OptionMenu(aplicacion, variable_paquete, *opciones_paquete, command=lambda _: habilitar_columnas())
menu_paquete.grid(row=1, column=4, padx=10, pady=5)

# Caja de texto para el recibo
texto_recibo = tk.Text(aplicacion, width=50, height=10, bg="#dfe6e9", font=("Courier", 10))
texto_recibo.grid(row=8, column=0, columnspan=4, pady=10)

# Botones de recibo
frame_botones = tk.Frame(aplicacion, bg="#e35165")
frame_botones.grid(row=9, column=0, columnspan=6, pady=10)

tk.Button(frame_botones, text="Generar Recibo", command=generar_recibo, **estilo_boton).pack(side="left", padx=10)
tk.Button(frame_botones, text="Guardar", command=guardar, **estilo_boton).pack(side="left", padx=10)
tk.Button(frame_botones, text="Resetear", command=resetear, **estilo_boton).pack(side="left", padx=10)

# Ejecucion
deshabilitar_columnas()
aplicacion.mainloop()
