import customtkinter as ctk
import pandas as pd

class Ejercicio2(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.lista_usuariosParque = []

        self.titulo =ctk.CTkLabel(self, text="Ejercicio 2", font=("Arial", 18, "bold"))

        self.entrada1 = ctk.CTkEntry(self, placeholder_text="Nombre de usuario", width=250)
        self.entrada1.pack(pady=10)

        self.entrada2=ctk.CTkEntry(self, placeholder_text="Edad del usuario", width=250)
        self.entrada2.pack(pady=10)

        self.entrada3 = ctk.CTkEntry(self, placeholder_text = "Cantidad de juegos utilizzados", width=250)
        self.entrada3.pack(pady=10)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú", command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=10)

    def pagos_parque(self):
        try:
            nombre = self.entrada1.get()
            edad = int(self.entrada2.get())
            n_juegos = int(self.entrada3.get())
            costoInicial = n_juegos * 50

            if edad < 10:
                nuevoCosto = costoInicial * 0.75
            elif edad >= 10 and edad <=17:
                nuevoCosto = costoInicial * 0.90
            else:
                costoInicial *=1
            totalNuevo = costoInicial - nuevoCosto

            registro = {
                "Empleado": nombre,
                "Edad": edad,
                "Juegos Utilizados": n_juegos,
                "Costo Inicial": costoInicial,
                "Descuento por edad" : nuevoCosto,
            }
            self.lista_usuariosParque.append(registro)

        except:
            self.resultado_label.configure(text="Error: Datos inválidos", text_color="red")

    def recaudo_parque(self):
        try:
            print('')
        except:
            self.resultado_label.configure(text = "No hay datos que analizar", text_color="red")










