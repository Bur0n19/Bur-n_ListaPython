import customtkinter as ctk


class Ejercicio4(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador

        # --- Variables de clase ---
        # Reemplazamos la variable global por un atributo de la instancia
        self.intentos = 0

        # --- INTERFAZ GRÁFICA ---
        self.titulo = ctk.CTkLabel(self, text="Validación de Número Menor a 10", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=(20, 10))

        self.instruccion = ctk.CTkLabel(self, text="Ingresa un número entero menor que 10:")
        self.instruccion.pack(pady=5)

        # Entrada de texto (reemplaza a Entry y StringVar)
        self.entrada_numero = ctk.CTkEntry(self, placeholder_text="Ej: 5", width=250)
        self.entrada_numero.pack(pady=10)

        # Botón de validación
        self.btn_validar = ctk.CTkButton(self, text="Validar Número", command=self.validar_numero)
        self.btn_validar.pack(pady=10)

        # Etiquetas para mostrar alertas y resultados
        self.alertas = ctk.CTkLabel(self, text="", text_color="red")
        self.alertas.pack(pady=5)

        self.resultados = ctk.CTkLabel(self, text="", font=("Arial", 14, "bold"))
        self.resultados.pack(pady=10)

        # Botón para regresar al menú principal
        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",
                                          command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=20)

    # --- LÓGICA DEL PROGRAMA ---
    def validar_numero(self):
        # 1. Aumentamos el contador de intentos cada vez que se presiona el botón
        self.intentos += 1

        # 2. Obtenemos el texto ingresado
        numero_texto = self.entrada_numero.get().strip()

        # Validación A: Campo vacío
        if not numero_texto:
            self.alertas.configure(text=f"Intento {self.intentos}: El campo está vacío.", text_color="red")
            self.resultados.configure(text="")  # Limpiamos resultados anteriores si los hay
            return

        # Validación B: Que sea un número entero
        try:
            numero = int(numero_texto)
        except ValueError:
            self.alertas.configure(text=f"Intento {self.intentos}: Ingresa solo números enteros.", text_color="red")
            self.resultados.configure(text="")
            return

        # Validación C: Lógica principal (Menor a 10)
        if numero >= 10:
            self.alertas.configure(text=f"Intento {self.intentos}: El número {numero} NO es menor a 10.",
                                   text_color="red")
            self.resultados.configure(text="")
        else:
            # Éxito
            self.alertas.configure(text="¡Validación exitosa!", text_color="green")
            self.resultados.configure(
                text=f"Número correcto ingresado: {numero}\nCantidad de intentos: {self.intentos}"
            )

            # Reiniciamos el sistema para un nuevo juego/validación
            self.intentos = 0
            self.entrada_numero.delete(0, 'end')