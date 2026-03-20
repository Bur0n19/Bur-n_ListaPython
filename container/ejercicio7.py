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
        numeroN = float(self.entradaNumero.get())
        n_limpio = int(round(numeroN))

        self.listaNumeros = []
        self.listaNumeros.append(n_limpio)

        for numeros in range(n_limpio):
            n_limpio -= 1
            self.listaNumeros.append(n_limpio)
        suma_total = sum(self.listaNumeros)
        self.resultado_label.configure(
            text=f"Guardado desde {n_limpio} -> Suma Total: {suma_total}",
            text_color="green"
        )

        self.actualizar_tabla_visual()


    def actualizar_tabla_visual(self):
        df = pd.DataFrame(self.listaNumeros, columns=["Numero"])

        self.caja_tabla.delete("1.0", "end")
        self.caja_tabla.insert("1.0", df.to_string(index=False))







