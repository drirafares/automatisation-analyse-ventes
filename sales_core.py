from pathlib import Path

import numpy as np
import pandas as pd

COLONNES_SOURCE = ["ID", "Prix", "Quantite", "Remise"]
COLONNES_RESULTATS = [
    "ID",
    "Prix",
    "Quantite",
    "Remise",
    "CA_Brut",
    "Montant_Remise",
    "CA_Net",
    "TVA_20",
    "Total_TTC",
]
COLONNES_EXPORT_RESULTATS = [
    "ID",
    "CA_Brut",
    "Montant_Remise",
    "CA_Net",
    "TVA_20",
    "Total_TTC",
]
DOSSIER_EXPORTS = Path("exports")
FICHIER_VENTES = DOSSIER_EXPORTS / "ventes.csv"
FICHIER_RESULTATS = DOSSIER_EXPORTS / "resultats_final.csv"
FICHIER_GRAPHIQUE = DOSSIER_EXPORTS / "ca_par_produit_barres.png"
FICHIERS_GRAPHIQUES = {
    "Barres horizontales": FICHIER_GRAPHIQUE,
    "Rectangles": DOSSIER_EXPORTS / "ca_par_produit_rectangles.png",
    "Cylindres": DOSSIER_EXPORTS / "ca_par_produit_cylindres.png",
    "Points": DOSSIER_EXPORTS / "ca_par_produit_points.png",
    "Cercle": DOSSIER_EXPORTS / "ca_par_produit_cercle.png",
}
FICHIERS_EXPORTS = [
    FICHIER_VENTES,
    FICHIER_RESULTATS,
    *FICHIERS_GRAPHIQUES.values(),
]
TAUX_TVA = 0.20
SEED_DEFAUT = 42


def format_montant(valeur: float) -> str:
    return f"{valeur:,.2f} EUR".replace(",", " ")


def generer_donnees(nb_ventes=100, nb_produits=20, seed=SEED_DEFAUT):
    """Genere un DataFrame de ventes au format demande par le projet."""
    if nb_ventes < 0:
        raise ValueError("Le nombre de ventes ne doit pas etre negatif.")
    if nb_produits < 0:
        raise ValueError("Le nombre de produits ne doit pas etre negatif.")
    if nb_ventes > 0 and nb_produits < 1:
        raise ValueError("Le nombre de produits doit etre superieur a 0.")
    if nb_ventes == 0:
        return pd.DataFrame(columns=COLONNES_SOURCE)

    rng = np.random.default_rng(seed)
    ids_produits = np.arange(101, 101 + nb_produits)

    return pd.DataFrame(
        {
            "ID": rng.choice(ids_produits, size=nb_ventes),
            "Prix": np.round(rng.uniform(5, 150, size=nb_ventes), 2),
            "Quantite": rng.integers(1, 20, size=nb_ventes),
            "Remise": rng.choice([0, 5, 10, 15, 20, 25], size=nb_ventes),
        }
    )


def verifier_colonnes(df):
    colonnes_manquantes = [
        colonne for colonne in COLONNES_SOURCE if colonne not in df.columns
    ]
    if colonnes_manquantes:
        raise ValueError(
            "Colonnes manquantes dans le fichier CSV : "
            + ", ".join(colonnes_manquantes)
        )


def preparer_donnees(df):
    """Nettoie et valide les colonnes attendues avant les calculs."""
    verifier_colonnes(df)

    donnees = df[COLONNES_SOURCE].copy()
    for colonne in COLONNES_SOURCE:
        donnees[colonne] = pd.to_numeric(donnees[colonne], errors="coerce")

    if donnees.isna().any().any():
        raise ValueError("Le fichier CSV contient des valeurs vides ou non numeriques.")
    if (donnees["Prix"] < 0).any():
        raise ValueError("La colonne Prix ne doit pas contenir de valeurs negatives.")
    if (donnees["Quantite"] <= 0).any():
        raise ValueError("La colonne Quantite doit contenir des valeurs superieures a 0.")
    if ((donnees["Remise"] < 0) | (donnees["Remise"] > 100)).any():
        raise ValueError("La colonne Remise doit contenir un pourcentage entre 0 et 100.")

    donnees["ID"] = donnees["ID"].astype(int)
    donnees["Quantite"] = donnees["Quantite"].astype(int)
    donnees["Remise"] = donnees["Remise"].astype(float)
    donnees["Prix"] = donnees["Prix"].round(2)

    return donnees


def calculer_resultats(df):
    """Ajoute les colonnes calculees : CA brut, CA net, TVA et total TTC."""
    resultats = preparer_donnees(df)

    resultats["CA_Brut"] = resultats["Prix"] * resultats["Quantite"]
    resultats["Montant_Remise"] = resultats["CA_Brut"] * resultats["Remise"] / 100
    resultats["CA_Net"] = resultats["CA_Brut"] - resultats["Montant_Remise"]
    resultats["TVA_20"] = resultats["CA_Net"] * TAUX_TVA
    resultats["Total_TTC"] = resultats["CA_Net"] + resultats["TVA_20"]

    colonnes_montants = ["CA_Brut", "Montant_Remise", "CA_Net", "TVA_20", "Total_TTC"]
    resultats[colonnes_montants] = resultats[colonnes_montants].round(2)
    return resultats[COLONNES_RESULTATS]


def resumer_ventes(df):
    if df.empty:
        return {
            "ca_total": 0.0,
            "tva_total": 0.0,
            "total_ttc": 0.0,
            "produit_top": None,
            "ca_top": 0.0,
            "nb_ventes": 0,
            "nb_produits": 0,
            "quantite_totale": 0,
            "remise_moyenne": 0.0,
            "panier_moyen": 0.0,
            "ca_par_produit": pd.Series(dtype=float, name="CA_Net"),
        }

    ca_par_produit = df.groupby("ID")["CA_Net"].sum().sort_values(ascending=False)
    produit_top = int(ca_par_produit.index[0])
    ca_top = float(ca_par_produit.iloc[0])
    quantite_totale = int(df["Quantite"].sum())
    remise_moyenne = float(df["Remise"].mean())
    panier_moyen = float(df["Total_TTC"].mean())

    return {
        "ca_total": float(df["CA_Net"].sum()),
        "tva_total": float(df["TVA_20"].sum()),
        "total_ttc": float(df["Total_TTC"].sum()),
        "produit_top": produit_top,
        "ca_top": ca_top,
        "nb_ventes": int(len(df)),
        "nb_produits": int(df["ID"].nunique()),
        "quantite_totale": quantite_totale,
        "remise_moyenne": remise_moyenne,
        "panier_moyen": panier_moyen,
        "ca_par_produit": ca_par_produit,
    }


def exporter_csv(df, chemin):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(chemin, index=False, encoding="utf-8")


def lire_csv(source):
    source = Path(source)
    if not source.exists():
        raise FileNotFoundError(f"Fichier introuvable : {source}")
    return pd.read_csv(source)


def traiter_fichier(
    source,
    generer_si_absent=True,
    forcer_generation=False,
    nb_ventes=100,
    nb_produits=20,
    seed=SEED_DEFAUT,
):
    source = Path(source)

    if forcer_generation or (not source.exists() and generer_si_absent):
        df = generer_donnees(nb_ventes, nb_produits, seed=seed)
        exporter_csv(df, source)
    elif source.exists():
        df = pd.read_csv(source)
    else:
        raise FileNotFoundError(f"Fichier introuvable : {source}")

    resultats = calculer_resultats(df)
    exporter_csv(resultats[COLONNES_EXPORT_RESULTATS], FICHIER_RESULTATS)

    return resultats, resumer_ventes(resultats)
