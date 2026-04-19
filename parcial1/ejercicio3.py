import customtkinter as ctk

class Ejercicio3(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador

        self.total_vendido = 0.0
        self.lista_compras = []

        self.titulo = ctk.CTkLabel(self, text="Sistema de Descuentos por Mes", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=10)

        self.alertas = ctk.CTkLabel(self, text="", text_color="red")
        self.alertas.pack(pady=5)

        self.entrada_nombre = ctk.CTkEntry(self, placeholder_text="Nombre del cliente", width=250)
        self.entrada_nombre.pack(pady=5)

        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.combo_mes = ctk.CTkOptionMenu(self, values=meses, width=250)
        self.combo_mes.set("Enero")
        self.combo_mes.pack(pady=5)

        self.entrada_importe = ctk.CTkEntry(self, placeholder_text="Importe de la compra", width=250)
        self.entrada_importe.pack(pady=5)

        self.btn_guardar = ctk.CTkButton(self, text="Guardar Compra", command=self.calcular_descuento)
        self.btn_guardar.pack(pady=15)

        self.titulo_historial = ctk.CTkLabel(self, text="Historial de compras:")
        self.titulo_historial.pack(pady=(5, 0))

        self.caja_compras = ctk.CTkTextbox(self, width=450, height=150, font=("Courier New", 12))
        self.caja_compras.pack(pady=5)

        self.etiqueta_total = ctk.CTkLabel(self, text="Total vendido en el día: $0.00", font=("Arial", 14, "bold"))
        self.etiqueta_total.pack(pady=10)

        self.btn_regresar = ctk.CTkButton(self, text="Volver al Menú",command=lambda: controlador.mostrar_frame("menu"), fg_color="gray")
        self.btn_regresar.pack(pady=10)

    def calcular_descuento(self):
        nombre = self.entrada_nombre.get().strip()
        mes = self.combo_mes.get()
        importe_texto = self.entrada_importe.get().strip()

        if not nombre or not importe_texto:
            self.alertas.configure(text="Error: Completa todos los campos", text_color="red")
            return

        try:
            importe = float(importe_texto)

            if importe <= 0:
                self.alertas.configure(text="Error: El importe debe ser mayor a $0", text_color="red")
                return

            if importe > 1000000:
                self.alertas.configure(text="Error: El importe excede el límite permitido", text_color="red")
                return

            if mes == "Octubre":
                descuento = importe * 0.15
            elif mes == "Diciembre":
                descuento = importe * 0.20
            elif mes == "Julio":
                descuento = importe * 0.10
            else:
                descuento = 0.0

            total_final = importe - descuento
            self.total_vendido += total_final

            registro = f"{nombre} ({mes}) | Pago: ${total_final:.2f}\n"
            self.lista_compras.append(registro)

            self.caja_compras.insert("end", registro)
            self.etiqueta_total.configure(text=f"Total vendido en el día: ${self.total_vendido:.2f}")

            self.alertas.configure(
                text=f"¡Compra registrada! Total: ${total_final:.2f} | Descuento: ${descuento:.2f}",
                text_color="green"
            )

            self.entrada_nombre.delete(0, 'end')
            self.entrada_importe.delete(0, 'end')
            self.combo_mes.set("Enero")
            self.entrada_nombre.focus()

        except ValueError:
            self.alertas.configure(text="Error: Ingresa un número numérico válido para el importe", text_color="red")