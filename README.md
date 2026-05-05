# Automatisation et analyse des ventes

Application Python permettant d'automatiser l'analyse de ventes e-commerce a partir d'un fichier CSV, de calculer les indicateurs financiers, d'afficher un dashboard Streamlit et d'exporter les resultats.

## Apercu

Le projet remplace un traitement manuel dans Excel par un workflow automatise :

1. Charger ou generer des donnees de ventes.
2. Valider les colonnes et les valeurs.
3. Calculer le chiffre d'affaires, les remises, la TVA et le total TTC.
4. Afficher les KPI et les graphiques dans un dashboard.
5. Exporter les fichiers CSV et les graphiques PNG.

## Fonctionnalites

- Generation automatique de donnees de ventes.
- Import d'un fichier CSV.
- Saisie manuelle des ventes depuis le dashboard.
- Lecture des donnees partagees depuis `exports/ventes.csv`.
- Mode terminal avec menu interactif.
- Calcul automatique des indicateurs financiers.
- Dashboard Streamlit avec KPI, graphiques et tableaux.
- Export des resultats en CSV.
- Export de plusieurs graphiques Matplotlib en PNG.
- Validation des donnees pour eviter les erreurs de calcul.

## Technologies utilisees

- Python
- pandas
- NumPy
- Matplotlib
- Streamlit

## Structure du projet

```text
automatisation-analyse-ventes/
|-- analyse_ventes.py
|-- dashboard_ui.py
|-- sales_core.py
|-- requirements.txt
|-- README.md
|-- GUIDE_UTILISATION.md
|-- exports/
|   |-- ventes.csv
|   |-- resultats_final.csv
|   |-- ca_par_produit_barres.png
|   |-- ca_par_produit_rectangles.png
|   |-- ca_par_produit_cylindres.png
|   |-- ca_par_produit_points.png
|   |-- ca_par_produit_cercle.png
```

## Installation

Cloner le depot GitHub :

```powershell
git clone https://github.com/drirafares/automatisation-analyse-ventes.git
cd automatisation-analyse-ventes
```

Creer un environnement virtuel :

```powershell
python -m venv venv
```

Activer l'environnement virtuel :

```powershell
venv\Scripts\activate
```

Installer les dependances :

```powershell
pip install -r requirements.txt
```

## Lancer le dashboard

Executer l'application Streamlit :

```powershell
python -m streamlit run analyse_ventes.py
```

Ouvrir ensuite le lien affiche dans le terminal, generalement :

```text
http://localhost:8501
```

## Lancer le mode terminal

Le projet peut aussi etre utilise sans interface web :

```powershell
python analyse_ventes.py --terminal
```

Le menu terminal permet d'ajouter une vente, de generer des ventes aleatoires, de relire le fichier `exports/ventes.csv` et de regenerer les fichiers de sortie.

## Format du fichier CSV

Le fichier d'entree doit contenir exactement ces colonnes :

```csv
ID,Prix,Quantite,Remise
101,15.0,3,10
102,25.0,2,5
103,10.0,5,0
```

Description des colonnes :

- `ID` : identifiant du produit.
- `Prix` : prix unitaire du produit.
- `Quantite` : nombre d'unites vendues.
- `Remise` : pourcentage de remise entre 0 et 100.

## Calculs realises

- `CA_Brut` = `Prix * Quantite`
- `Montant_Remise` = `CA_Brut * Remise / 100`
- `CA_Net` = `CA_Brut - Montant_Remise`
- `TVA_20` = `CA_Net * 0.20`
- `Total_TTC` = `CA_Net + TVA_20`

Le projet calcule aussi :

- le chiffre d'affaires total net ;
- la TVA totale ;
- le total TTC ;
- le panier moyen ;
- le nombre de ventes ;
- le nombre de produits actifs ;
- la quantite totale vendue ;
- la remise moyenne ;
- le produit qui genere le plus gros chiffre d'affaires.

## Fichiers generes

Les fichiers de sortie sont regroupes dans le dossier `exports` :

- `exports/ventes.csv` : donnees sources generees ou saisies.
- `exports/resultats_final.csv` : resultats avec les colonnes d'origine et les colonnes calculees.
- `exports/ca_par_produit_barres.png` : graphique en barres horizontales.
- `exports/ca_par_produit_rectangles.png` : graphique en rectangles.
- `exports/ca_par_produit_cylindres.png` : graphique en cylindres.
- `exports/ca_par_produit_points.png` : diagramme en points.
- `exports/ca_par_produit_cercle.png` : diagramme circulaire.

## Role des fichiers Python

- `sales_core.py` contient la logique metier : generation des donnees, validation, calculs, resumes et exports.
- `analyse_ventes.py` contient le mode terminal et l'application Streamlit.
- `dashboard_ui.py` contient le style visuel du dashboard, les cartes KPI et les graphiques.

## Documentation detaillee

Un guide complet est disponible dans [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md). Il explique comment ouvrir le projet, utiliser chaque mode, importer un CSV et comprendre les resultats.

## Auteurs

## 🧠 Auteurs

### 👤 mhomed maymoun aouay
![mhomed maymoun aouay] <img width="500" height="500" alt="470533734_122106714482680932_3683554923486708182_n" src="https://github.com/user-attachments/assets/dd1d0a29-f315-44ff-8b15-19ef4d3ee61d" />


  

---

### 👤 amine gdaiem 
![amine gdaiem ] <img width="500" height="500" alt="e5658a6a-98b8-4cc3-b1b3-ffca180c982c" src="https://github.com/user-attachments/assets/4ed62c38-c110-412a-a017-affc963bdacf" />


### 👤 fers drira
![fers drira] <img width="500" height="500" alt="8ca34b6d-95a4-4e32-aff4-777099cdebb4" src="https://github.com/user-attachments/assets/5dc58baf-ef96-46e3-804b-a0e58e62d5b4" />
