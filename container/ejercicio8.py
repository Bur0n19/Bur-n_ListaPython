import customtkinter as ctk
import pandas as pd

class Ejercicio8(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.listaNumeros = []

        self.titulo = ctk.CTkLabel(self, text="8. Suma de N números", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=10)

        self.entradaNumero = ctk.CTkEntry(self, placeholder_text="Ingresa un numero", width=250)
        self.entradaNumero.pack(pady=10)

        self.btnCalcular = ctk.CTkButton(self, text="Guardar Numero", command=self.sumatoria)
        self.btnCalcular.pack(pady=10)

        self.total = ctk.CTkLabel(self, text=f"Suma total: 0", font=("Arial", 18, "bold"))
        self.total.pack(pady=10)

        self.alertas = ctk.CTkLabel(self, text="", text_color="red")
        self.alertas.pack(pady=5)

        self.caja_tabla = ctk.CTkTextbox(self, width=600, height=200, font=("Courier New", 12))
        self.caja_tabla.pack(pady=10)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=10)

    def sumatoria(self):
        try:
            numero = float(self.entradaNumero.get())
            self.alertas.configure(text="")
            self.listaNumeros.append(numero)
            self.suma = sum(self.listaNumeros)
            self.total.configure(text=f"Suma total: {self.suma}")
            self.entradaNumero.delete(0, 'end')
            self.actualizar_tabla_visual()
        except ValueError:
            self.alertas.configure(text="Ingresa un número válido para la suma", text_color="red")

    def actualizar_tabla_visual(self):
        df = pd.DataFrame(self.listaNumeros, columns=["Numero"])

        self.caja_tabla.delete("1.0", "end")
        self.caja_tabla.insert("1.0", df.to_string(index=False))



