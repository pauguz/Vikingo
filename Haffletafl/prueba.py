import tkinter as tk
from PIL import Image, ImageTk
from Conteo import CuentaRegresiva, Multicuenta
def Imagenes():
    # Crear una ventana principal
    root = tk.Tk()

    # Abrir una imagen con Pillow
    imgrey = Image.open("reg.png")
    imgrey = imgrey.resize((50,50), Image.LANCZOS)
    # Convertir la imagen a un formato que Tkinter puede usar
    tk_imgrey = ImageTk.PhotoImage(imgrey)

    # Abrir una imagen con Pillow
    imgb = Image.open("vikingoblanco.png")
    imgb = imgb.resize((50,50), Image.LANCZOS)
    # Convertir la imagen a un formato que Tkinter puede usar
    tk_imgb = ImageTk.PhotoImage(imgb)

    # Abrir una imagen con Pillow
    imgn = Image.open("vikingonegro.png")
    imgn = imgn.resize((50,50), Image.LANCZOS)
    # Convertir la imagen a un formato que Tkinter puede usar
    tk_imgn = ImageTk.PhotoImage(imgn)

    # Crear un widget Label y poner la imagen en él
    labels=[tk.Label(root), tk.Label(root), tk.Label(root)]
    i=0
    for label in labels:
        label.grid(row=0, column=i)
        i+=1

    #Asignar la imagen al Label existente
    labels[0].config(image=tk_imgrey, text="1")
    labels[1].config(image=tk_imgb)
    labels[2].config(image=tk_imgn)

def struct():
    root = tk.Tk()
    root.title("Interfaz con cuenta regresiva")

    # Barra lateral
    sidebar = tk.Frame(root, width=150, bg="lightgray")
    sidebar.pack(side=tk.LEFT, fill="y")

    # Área principal
    main = tk.Frame(root, bg="white")
    main.pack(side=tk.LEFT, fill="both", expand=True)
    # Insertamos la cuenta regresiva dentro de `main`
    contador = CuentaRegresiva(main, segundos=75, funcion_final=mi_funcion)
    contador.pack(pady=20)
    root.mainloop()


def mi_funcion():
    print("⏰ ¡Tiempo cumplido!")



def multic(n: int):
    ana = tk.Tk()
    ana.title("Reloj con botón y tecla espacio")

    # Crear el contenedor principal
    main_frame = tk.Frame(ana, bg="beige")
    main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Expandir correctamente el layout
    ana.grid_rowconfigure(0, weight=1)
    ana.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    # Crear multicuenta
    multi = Multicuenta(main_frame, n=2, segundos=n, funcion_final=mi_funcion)
    multi.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    # Botón para alternar manualmente
    boton_cambiar = tk.Button(main_frame, text="⏱ Cambiar turno", command=multi.cambiar, font=("Verdana", 12, "bold"),
        bg="lightblue",relief="raised", padx=10, pady=5
    )
    boton_cambiar.grid(row=1, column=0, pady=10)

    # Iniciar primer reloj
    multi.comenzar()

    # Cambiar reloj al presionar espacio
    ana.bind("<space>", lambda e: multi.cambiar())

    ana.mainloop()

def vacio():
    a=mi_funcion()
    print(a)
    #Imprime None 




multic(20)