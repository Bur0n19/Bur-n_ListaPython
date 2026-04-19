import customtkinter as ctk
import pandas as pd


class Ejercicio1(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.lista_usuarios = []

        self.titulo = ctk.CTkLabel(self, text="1. Sistema de aumento de sueldos", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=10)

        self.entrada1 = ctk.CTkEntry(self, placeholder_text="Nombre del empleado", width=250)
        self.entrada1.pack(pady=5)

        self.entrada2 = ctk.CTkEntry(self, placeholder_text="Sueldo actual", width=250)
        self.entrada2.pack(pady=5)

        self.btnCalcular = ctk.CTkButton(self, text="Calcular y Guardar", command=self.aumentoSueldos)
        self.btnCalcular.pack(pady=10)

        self.resultado_label = ctk.CTkLabel(self, text = "")
        self.resultado_label.pack(pady=10)

        self.titulo_tabla = ctk.CTkLabel(self, text="Historial de Empleados:", font=("Arial", 12, "italic"))
        self.titulo_tabla.pack(pady=(10, 0))

        self.caja_tabla = ctk.CTkTextbox(self, width=600, height=200, font=("Courier New", 12))
        self.caja_tabla.pack(pady=10)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=10)

    def aumentoSueldos(self):
        nombre = self.entrada1.get().strip()
        texto_sueldo = self.entrada2.get()

        if not nombre:
            self.resultado_label.configure(text="Error: Ingresa el nombre del empleado", text_color="red")
            return
        try:
            sueldo = float(texto_sueldo)
            if sueldo < 0:
                self.resultado_label.configure(text="Error: El sueldo no puede ser negativo", text_color="red")
                return
            if sueldo > 100000:
                self.resultado_label.configure(text="Error: Sueldo fuera de rango permitido", text_color="red")
                return

            if sueldo < 4000:
                nuevoSueldo = sueldo * 1.15
            elif 4000 <= sueldo <= 7000:
                nuevoSueldo = sueldo * 1.10
            else:
                nuevoSueldo = sueldo * 1.08

            registro = {
                "Empleado": nombre,
                "Sueldo Base": sueldo,
                "Aumento": nuevoSueldo - sueldo,
                "Sueldo Final": nuevoSueldo
            }
            self.lista_usuarios.append(registro)

            self.resultado_label.configure(text=f"Guardado: {nombre} -> ${nuevoSueldo:.2f}", text_color="green")

            self.actualizar_tabla_visual()

            self.entrada1.delete(0, 'end')
            self.entrada2.delete(0, 'end')
            self.entrada1.focus()

        except ValueError:
            self.resultado_label.configure(text="Error: Ingresa un sueldo numérico válido", text_color="red")

    def actualizar_tabla_visual(self):
        df = pd.DataFrame(self.lista_usuarios)

        self.caja_tabla.delete("1.0", "end")
        self.caja_tabla.insert("1.0", df.to_string(index=False))