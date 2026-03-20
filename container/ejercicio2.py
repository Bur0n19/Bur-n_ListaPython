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

        self.btnCalcular = ctk.CTkButton(self, text="Calcular", command=self.pagos_parque)
        self.btnCalcular.pack(pady=10)

        self.resultado_label = ctk.CTkLabel(self, text="")
        self.resultado_label.pack(pady=10)

        self.titulo_tabla = ctk.CTkLabel(self, text="Historial de Usuarios:", font=("Arial", 12, "italic"))
        self.titulo_tabla.pack(pady=(10, 0))

        self.caja_tabla = ctk.CTkTextbox(self, width=600, height=200, font=("Courier New", 12))
        self.caja_tabla.pack(pady=10)

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
                print('e1')
            elif edad >= 10 and edad <=17:
                nuevoCosto = costoInicial * 0.90
                print('e2')
            else:
                costoInicial *=1
                print('e3')
            totalNuevo = costoInicial - nuevoCosto

            registro = {
                "Empleado": nombre,
                "Edad": edad,
                "Juegos Utilizados": n_juegos,
                "Costo Inicial": costoInicial,
                "Descuento por edad" : nuevoCosto,
            }
            self.lista_usuariosParque.append(registro)

            self.resultado_label.configure(text=f"Guardado: {nombre} -> ${nuevoCosto:.2f}", text_color="green")

            self.actualizar_tabla_visual()

            self.entrada1.delete(0, 'end')
            self.entrada2.delete(0, 'end')
            self.entrada3.delete(0, 'end')

        except ValueError:
            self.resultado_label.configure(text="Error: Ingrese números válidos en Edad y Juegos", text_color="red")
        except Exception as e:
            # Esto imprimirá en la consola si hay un error de código interno (ej. variables mal escritas)
            print(f"Error interno: {e}")
            self.resultado_label.configure(text="Error en el sistema, revisa la consola", text_color="red")

    def actualizar_tabla_visual(self):

        if not self.lista_usuariosParque:
            return
        df = pd.DataFrame(self.lista_usuariosParque)
        self.caja_tabla.delete("1.0", "end")
        self.caja_tabla.insert("1.0", df.to_string(index=False))

    def recaudo_parque(self):
        try:

            pass
        except:
            self.resultado_label.configure(text = "No hay datos que analizar", text_color="red")










