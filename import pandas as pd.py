from pathlib import Path
import pandas as pd
import re

# --- Localisation du fichier CSV ---
current_dir = Path().resolve()
project_root = current_dir.parent
data_path = project_root / "Data" / "Dataset of weighing station temperature measurements.csv"
print("Fichier CSV :", data_path)

# --- Chargement ---
df = pd.read_csv(data_path, sep=";")
df.columns = df.columns.str.strip()  # nettoie les espaces parasites

# --- Ne garder QUE les colonnes de températures (°C) ---
# On repère les colonnes qui mentionnent des degrés Celsius : "deg. C", "degC", "°C", "[C]"
temp_pattern = re.compile(r'(?i)(deg\.?\s*c|degc|°c|\[c\])')
temp_cols = [c for c in df.columns if temp_pattern.search(c)]

# (Option) Si tu veux EXCLURE la température extérieure :
# temp_cols = [c for c in temp_cols if "Outdoor" not in c]

# Conversion en numérique (sécurise au cas où certaines colonnes sont lues en string)
temp_df = df[temp_cols].apply(pd.to_numeric, errors="coerce")

# --- Trouver le max global, la colonne et le timestamp ---
temp_max_val = temp_df.max().max()
temp_max_col = temp_df.max().idxmax()

# Convertir Time si présent pour récupérer le moment exact
time_of_max = None
if "Time" in df.columns:
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
    time_of_max = df.loc[temp_df[temp_max_col].idxmax(), "Time"]

print(f"\nColonnes de température détectées : {len(temp_cols)}")
print("Exemples :", temp_cols[:5])
print(f"\nTempérature maximale : {temp_max_val}")
print(f"Colonne : {temp_max_col}")
if time_of_max is not None:
    print(f"Moment : {time_of_max}")

