

import csv
import matplotlib.pyplot as plt

x1 = []
x2 = []
y1 = []



with open("prix_electricite_france_2022.csv", newline= "") as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)
    for row in reader:
        if len(row) >= 2:
            h,m,s = row[0].split(":")
            sec = int(h)*3600 + int (m)*60 + float(s)
            x1.append(sec)
            x2.append(float(row[2]))
            y1.append(float(row[4]))
         

plt.plot(x2,y1)
plt.xlabel("Prix")
plt.ylabel("Mois")
plt.show()