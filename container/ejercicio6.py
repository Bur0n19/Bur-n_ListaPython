import customtkinter as ctk
import pandas as pd

class Ejercicio6(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.intentos = 0
        self.lista_intentos =[]

        self.titulo = ctk.CTkLabel(self, text="Validación de Número (0 a 20)", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=(20, 10))

        self.instruccion = ctk.CTkLabel(self, text="Ingresa un número entero entre 0 y 20:")
        self.instruccion.pack(pady=5)

        self.entrada_numero = ctk.CTkEntry(self, placeholder_text="", width=250)
        self.entrada_numero.pack(pady=10)

        self.btn_validar = ctk.CTkButton(self, text="Validar Número", command=self.validar)
        self.btn_validar.pack(pady=10)

        self.alertas = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 14))
        self.alertas.pack(pady=10)

        self.caja_tabla = ctk.CTkTextbox(self, width=600, height=200, font=("Courier New", 12))
        self.caja_tabla.pack(pady=10)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=20)

    def validar_rango(self, num):
        return 0 <= num <= 20

    def validar(self):
        self.intentos += 1

        numero_texto = self.entrada_numero.get().strip()

        if not numero_texto:
            self.alertas.configure(text=f"El campo está vacío. (Intento {self.intentos})", text_color="red")
            return

        try:
            numero = int(numero_texto)
            self.lista_intentos.append(numero)
            self.actualizar_tabla_visual()

            if not self.validar_rango(numero):
                self.alertas.configure(text=f"El {numero} está fuera del rango. (Intento {self.intentos})",text_color="red")
                self.entrada_numero.delete(0, 'end')
            else:
                self.alertas.configure(text=f"¡Número válido: {numero}!\nTe tomó {self.intentos} intento(s).",text_color="green")
                self.intentos = 0
                self.lista_intentos.clear()
                self.entrada_numero.delete(0, 'end')

        except ValueError:
            self.alertas.configure(text=f"Ingresa solo números enteros. (Intento {self.intentos})", text_color="red")

    def actualizar_tabla_visual(self):
        if not self.lista_intentos:
            self.caja_tabla.delete("1.0", "end")
            return

        df = pd.DataFrame(self.lista_intentos, columns=["Numeros Intentados"])

        self.caja_tabla.delete("1.0", "end")
        self.caja_tabla.insert("1.0", df.to_string(index=False))