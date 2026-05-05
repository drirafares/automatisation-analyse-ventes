# Automatisation des ventes

Projet de fin d'annee realise par Imene Amira pour la matiere Logiciels.

## Objectif

L'application automatise l'analyse d'un fichier de ventes e-commerce au format CSV. Elle remplace les calculs manuels dans Excel par un script Python capable de generer, lire, analyser et exporter les resultats.

## Donnees attendues

Le fichier d'entree s'appelle `ventes.csv` et contient les colonnes suivantes :

```csv
ID,Prix,Quantite,Remise
101,15.0,3,10
102,25.0,2,5
103,10.0,5,0
```

## Calculs realises

- `CA_Brut` : prix multiplie par quantite.
- `Montant_Remise` : montant retire selon le pourcentage de remise.
- `CA_Net` : chiffre d'affaires apres remise.
- `TVA_20` : TVA calculee avec un taux de 20%.
- `Total_TTC` : CA net plus TVA.
- Produit leader : ID du produit qui genere le CA net le plus eleve.

## Fichiers produits

Les fichiers generes sont regroupes dans le dossier `exports` :

- `exports/ventes.csv` : fichier source genere ou importe.
- `exports/resultats_final.csv` : fichier final avec `ID` et les colonnes calculees, sans `Prix`, `Quantite` ni `Remise`.
- `exports/ca_par_produit_barres.png` : graphique en barres horizontales.
- `exports/ca_par_produit_rectangles.png` : graphique en rectangles.
- `exports/ca_par_produit_cylindres.png` : graphique en cylindres.
- `exports/ca_par_produit_points.png` : diagramme en points.
- `exports/ca_par_produit_cercle.png` : diagramme circulaire.

## Lancer le projet

Ouvrir le terminal dans le dossier du projet :

```powershell
cd c:\logiciels\projet
```

Installer les dependances :

```powershell
pip install -r requirements.txt
```

Lancer l'interface graphique Streamlit :

```powershell
python -m streamlit run analyse_ventes.py
```

Ensuite, ouvrir ce lien dans le navigateur :

```text
http://localhost:8501
```

Lancer en mode terminal :

```powershell
python analyse_ventes.py --terminal
```

## Organisation

- `sales_core.py` contient toute la logique metier : generation, validation, calculs, resume et exports.
- `analyse_ventes.py` contient le mode terminal et l'interface Streamlit.
- `dashboard_ui.py` contient le style et les composants visuels du tableau de bord.
