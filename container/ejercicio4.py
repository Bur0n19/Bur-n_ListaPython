import customtkinter as ctk

class Ejercicio4(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
"""""
        intentos_ej4 = 0

        def ventana_ejercicio_4():
            global intentos_ej4
            intentos_ej4 = 0

            nuevaVentana = Toplevel(window)
            nuevaVentana.title("Ejercicio 4: Validación de Numeros <10")
            nuevaVentana.geometry("400x350")

            Label(nuevaVentana, text="Validacion de Numero Menor a 10", font=("Arial", 12, "bold")).pack(pady=10)

            numero_var = StringVar()

            Label(nuevaVentana, text="Ingresa un numero entero menor que 10:").pack()
            Entry(nuevaVentana, textvariable=numero_var, width=30).pack(pady=5)

            alertas_ej4 = Label(nueva_ventana, text="", fg="red")
            alertas_ej4.pack(pady=5)

            resultados_ej4 = Label(nueva_ventana, text="", font=("Arial", 11, "bold"))
            resultados_ej4.pack(pady=10)

            def validar():
                global intentos_ej4

                intentos_ej4 += 1

                numeroTexto = numero_var.get()

                if numerooTexto == "":
                    alertas_ej4.config(text=f"Intento {intentos_ej4}: El campo está vacio.", fg="red")
                    return

                try:
                    numero = int(numeroTexto)
                except ValueError:
                    alertas_ej4.config(text=f"Intento {intentos_ej4}: Ingresa solo numeros enteros.", fg="red")
                    return

                if numero >= 10:
                    alertas_ej4.config(text=f"Intento {intentos_ej4}: El numero {numero} NO es menor a 10.", fg="red")
                    resultados_ej4.config(text="")
                else:
                    alertas_ej4.config(text="Validación exitosa", fg="green")
                    resultados_ej4.config(
                        text=f"Numero correcto ingresado: {numero}\nCantidad de intentos: {intentos_ej4}")

                    intentos_ej4 = 0
                    numero_var.set("")

            Button(nueva_ventana, text="Validar Numero", command=validar).pack(pady=10)
"""