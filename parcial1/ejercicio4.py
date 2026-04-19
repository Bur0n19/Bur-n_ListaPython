import customtkinter as ctk


class Ejercicio4(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador

        self.intentos = 0

        self.titulo = ctk.CTkLabel(self, text="Validación de Número Menor a 10", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=(20, 10))

        self.instruccion = ctk.CTkLabel(self, text="Ingresa un número entero menor que 10:")
        self.instruccion.pack(pady=5)

        self.entrada_numero = ctk.CTkEntry(self, placeholder_text="Ej: 5", width=250)
        self.entrada_numero.pack(pady=10)

        self.btn_validar = ctk.CTkButton(self, text="Validar Número", command=self.validar_numero)
        self.btn_validar.pack(pady=10)

        self.alertas = ctk.CTkLabel(self, text="", text_color="red")
        self.alertas.pack(pady=5)

        self.resultados = ctk.CTkLabel(self, text="", font=("Arial", 14, "bold"))
        self.resultados.pack(pady=10)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",
                                          command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=20)

    def validar_numero(self):
        self.intentos += 1

        numero_texto = self.entrada_numero.get().strip()

        if not numero_texto:
            self.alertas.configure(text=f"Intento {self.intentos}: El campo está vacío.", text_color="red")
            self.resultados.configure(text="")
            self.entrada_numero.focus()
            return

        try:
            numero = int(numero_texto)
        except ValueError:
            self.alertas.configure(text=f"Intento {self.intentos}: Ingresa solo números enteros.", text_color="red")
            self.resultados.configure(text="")
            return

        if numero >= 10:
            self.alertas.configure(text=f"Intento {self.intentos}: El número {numero} NO es menor a 10.",text_color="red")
            self.resultados.configure(text="")
            self.entrada_numero.delete(0, 'end')
        else:
            self.alertas.configure(text="¡Validación exitosa!", text_color="green")
            self.resultados.configure(
                text=f"Número correcto ingresado: {numero}\nCantidad de intentos: {self.intentos}"
            )

            self.intentos = 0
            self.entrada_numero.delete(0, 'end')
            self.entrada_numero.focus()