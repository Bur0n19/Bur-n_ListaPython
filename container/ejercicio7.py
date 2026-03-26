import customtkinter as ctk
import pandas as pd

class Ejercicio7(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador


        self.titulo = ctk.CTkLabel(self, text="7. Cálculo de suma de números enteros", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=10)

        self.entradaNumero = ctk.CTkEntry(self, placeholder_text="Ingresa un numero", width = 250)
        self.entradaNumero.pack(pady=10)

        self.btnCalcular = ctk.CTkButton(self, text="Calcular y Guardar", command=self.sumatoria_hastaN)
        self.btnCalcular.pack(pady=10)

        self.resultado_label = ctk.CTkLabel(self, text="")
        self.resultado_label.pack(pady=10)

        self.caja_tabla = ctk.CTkTextbox(self, width=600, height=200, font=("Courier New", 12))
        self.caja_tabla.pack(pady=10)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",
                                          command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=10)

    def sumatoria_hastaN(self):
        texto_numero = self.entradaNumero.get().strip()

        if not texto_numero:
            self.resultado_label.configure(text="Error: El campo está vacío.", text_color="red")
            self.entradaNumero.focus()
            return

        try:
            numeroN = float(texto_numero)
            n_original = int(round(numeroN))

            if n_original < 0:
                self.resultado_label.configure(text="Error: Ingresa un número positivo.", text_color="red")
                self.entradaNumero.delete(0, 'end')
                self.entradaNumero.focus()
                return

            if n_original > 100000:
                self.resultado_label.configure(text="Error: El número es demasiado grande.", text_color="red")
                self.entradaNumero.delete(0, 'end')
                self.entradaNumero.focus()
                return

            self.listaNumeros = []
            n_calculo = n_original
            self.listaNumeros.append(n_calculo)

            for _ in range(n_calculo):
                n_calculo -= 1
                self.listaNumeros.append(n_calculo)

            suma_total = sum(self.listaNumeros)

            self.resultado_label.configure(
                text=f"Sumatoria de {n_original} a 0 -> Total: {suma_total}",
                text_color="green"
            )

            self.entradaNumero.delete(0, 'end')
            self.entradaNumero.focus()

        except ValueError:
            self.resultado_label.configure(text="Error: Ingresa un número válido.", text_color="red")
            self.entradaNumero.delete(0, 'end')
            self.entradaNumero.focus()

        self.actualizar_tabla_visual()


    def actualizar_tabla_visual(self):
        df = pd.DataFrame(self.listaNumeros, columns=["Numero"])

        self.caja_tabla.delete("1.0", "end")
        self.caja_tabla.insert("1.0", df.to_string(index=False))







