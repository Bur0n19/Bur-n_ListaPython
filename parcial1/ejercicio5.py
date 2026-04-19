import customtkinter as ctk


class Ejercicio5(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador

        self.intentos = 0

        self.titulo = ctk.CTkLabel(self, text="Validación de Número (0 a 20)", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=(20, 10))

        self.instruccion = ctk.CTkLabel(self, text="Ingresa un número entero entre 0 y 20:")
        self.instruccion.pack(pady=5)

        self.entrada_numero = ctk.CTkEntry(self, placeholder_text="Ej: 15", width=250)
        self.entrada_numero.pack(pady=10)

        self.btn_validar = ctk.CTkButton(self, text="Validar Número", command=self.validar)
        self.btn_validar.pack(pady=10)

        self.alertas = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 14))
        self.alertas.pack(pady=10)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",
                                          command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=20)

    def validar_rango(self, num):
        return 0 <= num <= 20

    def validar(self):
        def validar(self):
            self.intentos += 1
            numero_texto = self.entrada_numero.get().strip()

            if not numero_texto:
                self.alertas.configure(text=f"El campo está vacío. (Intento {self.intentos})", text_color="red")
                self.entrada_numero.focus()
                return

            try:
                numero = int(numero_texto)

                if not self.validar_rango(numero):
                    self.alertas.configure(text=f"El {numero} está fuera del rango. (Intento {self.intentos})",text_color="red")
                    self.entrada_numero.delete(0, 'end')
                    self.entrada_numero.focus()
                else:
                    self.alertas.configure(text=f"¡Número válido: {numero}!\nTe tomó {self.intentos} intento(s).",text_color="green")
                    self.intentos = 0
                    self.entrada_numero.delete(0, 'end')
                    self.entrada_numero.focus()

            except ValueError:
                self.alertas.configure(text=f"Ingresa solo números enteros. (Intento {self.intentos})",text_color="red")
                self.entrada_numero.delete(0, 'end')
                self.entrada_numero.focus()