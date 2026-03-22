import customtkinter as ctk
import pandas as pd

class Ejercicio2(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.lista_usuariosParque = []
        self.listaPrecios = []

        self.titulo = ctk.CTkLabel(self, text="Ejercicio 2", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=10)

        self.entrada1 = ctk.CTkEntry(self, placeholder_text="Nombre de usuario", width=250)
        self.entrada1.pack(pady=5)

        self.entrada2 = ctk.CTkEntry(self, placeholder_text="Edad del usuario", width=250)
        self.entrada2.pack(pady=5)

        self.entrada3 = ctk.CTkEntry(self, placeholder_text="Cantidad de juegos", width=250)
        self.entrada3.pack(pady=5)

        self.btnCalcular = ctk.CTkButton(self, text="Guardar", command=self.pagos_parque)
        self.btnCalcular.pack(pady=5)

        self.btnVerHistorial = ctk.CTkButton(self, text="Historial de Pagos", command=self.actualizar_tabla_visual,
                                             fg_color="blue")
        self.btnVerHistorial.pack(pady=5)

        self.btnCalcularSuma = ctk.CTkButton(self, text="Recaudo Total", command=self.recaudo_parque,
                                             fg_color="#e67e22")
        self.btnCalcularSuma.pack(pady=5)

        self.resultado_label = ctk.CTkLabel(self, text="")
        self.resultado_label.pack(pady=5)

        self.titulo_tabla = ctk.CTkLabel(self, text="Historial de Usuarios:", font=("Arial", 12, "italic"))
        self.titulo_tabla.pack(pady=(10, 0))

        self.caja_tabla = ctk.CTkTextbox(self, width=650, height=200, font=("Courier New", 12))
        self.caja_tabla.pack(pady=10)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",
                                          command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=10)

    def pagos_parque(self):
        try:
            nombre = self.entrada1.get()
            edad = int(self.entrada2.get())
            n_juegos = int(self.entrada3.get())
            costoInicial = n_juegos * 50

            if edad < 10:
                nuevoCosto = costoInicial * 0.75
            elif 10 <= edad <= 17:
                nuevoCosto = costoInicial * 0.90
            else:
                nuevoCosto = 0

            registro = {
                "Empleado": nombre,
                "Edad": edad,
                "Juegos Utilizados": n_juegos,
                "Costo Inicial": costoInicial,
                "Descuento por edad": nuevoCosto,
            }

            self.lista_usuariosParque.append(registro)

            self.listaPrecios = [reg["Descuento por edad"] for reg in self.lista_usuariosParque]

            self.resultado_label.configure(text=f"Guardado: {nombre}", text_color="green")

            self.entrada1.delete(0, 'end')
            self.entrada2.delete(0, 'end')
            self.entrada3.delete(0, 'end')

            self.actualizar_tabla_visual()

        except ValueError:
            self.resultado_label.configure(text="Error: Ingrese números válidos en Edad y Juegos", text_color="red")
        except Exception as e:
            print(f"Error interno: {e}")
            self.resultado_label.configure(text="Error en el sistema", text_color="red")

    def actualizar_tabla_visual(self):
        if not self.lista_usuariosParque:
            self.caja_tabla.delete("1.0", "end")
            self.caja_tabla.insert("1.0", "No hay registros todavía.")
            return

        df = pd.DataFrame(self.lista_usuariosParque)
        self.caja_tabla.delete("1.0", "end")
        self.caja_tabla.insert("1.0", df.to_string(index=False))
        self.titulo_tabla.configure(text="VISTA: Historial de Usuarios Registrados")

    def recaudo_parque(self):
        if not self.listaPrecios:
            self.resultado_label.configure(text="No hay datos para calcular el recaudo", text_color="red")
            return
        try:
            recaudo_total = sum(self.listaPrecios)
            total_usuarios = len(self.lista_usuariosParque)

            datos_resumen = {
                "Total de Usuarios Atendidos": [total_usuarios],
                "Dinero Total Recaudado": [f"${recaudo_total:.2f}"]
            }
            df_recaudo = pd.DataFrame(datos_resumen)

            self.caja_tabla.delete("1.0", "end")
            self.caja_tabla.insert("1.0", df_recaudo.to_string(index=False))

            self.titulo_tabla.configure(text="VISTA: Resumen de Recaudo Total")
            self.resultado_label.configure(text="Mostrando recaudo total", text_color="blue")

        except Exception as e:
            print(f"Error al calcular recaudo: {e}")
            self.resultado_label.configure(text="Error al mostrar recaudo", text_color="red")