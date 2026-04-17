import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("calificaciones.csv")
tab = pd.crosstab(index = df["nombre"], columns = df["calificacion"])
print(tab)

y = tab.loc[tab.index>5["califiacion"]["nombre"].sum]
fila = tab.loc(tab.indexes == 5)
y = int(y)

print("% de alumnos que han sacado 5" %y)


