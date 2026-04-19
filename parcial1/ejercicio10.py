import customtkinter as ctk
import pandas as pd


class Ejercicio10(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador

        self.lista_trabajadores = []

        self.titulo = ctk.CTkLabel(self, text="Sistema de Pago de Nómina", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=(20, 10))

        self.entrada_nombre = ctk.CTkEntry(self, placeholder_text="Nombre del trabajador", width=250)
        self.entrada_nombre.pack(pady=5)

        self.entrada_horas_norm = ctk.CTkEntry(self, placeholder_text="Horas normales trabajadas", width=250)
        self.entrada_horas_norm.pack(pady=5)

        self.entrada_pago_hora = ctk.CTkEntry(self, placeholder_text="Pago por hora normal ($)", width=250)
        self.entrada_pago_hora.pack(pady=5)

        self.entrada_horas_ext = ctk.CTkEntry(self, placeholder_text="Horas extras trabajadas", width=250)
        self.entrada_horas_ext.pack(pady=5)

        self.entrada_hijos = ctk.CTkEntry(self, placeholder_text="Número de hijos", width=250)
        self.entrada_hijos.pack(pady=5)

        self.btn_calcular = ctk.CTkButton(self, text="Calcular Pago", command=self.calcular_nomina)
        self.btn_calcular.pack(pady=15)

        self.alertas = ctk.CTkLabel(self, text="", text_color="red")
        self.alertas.pack(pady=5)

        self.titulo_reporte = ctk.CTkLabel(self, text="Reporte de Pagos:", font=("Arial", 12, "italic"))
        self.titulo_reporte.pack(pady=(5, 0))

        self.caja_reporte = ctk.CTkTextbox(self, width=650, height=150, font=("Courier New", 12))
        self.caja_reporte.pack(pady=5)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",
                                          command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=20)

    def calcular_nomina(self):
        nombre = self.entrada_nombre.get().strip()
        horas_norm_txt = self.entrada_horas_norm.get().strip()
        pago_hora_txt = self.entrada_pago_hora.get().strip()
        horas_ext_txt = self.entrada_horas_ext.get().strip()
        hijos_txt = self.entrada_hijos.get().strip()

        if not nombre or not horas_norm_txt or not pago_hora_txt or not horas_ext_txt or not hijos_txt:
            self.alertas.configure(text="Completa todos los campos", text_color="red")
            return

        try:
            horas_norm = float(horas_norm_txt)
            pago_hora = float(pago_hora_txt)
            horas_ext = float(horas_ext_txt)
            hijos = int(hijos_txt)

            if horas_norm < 0 or pago_hora < 0 or horas_ext < 0 or hijos < 0:
                self.alertas.configure(text="Error: No se permiten valores negativos.", text_color="red")
                return

            if horas_norm > 300:
                self.alertas.configure(text="Error: Las horas normales exceden el límite lógico.", text_color="red")
                return
            if pago_hora > 100000:
                self.alertas.configure(text="Error: El pago por hora excede el límite del sistema.", text_color="red")
                return
            if horas_ext > 150:
                self.alertas.configure(text="Error: Las horas extra exceden el límite permitido.", text_color="red")
                return
            if hijos > 25:
                self.alertas.configure(text="Error: Cantidad de hijos fuera de un rango realista.", text_color="red")
                return

            pago_normal = horas_norm * pago_hora
            pago_extra = horas_ext * (pago_hora * 1.5)
            bono = hijos * 0.5
            pago_total = pago_normal + pago_extra + bono

            registro = {
                "Nombre": nombre,
                "Normal": f"${pago_normal:.2f}",
                "Extra": f"${pago_extra:.2f}",
                "Bono": f"${bono:.2f}",
                "Total": f"${pago_total:.2f}"
            }

            self.lista_trabajadores.append(registro)

            self.alertas.configure(text=f"Nómina de {nombre} calculada correctamente", text_color="green")
            self.actualizar_tabla_visual()

            self.entrada_nombre.delete(0, 'end')
            self.entrada_horas_norm.delete(0, 'end')
            self.entrada_pago_hora.delete(0, 'end')
            self.entrada_horas_ext.delete(0, 'end')
            self.entrada_hijos.delete(0, 'end')

            self.entrada_nombre.focus()

        except ValueError:
            self.alertas.configure(text="Error: Verifica que los valores ingresados sean numéricos.",text_color="red")
    def actualizar_tabla_visual(self):
        if not self.lista_trabajadores:
            self.caja_reporte.delete("1.0", "end")
            return

        df = pd.DataFrame(self.lista_trabajadores)
        self.caja_reporte.delete("1.0", "end")
        self.caja_reporte.insert("1.0", df.to_string(index=False))