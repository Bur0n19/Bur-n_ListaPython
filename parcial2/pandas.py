import pandas as pd
import matplotlib.pyplot as plt

df_profesores= pd.DataFrame({
        "nombre":["Jaime", "Armando", "Chucho"],
        "a_paterno":["Minor", "Alvarez", "Martínez"],
        "a_materno":["Gomez", "Galvan", "Campos"]
    })


print(df_profesores)
print(type(df_profesores))

df_archivo = pd.read_csv("sacramento.csv")
print(df_archivo)
print(df_archivo.head())
print(df_archivo.head(20))
print(df_archivo.tail())
print(df_archivo.dtypes)

print(df_archivo.describe())
print(df_archivo["city"]=="SACRAMENTO")
city = "SACRAMENTO"
print(df_archivo.query("city==@city"))
city = "ANTELOPE"
print(df_archivo.query("city==@city"))

print(df_archivo.sort_values(by="city", ascending=True))
print(df_archivo.loc[30])
print(df_archivo["city"].value_counts())


print(df_archivo.sort_values(by="city", ascending=False))


plt.figure()
df_archivo["price"].hist()
plt.title("Distribucion de PRecios")
plt.xlabel("Precios")
plt.ylabel("Distribuciones")
plt.xticks(rotation=45)
plt.show()

plt.figure()
df_archivo["city"].value_counts().head(10).plot(kind="bar")
plt.title("Distribucion de PRecios")
plt.xlabel("Precios")
plt.ylabel("Distribuciones")
plt.xticks(rotation=45)
plt.show()
precio_promedio = df_archivo.groupby("city")["price"].mean().sort_values(ascending=False)


plt.figure()
df_archivo["city"].value_counts().head(10).plot(kind="bar")
plt.title("Distribucion de PRecios")
plt.xlabel("Precios")
plt.ylabel("Distribuciones")
plt.xticks(rotation=45)
plt.show()
precio_promedio = df_archivo.groupby("city")["price"].mean().sort_values(ascending=False)