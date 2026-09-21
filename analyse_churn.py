"""Analyse exploratoire du churn client (jeu de données public Telco Customer Churn, IBM).
Pas de modèle prédictif ici : uniquement des regroupements (pandas) pour identifier
les segments à risque, à un niveau que je peux expliquer simplement.
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/telco_churn.csv")
df["Churn_bin"] = (df["Churn"] == "Yes").astype(int)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

taux_global = df["Churn_bin"].mean() * 100
print(f"Taux de churn global : {taux_global:.1f}%  (sur {len(df)} clients)")

# --- Par type de contrat ---
par_contrat = (df.groupby("Contract")["Churn_bin"].mean() * 100).reindex(
    ["Month-to-month", "One year", "Two year"]
)
print("\nPar type de contrat :")
print(par_contrat.round(1))

# --- Par ancienneté (tenure) ---
bins = [0, 12, 24, 48, 72]
labels = ["0-12 mois", "13-24 mois", "25-48 mois", "49-72 mois"]
df["tenure_bin"] = pd.cut(df["tenure"], bins=bins, labels=labels, include_lowest=True)
par_anciennete = df.groupby("tenure_bin", observed=True)["Churn_bin"].mean() * 100
print("\nPar ancienneté :")
print(par_anciennete.round(1))

# --- Par type de service internet ---
par_internet = (df.groupby("InternetService")["Churn_bin"].mean() * 100).reindex(
    ["DSL", "Fiber optic", "No"]
)
print("\nPar service internet :")
print(par_internet.round(1))

# --- Graphiques ---
plt.rcParams["font.size"] = 10

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(par_contrat.index, par_contrat.values, color="#C44E52")
ax.axhline(taux_global, color="gray", linestyle="--", linewidth=1, label=f"Moyenne globale ({taux_global:.1f}%)")
ax.set_ylabel("Taux de churn (%)")
ax.set_title("Taux de churn par type de contrat")
ax.legend()
plt.tight_layout()
plt.savefig("chart_churn_par_contrat.png", dpi=130)
plt.close()

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(par_anciennete.index.astype(str), par_anciennete.values, color="#4C72B0")
ax.axhline(taux_global, color="gray", linestyle="--", linewidth=1, label=f"Moyenne globale ({taux_global:.1f}%)")
ax.set_ylabel("Taux de churn (%)")
ax.set_title("Taux de churn par ancienneté du client")
ax.legend()
plt.tight_layout()
plt.savefig("chart_churn_par_anciennete.png", dpi=130)
plt.close()

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(par_internet.index, par_internet.values, color="#55A868")
ax.axhline(taux_global, color="gray", linestyle="--", linewidth=1, label=f"Moyenne globale ({taux_global:.1f}%)")
ax.set_ylabel("Taux de churn (%)")
ax.set_title("Taux de churn par type de service internet")
ax.legend()
plt.tight_layout()
plt.savefig("chart_churn_par_internet.png", dpi=130)
plt.close()

print("\n3 graphiques générés.")
