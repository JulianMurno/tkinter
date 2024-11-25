import tkinter as tk
from tkinter import messagebox, ttk
from fpdf import FPDF

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

def guardar():
    recibo_texto = texto_recibo.get(1.0, tk.END).strip()
    if not recibo_texto:
        messagebox.showerror("Error", "No hay información para guardar.")
        return

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Agregar líneas del recibo al PDF
        for line in recibo_texto.split('\n'):
            pdf.cell(0, 10, txt=line, ln=True)

        # Guardar el PDF
        pdf_output_path = "recibo_facturacion.pdf"
        pdf.output(pdf_output_path)
        messagebox.showinfo("Guardado", f"Recibo guardado como {pdf_output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al guardar el PDF: {e}")

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
aplicacion.config(bg="#edf2f7")  # Fondo general azul claro suave
aplicacion.resizable(False, False)

# Establecer el ícono de la aplicación
aplicacion.iconbitmap("logo.ico")

# Estilos ajustados
estilo_label = {"font": ("Trebuchet MS", 12, "bold"), "bg": "#edf2f7", "fg": "#2d3436"}  # Texto oscuro en fondo claro
estilo_checkbutton = {"bg": "#edf2f7", "activebackground": "#ffffff", "fg": "#000000","font":("Trebuchet MS", 10, "bold")}  # Consistente con el esquema
estilo_boton = {"bg": "#0f2775", "fg": "white", "font": ("Trebuchet MS", 11, "bold"), "relief": "raised"}  # Botón azul
estilo_TMenu = ttk.Style()

estilo_TMenu.configure("TMenubutton", 
                       background="#e35165",  # Fondo del menú
                       foreground="white",  # Color del texto
                       font=("Trebuchet MS", 10, "bold"),  # Estilo de la fuente
                       borderwidth=2,  # Grosor del borde
                       relief="raised")  # Relieve para el botón

estilo_TMenu.map("TMenubutton",
                 background=[("active", "#d0455a"), ("pressed", "#c0394f")],  # Colores cuando está activo/presionado
                 foreground=[("active", "white"), ("pressed", "white")])

# Línea superior para el cliente
frame_cliente = tk.Frame(aplicacion, bg="#edf2f7")
frame_cliente.grid(row=0, column=0, columnspan=6, pady=10, sticky="w")

marca = tk.PhotoImage(file="marca.png")
marca = marca.subsample(2, 2)
label_marca = tk.Label(frame_cliente, image=marca, bg="#e35165")
label_marca.pack(side="left", padx=10)

tk.Label(frame_cliente, text="CLIENTE:", **estilo_label).pack(side="left", padx=5)
entry_nombre_cliente = tk.Entry(frame_cliente, font=("Trebuchet MS", 12), width=20)
entry_nombre_cliente.pack(side="left", padx=5)

tk.Label(frame_cliente, text="CUIL:", **estilo_label).pack(side="left", padx=5)
entry_dato_numerico = tk.Entry(frame_cliente, font=("Trebuchet MS", 12), width=20)
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
texto_recibo = tk.Text(aplicacion, width=50, height=10, bg="#ffffff", font=("Courier", 10), bd=2, relief="groove")
texto_recibo.grid(row=8, column=0, columnspan=5, pady=10)

# Botones de recibo
frame_botones = tk.Frame(aplicacion, bg="#edf2f7")
frame_botones.grid(row=9, column=0, columnspan=5, pady=10)

tk.Button(frame_botones, text="Generar Recibo", command=generar_recibo, **estilo_boton).pack(side="left", padx=10)
tk.Button(frame_botones, text="Guardar", command=guardar, **estilo_boton).pack(side="left", padx=10)
tk.Button(frame_botones, text="Resetear", command=resetear, **estilo_boton).pack(side="left", padx=10)

# Inicialización
deshabilitar_columnas()

# Ejecución
aplicacion.mainloop()
