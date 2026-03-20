from symtable import Class

class()

ej1 = ctk.CTkFrame(contenedor)
frames["ej1"] = ej1

ej1.grid(row=0, column=0, sticky="nsew")

label = ctk.CTkLabel(ej1, text="Ejercicio 1")
label.pack(pady=20)

btn_volver = ctk.CTkButton(ej1, text="Volver al menú",
command=lambda: mostrar_frame("menu"))
btn_volver.pack(pady=10)