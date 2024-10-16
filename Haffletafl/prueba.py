import tkinter as tk
from PIL import Image, ImageTk

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

# Ejecutar el bucle principal de la aplicación
#root.mainloop()
help(tk.Label())