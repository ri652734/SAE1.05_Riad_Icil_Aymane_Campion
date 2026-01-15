import csv
import matplotlib.pyplot as plt
from datetime import datetime

dates = []
prix = []
conso = []
heures = []


with open("prix_electricite_analyse.csv", newline="") as f:
    reader = csv.reader(f)
    next(reader) # On saute le titre
    for row in reader:
        dates.append(row[0])
        prix.append(float(row[1]))
        conso.append(float(row[2]))
        # On récupère l'heure (ex: "2022-01-01 14:00" -> 14)
        heures.append(int(row[0][11:13])) 



plt.figure(figsize=(12, 6))
plt.plot(dates, prix, color='blue', linewidth=1)
plt.xticks(dates[::48], rotation=45)
plt.title("1. Évolution du prix (Monitoring)")
plt.ylabel("Prix (€/MWh)")
plt.grid(True, alpha=0.5)
plt.tight_layout()


jours = []
volatilite = []

for i in range(0, len(prix), 24):
    bloc = prix[i:i+24]
    if len(bloc) == 24:
        jours.append(dates[i][:10]) 
        
        
        moyenne = sum(bloc) / len(bloc)
        variance = 0
        for valeur in bloc:
            variance += (valeur - moyenne) ** 2
        variance = variance / len(bloc)
        ecart_type = variance ** 0.5
        volatilite.append(ecart_type)

plt.figure(figsize=(12, 6))
plt.plot(jours, volatilite, color='orange', marker='o')
plt.xticks(jours[::5], rotation=45) 
plt.title("2. Volatilité Journalière (Stabilité)")
plt.ylabel("Écart-type")
plt.grid(True, alpha=0.5)
plt.tight_layout()

moyenne_par_heure = []
for h in range(24):
    valeurs_h = [prix[i] for i in range(len(prix)) if heures[i] == h]
    moyenne_par_heure.append(sum(valeurs_h) / len(valeurs_h))

plt.figure(figsize=(12, 6))
plt.plot(range(24), moyenne_par_heure, marker='o', color='green')
plt.title("3. Profil type d'une journée (Heures pleines/creuses)")
plt.xlabel("Heure (0h - 23h)")
plt.ylabel("Prix Moyen")
plt.xticks(range(24))
plt.grid(True, alpha=0.5)
plt.tight_layout()

min_prix = min(prix)
max_prix = max(prix)
min_conso = min(conso)
max_conso = max(conso)

prix_norm = []
for p in prix:
    valeur_norm = (p - min_prix) / (max_prix - min_prix)
    prix_norm.append(valeur_norm)

conso_norm = []
for c in conso:
    valeur_norm = (c - min_conso) / (max_conso - min_conso)
    conso_norm.append(valeur_norm)

plt.figure(figsize=(12, 6))
plt.plot(dates, prix_norm, label="Prix", color="blue", alpha=0.7)
plt.plot(dates, conso_norm, label="Consommation", color="green", alpha=0.7)
plt.xticks(dates[::48], rotation=45)
plt.title("4. Comparaison Normalisée (Offre vs Demande)")
plt.legend()
plt.grid(True, alpha=0.5)
plt.tight_layout()
