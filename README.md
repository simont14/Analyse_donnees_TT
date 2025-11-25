
# Analyse des données – Station de pesée chauffée

Projet GMC-3005 – Transferts thermiques

## Structure de ce dossier

```
Analyse_donnees/
│── data/                         # CSV et Excel de la campagne de mesures
│── notebooks/                    # Jupyter notebooks pour l’analyse
│── scripts/                      # Scripts Python propres et réutilisables
│── figures/                      # Images générées (stratification, heatmaps, courbes temporelles)
│── README.md                     # Documentation actuelle
```

---

# Objectif de l’analyse (Mandat 2.1)

À partir du jeu de données fourni par l’équipe de recherche (Tohidi et al.), nous devons :

1. Détecter et quantifier la stratification thermique dans le puits.
2. Analyser la température moyenne sous chaque plateau (P1–P6) au cours du temps.
3. Déduire les règles de contrôle des aérothermes basées sur les mesures observées.

L’analyse se déroule de décembre 2023 à mars 2024 et couvre 87 capteurs mesurés toutes les 2 minutes.

---

# Dataset utilisé

Le dataset contient :

* Température extérieure et humidité
* Températures dans le puits à trois hauteurs :

  * LOW – 0.40 m
  * MID – 0.80 m
  * TOP – 1.20 m
* 29 positions (P1 à P29) × 3 niveaux = 87 capteurs

Points importants à noter :

* Certains capteurs ont cessé de fonctionner en cours de route, entraînant des valeurs NaN.
* Avant le 26 janvier 2024, l’aérotherme sous P6 était hors fonction, créant une zone froid anormale.

---

# Prétraitement des données

Les données originales ont été filtrées avant publication :

* Retrait des valeurs négatives
* Retrait des valeurs inférieures à 0.1 V ou supérieures à 4.9 V
* Conversion tension → résistance → température via l’équation de Steinhart-Hart :

[
T = \frac{1}{A + B\ln R + C(\ln R)^3}
]

[
R = \frac{V_t \times 10000}{V_{CC} - V_t}
]

Ces conversions ne sont pas incluses dans ce dossier, car les données fournies sont déjà en degrés Celsius.

---

# Étapes d’analyse

## 1. Importation et préparation des données

* Chargement du CSV (datetime et champs numériques)
* Nettoyage des NaN
* Séparation des capteurs en trois niveaux : LOW, MID, TOP
* Attribution des positions (P1–P29) en fonction des en-têtes de colonnes

## 2. Détection de la stratification thermique

Méthodes utilisées :

### Méthode qualitative

Tracer la température moyenne LOW, MID et TOP en fonction du temps.
Une stratification est observée lorsque :

[
T_{\text{TOP}} > T_{\text{MID}} > T_{\text{LOW}}
]

### Méthode quantitative

Calcul du gradient vertical pour chaque position :

[
\text{Gradient}(t) = \frac{T_{\text{TOP}}(t) - T_{\text{LOW}}(t)}{1.2 - 0.4}
]

* Gradient > 0 : stratification
* Gradient ≈ 0 : mélange
* Gradient < 0 : inversion thermique

Les capteurs près de P6 montrent des comportements anormaux avant le 26 janvier en raison de l’aérotherme défectueux.

## 3. Température moyenne sous chaque plateau

Pour chaque plateau, les capteurs LOW, MID et TOP associés aux positions correspondantes sont regroupés.
La température moyenne est :

[
\bar{T}_{\text{plateau}}(t) = \text{moyenne de tous les capteurs LOW+MID+TOP du plateau}
]

Cette analyse permet d’identifier les zones plus chaudes ou plus froides du puits, ainsi que l’effet des aérothermes.

## 4. Déduction des règles de contrôle des aérothermes

D’après l’énoncé, les aérothermes fonctionnent selon :

* Mise en marche lorsque la température intérieure est inférieure à 3 °C
* Arrêt lorsque la température extérieure dépasse 3 °C

L’analyse consiste à :

* Identifier les cycles ON/OFF par la dérivée temporelle des températures
* Corréler température extérieure et intérieure
* Observer les périodes de chauffage continu (surtout avant le 26 janvier)

Cette approche permet d’inférer les règles réelles de contrôle, qui peuvent différer du modèle théorique.

---

# Visualisations générées

Les graphiques produits sont enregistrés dans le dossier `figures/`. Ils incluent :

* Courbes LOW / MID / TOP
* Gradient vertical
* Températures par plateau
* Comparaison avant et après 26 janvier
* Heatmaps spatio-temporelles

---

# Points clés observés

* Le puits présente une stratification thermique claire (TOP > MID > LOW).
* La stratification est fortement perturbée lors de la mise en marche des aérothermes ou en présence de mouvements d’air.
* Le plateau P6 est significativement plus froid avant le 26 janvier, confirmant la défaillance de l’aérotherme.
* Les cycles de chauffage montrent :

  * Une activation prolongée lorsque la température extérieure est très basse (< -10 °C)
  * De courts cycles proches de 0–3 °C
  * Un comportement de type hystérésis thermique

---

# Exemple minimal de reproduction (Python)

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/dataset.csv", parse_dates=["Time"])
df.set_index("Time", inplace=True)

# Moyenne par niveau
low_cols = df.filter(regex="LOW").columns
mid_cols = df.filter(regex="MID").columns
top_cols = df.filter(regex="TOP").columns

df["T_low"] = df[low_cols].mean(axis=1)
df["T_mid"] = df[mid_cols].mean(axis=1)
df["T_top"] = df[top_cols].mean(axis=1)

df[["T_low","T_mid","T_top"]].plot(figsize=(12,6))
plt.title("Stratification thermique dans le puits")
plt.show()
```

Les scripts complets sont disponibles dans les dossiers `scripts/` et `notebooks/`.

---

# Auteurs

Projet réalisé dans le cadre du TP GMC-3005 – Transferts thermiques,
Université Laval, Hiver 2025.

---




