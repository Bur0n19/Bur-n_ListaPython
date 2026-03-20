n = 5
lista = []

lista.append(n)
for i in range(n):
    n -= 1
   # k = n
   # print(k)
    lista.append(n)

print(lista)
total = sum(lista)
print(total)

