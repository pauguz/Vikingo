import tkinter as tk

class CuentaRegresiva(tk.Frame):
    def __init__(self, parent, segundos, funcion_final, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(background="brown")

        self.segundos = segundos
        self.funcion_final = funcion_final
        self.after_id = None

        # Label del reloj
        self.label = tk.Label(
            self,
            text=self.formato_tiempo(self.segundos),
            font=("Verdana", 10),
            relief="sunken",
            borderwidth=2,
            padx=10, pady=5
        )
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.label.config(background="blue")
        # Expandir en su celda (por si se usa en layouts con grid)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def formato_tiempo(self, segundos):
        minutos = segundos // 60
        seg = segundos % 60
        return f"{minutos:02}:{seg:02}"

    def actualizar(self):
        if self.segundos > 0:
            self.label.config(text=self.formato_tiempo(self.segundos))
            self.segundos -= 1
            self.after_id = self.after(1000, self.actualizar)
        else:
            self.label.config(text="00:00")
            self.funcion_final()

    def detener(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None


class Multicuenta(tk.Frame):
    def __init__(self, parent, n, segundos, funcion_final, ac=0, *args, **kwargs):
        """
        parent: contenedor (tk root o frame)
        n: cantidad de relojes
        segundos: tiempo inicial para cada reloj
        funcion_final: callback cuando un reloj termina
        ac: índice del reloj activo al inicio
        """
        super().__init__(parent, *args, **kwargs)

        self.n = n
        self.relojes = []
        self.activo = ac

        # Crear y colocar los relojes usando grid
        for i in range(n):
            reloj = CuentaRegresiva(self, segundos, funcion_final)
            reloj.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            self.relojes.append(reloj)

        # Permitir expansión vertical
        for i in range(n):
            self.grid_rowconfigure(i, weight=0, minsize=0)
        #self.grid_columnconfigure(0, weight=1)

    def comenzar(self):
        self.relojes[self.activo].actualizar()

    def cambiar(self):
        self.relojes[self.activo].detener()
        self.activo = (self.activo + 1) % self.n
        self.relojes[self.activo].actualizar()
