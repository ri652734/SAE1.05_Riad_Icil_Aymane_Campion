import csv
import matplotlib.pyplot as plt
from datetime import datetime


# fonction simple

def normaliser(liste):
    mn = min(liste)
    mx = max(liste)
    if mx - mn == 0:
        return [0 for _ in liste]
    return [(v - mn) / (mx - mn) for v in liste]

def moyenne_mobile(liste, fenetre):
    mm = []
    for i in range(len(liste)):
        if i < fenetre - 1:
            mm.append(None)
        else:
            bloc = liste[i - fenetre + 1 : i + 1]
            mm.append(sum(bloc) / len(bloc))
    return mm

def moyennes_par_jour(dates, serie, taille_bloc=24):
    jours = []
    moyennes = []
    for i in range(0, len(serie), taille_bloc):
        bloc = serie[i : i + taille_bloc]
        if len(bloc) == taille_bloc:
            jours.append(dates[i][:10])
            moyennes.append(sum(bloc) / taille_bloc)
    return jours, moyennes

def ecart_type(bloc):
    m = sum(bloc) / len(bloc)
    v = 0
    for x in bloc:
        v += (x - m) ** 2
    v = v / len(bloc)
    return v ** 0.5


# DONNÉES

dates, prix, conso, heures = [], [], [], []

with open("prix_electricite_analyse.csv", newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        dates.append(row[0])
        prix.append(float(row[1]))
        conso.append(float(row[2]))
        heures.append(int(row[0][11:13]))


# 1) Éevolution du prix et moyenne sur 24h

mm24 = moyenne_mobile(prix, 24)

plt.figure(figsize=(12, 6))
plt.plot(dates, prix, color="blue", linewidth=1, alpha=0.35, label="Prix brut")
plt.plot(dates, mm24, color="red", linewidth=2, label="Moyenne sur 24h")
plt.xticks(dates[::48], rotation=45)
plt.title("1. Evolution du prix")
plt.ylabel("Prix (€/MWh)")
plt.grid(True, alpha=0.5)
plt.legend()
plt.tight_layout()


# 2) écart-type par jour

jours = []
volatilite = []
for i in range(0, len(prix), 24):
    bloc = prix[i : i + 24]
    if len(bloc) == 24:
        jours.append(dates[i][:10])
        volatilite.append(ecart_type(bloc))

plt.figure(figsize=(12, 6))
plt.plot(jours, volatilite, color="orange", marker="o")
plt.xticks(jours[::5], rotation=45)
plt.title("2. Variation du prix par jour")
plt.ylabel("Ecart-type")
plt.grid(True, alpha=0.5)
plt.tight_layout()


# 3) Prix moyen par heure

moyenne_par_heure = []
for h in range(24):
    valeurs_h = [prix[i] for i in range(len(prix)) if heures[i] == h]
    moyenne_par_heure.append(sum(valeurs_h) / len(valeurs_h))

plt.figure(figsize=(12, 6))
plt.plot(range(24), moyenne_par_heure, marker="o", color="green")
plt.title("3. Prix moyen par heure")
plt.xlabel("Heure (0h - 23h)")
plt.ylabel("Prix moyen")
plt.xticks(range(24))
plt.grid(True, alpha=0.5)
plt.tight_layout()


# 4) prix et conso (lissés sur 24h) -> plus lisible

prix_norm = normaliser(prix)
conso_norm = normaliser(conso)

prix_lisse = moyenne_mobile(prix_norm, 24)
conso_lisse = moyenne_mobile(conso_norm, 24)

plt.figure(figsize=(12, 6))
plt.plot(dates, prix_lisse, label="Prix 24h")
plt.plot(dates, conso_lisse, label="Conso 24h")
plt.xticks(dates[::48], rotation=45)
plt.title("4. Prix et conso lisse")
plt.ylabel("Valeur (0 a 1)")
plt.legend()
plt.grid(True, alpha=0.5)
plt.tight_layout()


# 5) Prix moyen par jour de la semaine

jours_labels = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
somme_jours = [0] * 7
compte_jours = [0] * 7

for i in range(len(dates)):
    dt = datetime.strptime(dates[i], "%Y-%m-%d %H:%M:%S")
    j = dt.weekday()
    somme_jours[j] += prix[i]
    compte_jours[j] += 1

moyennes_jours = []
for j in range(7):
    moyennes_jours.append(somme_jours[j] / compte_jours[j] if compte_jours[j] > 0 else 0)

plt.figure(figsize=(12, 6))
plt.bar(jours_labels, moyennes_jours, edgecolor="black")
plt.title("5. Prix moyen selon le jour")
plt.ylabel("Prix moyen (€/MWh)")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()


# 6) histogramme des prix

plt.figure(figsize=(12, 6))
plt.hist(prix, bins=25, edgecolor="black")
plt.title("6. Histogramme des prix")
plt.xlabel("Prix (€/MWh)")
plt.ylabel("Frequence")
plt.grid(True, axis="y", alpha=0.3)
plt.tight_layout()


# 7) Moyennes par jour, prix vs consommation

jours2, prix_moy_jour = moyennes_par_jour(dates, prix, 24)
_, conso_moy_jour = moyennes_par_jour(dates, conso, 24)

prix_moy_jour_n = normaliser(prix_moy_jour)
conso_moy_jour_n = normaliser(conso_moy_jour)

plt.figure(figsize=(12, 6))
plt.plot(jours2, prix_moy_jour_n, marker="o", label="Prix moyen/jour")
plt.plot(jours2, conso_moy_jour_n, marker="o", label="Conso moyen/jour")
plt.xticks(jours2[::3], rotation=45)
plt.title("7. Prix vs conso (moyenne par jour)")
plt.ylabel("Valeur (0 a 1)")
plt.grid(True, alpha=0.5)
plt.legend()
plt.tight_layout()

plt.show()
