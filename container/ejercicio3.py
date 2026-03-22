import customtkinter as ctk

class Ejercicio3(ctk.CTkFrame):
    def __init__(self,parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        """ totalVendido_ej3 = 0.0

        def ventana_ejercicio_3():
            global totalVendido_ej3

            nuevaVentana = Toplevel(window)
            nuevaVentana.title("Ejercicio 3: Descuentos de tienda")
            nuevaVentana.geometry("400x500")
            alertas_ej3 = Label(nuevaVentana, text="", fg="red")
            alertas_ej3.pack(pady=5)
            Label(nuevaVentana, text="Sistema de Descuentos por Mes", font=("Arial", 12, "bold")).pack(pady=10)

            nombre_var = StringVar()
            importe_var = StringVar()
            mes_var = StringVar()

            lista_compras_ej3 = []

            Label(nuevaVentana, text="Nombre del cliente:").pack()
            Entry(nuevaVentana, textvariable=nombre_var, width=30).pack(pady=5)

            Label(nuevaVentana, text="Mes de la compra:").pack()
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre",
                     "Noviembre", "Diciembre"]
            combo_mes = ttk.Combobox(nuevaVentana, textvariable=mes_var, values=meses, state="readonly", width=27)
            combo_mes.pack(pady=5)

            Label(nuevaVentana, text="Importe de la compra:").pack()
            Entry(nuevaVentana, textvariable=importe_var, width=30).pack(pady=5)

            def calcular_descuento():
                global totalVendido_ej3

                nombre = nombre_var.get()
                mes = mes_var.get()
                importe_texto = importe_var.get()

                if nombre == "" or mes == "" or importe_texto == "":
                    alertas_ej3.config(text="Completa todos los campos y selecciona un mes", fg="red")
                    return

                try:
                    importe = float(importe_texto)
                    if importe <= 0:
                        alertas_ej3.config(text="El importe debe ser mayor a 0", fg="red")
                        return
                except ValueError:
                    alertas_ej3.config(text="Ingresa un numero valido para el importe", fg="red")
                    return

                if mes == "Octubre":
                    descuento = importe * 0.15
                elif mes == "Diciembre":
                    descuento = importe * 0.20
                elif mes == "Julio":
                    descuento = importe * 0.10
                else:
                    descuento = 0

                total_final = importe - descuento
                totalVendido_ej3 += total_final

                lista_compras_ej3.append(f"{nombre} ({mes}) | Pago: ${total_final:.2f}")

                caja_compras.delete(1.0, END)
                for registro in lista_compras_ej3:
                    caja_compras.insert(END, registro + "\n")

                etiqueta_total.config(text=f"Total vendido en el dia: ${totalVendido_ej3:.2f}")

                nombre_var.set("")
                importe_var.set("")
                combo_mes.set("")
                alertas_ej3.config(
                    text=f"Compra registrada.\nTotal a pagar: ${total_final:.2f}\nDescuento: ${descuento:.2f}",
                    fg="green")

            Button(nuevaVentana, text="Guardar", command=calcular_descuento).pack(pady=10)

            Label(nuevaVentana, text="Historial de compras:").pack(pady=5)
            caja_compras = Text(nuevaVentana, height=8, width=45)
            caja_compras.pack()

            etiqueta_total = Label(nuevaVentana, text="Total vendido en el día: $0.00", font=("Arial", 10, "bold"))
            etiqueta_total.pack(pady=10)
    """