# Guide d'utilisation detaille

Ce document explique comment installer, ouvrir et utiliser le projet d'automatisation et d'analyse des ventes.

## 1. Objectif du projet

Le projet sert a automatiser l'analyse des ventes e-commerce. Il permet de partir d'un fichier CSV simple, de calculer automatiquement les resultats financiers et d'afficher les indicateurs dans un dashboard web.

Le projet evite les calculs manuels dans Excel et reduit les erreurs de saisie ou de formule.

## 2. Prerequis

Avant de lancer le projet, il faut installer :

- Python 3.x
- Git
- Visual Studio Code, facultatif mais recommande

Pour verifier que Python est installe :

```powershell
python --version
```

Pour verifier que Git est installe :

```powershell
git --version
```

## 3. Recuperer le projet depuis GitHub

Dans un terminal PowerShell, executer :

```powershell
git clone https://github.com/drirafares/automatisation-analyse-ventes.git
cd automatisation-analyse-ventes
```

Si le projet est deja telecharge, il suffit d'ouvrir le dossier dans VS Code.

## 4. Creer et activer l'environnement virtuel

Creer l'environnement :

```powershell
python -m venv venv
```

Activer l'environnement :

```powershell
venv\Scripts\activate
```

Quand l'environnement est actif, le terminal affiche generalement `(venv)` au debut de la ligne.

## 5. Installer les bibliotheques

Installer les dependances du projet :

```powershell
pip install -r requirements.txt
```

Les bibliotheques utilisees sont :

- `pandas` pour lire et traiter les fichiers CSV ;
- `numpy` pour generer des donnees aleatoires ;
- `matplotlib` pour creer les graphiques ;
- `streamlit` pour afficher le dashboard web.

## 6. Lancer le dashboard Streamlit

Dans le dossier du projet, executer :

```powershell
python -m streamlit run analyse_ventes.py
```

Streamlit ouvre normalement le navigateur automatiquement. Sinon, ouvrir ce lien :

```text
http://localhost:8501
```

## 7. Utiliser le dashboard

Dans la barre laterale, choisir une source de donnees.

### Generer des donnees

Cette option cree automatiquement un tableau de ventes. Il faut choisir :

- le nombre de ventes a analyser ;
- le nombre de produits.

Ensuite, cliquer sur `Lancer l'analyse`.

### Importer un CSV

Cette option permet d'importer un fichier CSV depuis l'ordinateur. Le fichier doit contenir les colonnes :

```csv
ID,Prix,Quantite,Remise
```

Exemple :

```csv
ID,Prix,Quantite,Remise
101,15.0,3,10
102,25.0,2,5
103,10.0,5,0
```

### Lire exports/ventes.csv

Cette option lit les donnees deja generees par le mode terminal. Elle sert a synchroniser le terminal et le dashboard.

### Saisie manuelle

Cette option permet de saisir les ventes directement dans un tableau modifiable dans le dashboard.

## 8. Comprendre les KPI

Le dashboard affiche plusieurs indicateurs :

- `CA total net` : total du chiffre d'affaires apres remise.
- `TVA totale` : montant total de TVA calcule avec un taux de 20%.
- `Total TTC` : total final avec TVA.
- `Panier moyen` : moyenne du total TTC par vente.
- `Produit leader` : produit qui genere le plus grand CA net.
- `Ventes analysees` : nombre de lignes traitees.
- `Produits actifs` : nombre de produits differents.
- `Articles vendus` : somme des quantites vendues.
- `Remise moyenne` : moyenne des remises appliquees.

## 9. Comprendre les calculs

Pour chaque vente, le programme calcule :

```text
CA_Brut = Prix * Quantite
Montant_Remise = CA_Brut * Remise / 100
CA_Net = CA_Brut - Montant_Remise
TVA_20 = CA_Net * 0.20
Total_TTC = CA_Net + TVA_20
```

Exemple :

```text
Prix = 100
Quantite = 2
Remise = 10

CA_Brut = 100 * 2 = 200
Montant_Remise = 200 * 10 / 100 = 20
CA_Net = 200 - 20 = 180
TVA_20 = 180 * 0.20 = 36
Total_TTC = 180 + 36 = 216
```

## 10. Fichiers generes

Le dossier `exports` contient les fichiers produits par l'application :

```text
exports/
|-- ventes.csv
|-- resultats_final.csv
|-- ca_par_produit_barres.png
|-- ca_par_produit_rectangles.png
|-- ca_par_produit_cylindres.png
|-- ca_par_produit_points.png
|-- ca_par_produit_cercle.png
```

`ventes.csv` contient les donnees sources.

`resultats_final.csv` contient les colonnes d'origine et les colonnes calculees :

```csv
ID,Prix,Quantite,Remise,CA_Brut,Montant_Remise,CA_Net,TVA_20,Total_TTC
```

Les fichiers PNG sont les graphiques exportes.

## 11. Lancer le mode terminal

Le mode terminal se lance avec :

```powershell
python analyse_ventes.py --terminal
```

Le menu propose :

```text
1. Ajouter une vente
2. Generer des ventes aleatoires
3. Lire exports/ventes.csv
4. Regenerer les fichiers et afficher les resultats
q. Quitter
```

Ce mode est utile pour montrer que le projet fonctionne aussi sans interface web.

## 12. Validation des donnees

Le programme verifie que :

- les colonnes obligatoires existent ;
- les valeurs sont numeriques ;
- le prix n'est pas negatif ;
- la quantite est superieure a 0 ;
- la remise est entre 0 et 100.

Si une erreur est detectee, un message clair est affiche.

## 13. Role des fichiers du projet

`analyse_ventes.py` : fichier principal. Il lance soit le dashboard Streamlit, soit le mode terminal.

`dashboard_ui.py` : fichier responsable du style, des KPI et des graphiques.

`sales_core.py` : fichier contenant la logique metier : generation, validation, calculs, resumes et exports.

`requirements.txt` : liste des bibliotheques a installer.

`README.md` : presentation generale du projet sur GitHub.

`exports/` : dossier contenant les fichiers produits par l'application.

## 14. Probleme courant

Si Streamlit n'est pas reconnu, verifier que les dependances sont installees :

```powershell
pip install -r requirements.txt
```

Si le port 8501 est deja utilise, Streamlit peut proposer un autre port. Il suffit d'ouvrir le lien affiche dans le terminal.

Si un CSV ne fonctionne pas, verifier que les noms de colonnes sont exactement :

```text
ID, Prix, Quantite, Remise
```
