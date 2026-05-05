import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from dashboard_ui import (
    afficher_entete,
    afficher_graphique_barres,
    appliquer_style,
    bandeau_resume,
    carte_kpi,
)
from sales_core import (
    COLONNES_SOURCE,
    COLONNES_RESULTATS,
    COLONNES_EXPORT_RESULTATS,
    DOSSIER_EXPORTS,
    FICHIERS_EXPORTS,
    FICHIERS_GRAPHIQUES,
    FICHIER_GRAPHIQUE,
    FICHIER_RESULTATS,
    FICHIER_VENTES,
    calculer_resultats,
    exporter_csv,
    format_montant,
    generer_donnees,
    lire_csv,
    resumer_ventes,
)

TYPES_GRAPHIQUE = ["Barres horizontales", "Rectangles", "Cylindres", "Points", "Cercle"]
FICHIER_ORIGINE_EXPORT = DOSSIER_EXPORTS / "origine_export.txt"
FICHIER_META_TERMINAL = DOSSIER_EXPORTS / "meta_terminal.json"


def tableau_source_vide():
    return pd.DataFrame(columns=COLONNES_SOURCE)


def tableau_resultats_vide():
    return pd.DataFrame(columns=COLONNES_RESULTATS)


def supprimer_anciens_exports():
    for chemin in FICHIERS_EXPORTS:
        if chemin.exists():
            try:
                chemin.unlink()
            except PermissionError:
                pass
    if FICHIER_ORIGINE_EXPORT.exists():
        try:
            FICHIER_ORIGINE_EXPORT.unlink()
        except PermissionError:
            pass
    if FICHIER_META_TERMINAL.exists():
        try:
            FICHIER_META_TERMINAL.unlink()
        except PermissionError:
            pass


def exporter_graphiques(resume):
    DOSSIER_EXPORTS.mkdir(parents=True, exist_ok=True)
    for type_graphique, chemin in FICHIERS_GRAPHIQUES.items():
        fig = afficher_graphique_barres(resume["ca_par_produit"], type_graphique)
        fig.savefig(chemin, dpi=160, bbox_inches="tight")
        plt.close(fig)


def lire_meta_terminal():
    if not FICHIER_META_TERMINAL.exists():
        return {}
    try:
        return json.loads(FICHIER_META_TERMINAL.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def meta_terminal_a_jour():
    if not FICHIER_META_TERMINAL.exists() or not FICHIER_VENTES.exists():
        return False
    try:
        return FICHIER_META_TERMINAL.stat().st_mtime >= FICHIER_VENTES.stat().st_mtime
    except OSError:
        return False


def enregistrer_meta_terminal(resultats, nb_produits_saisi=None):
    nb_produits = nb_produits_saisi
    if nb_produits is None:
        nb_produits = int(resultats["ID"].nunique()) if "ID" in resultats.columns else 0

    FICHIER_META_TERMINAL.write_text(
        json.dumps(
            {
                "nb_ventes": int(len(resultats)),
                "nb_produits": int(nb_produits),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def exporter_analyse(df, enregistrer_exports=True, nb_produits_saisi=None):
    if enregistrer_exports:
        supprimer_anciens_exports()
    resultats = calculer_resultats(df)
    resume = resumer_ventes(resultats)
    if enregistrer_exports:
        exporter_csv(resultats[COLONNES_SOURCE], FICHIER_VENTES)
        exporter_csv(resultats[COLONNES_EXPORT_RESULTATS], FICHIER_RESULTATS)
        FICHIER_ORIGINE_EXPORT.write_text("terminal", encoding="utf-8")
        enregistrer_meta_terminal(resultats, nb_produits_saisi)
        exporter_graphiques(resume)
    return resultats, resume


def demander_nombre(message, type_nombre=float, minimum=None, maximum=None):
    while True:
        valeur = input(message).strip().replace(",", ".")
        try:
            valeur = type_nombre(valeur)
        except ValueError:
            print("Valeur invalide. Reessaie.")
            continue

        if minimum is not None and valeur < minimum:
            print(f"La valeur doit etre au moins {minimum}.")
            continue
        if maximum is not None and valeur > maximum:
            print(f"La valeur doit etre au maximum {maximum}.")
            continue
        return valeur


def saisir_vente_terminal():
    print("\nNouvelle vente")
    id_produit = demander_nombre("ID produit : ", int, minimum=1)
    prix = demander_nombre("Prix : ", float, minimum=0)
    quantite = demander_nombre("Quantite : ", int, minimum=1)
    remise = demander_nombre("Remise (%) : ", float, minimum=0, maximum=100)
    return {
        "ID": id_produit,
        "Prix": prix,
        "Quantite": quantite,
        "Remise": remise,
    }


def afficher_resume_terminal(resultats, resume):
    print("\nFichiers regeneres :")
    for chemin in FICHIERS_EXPORTS:
        print(f"- {chemin}")

    print("\nResultats principaux :")
    print(f"Nombre de ventes : {resume['nb_ventes']}")
    print(f"CA total net : {resume['ca_total']:.2f}")
    print(f"TVA totale : {resume['tva_total']:.2f}")
    print(f"Total TTC : {resume['total_ttc']:.2f}")
    print(f"Panier moyen TTC : {resume['panier_moyen']:.2f}")
    print(f"Produit avec le plus gros CA net : {resume['produit_top'] or '-'}")
    print(f"CA net du produit top : {resume['ca_top']:.2f}")

    print("\nResultats avec ID et colonnes calculees :")
    if resultats.empty:
        print(resultats)
    else:
        print(resultats.to_string(index=False))


def charger_donnees_terminal():
    if FICHIER_VENTES.exists():
        try:
            return lire_csv(FICHIER_VENTES)
        except ValueError:
            return tableau_source_vide()
    return tableau_source_vide()


def mode_terminal():
    print("Analyse automatique des ventes")
    print("-" * 35)
    print("Le terminal reste ouvert. Tape q dans le menu pour quitter.")
    print("Pour voir les memes donnees dans le dashboard, choisis 'Lire exports/ventes.csv'.")

    donnees = charger_donnees_terminal()
    nb_produits_terminal = lire_meta_terminal().get("nb_produits")

    while True:
        print("\nMenu")
        print("1. Ajouter une vente")
        print("2. Generer des ventes aleatoires")
        print("3. Lire exports/ventes.csv")
        print("4. Regenerer les fichiers et afficher les resultats")
        print("q. Quitter")
        choix = input("Choix : ").strip().lower()

        try:
            if choix == "1":
                nouvelle_vente = saisir_vente_terminal()
                donnees = pd.concat(
                    [donnees, pd.DataFrame([nouvelle_vente])],
                    ignore_index=True,
                )
                resultats, resume = exporter_analyse(
                    donnees,
                    nb_produits_saisi=nb_produits_terminal,
                )
                afficher_resume_terminal(resultats, resume)
            elif choix == "2":
                nb_ventes = demander_nombre("Nombre de ventes a generer : ", int, minimum=0)
                nb_produits = demander_nombre("Nombre de produits : ", int, minimum=0)
                donnees = generer_donnees(nb_ventes, nb_produits)
                nb_produits_terminal = nb_produits
                resultats, resume = exporter_analyse(
                    donnees,
                    nb_produits_saisi=nb_produits_terminal,
                )
                afficher_resume_terminal(resultats, resume)
            elif choix == "3":
                donnees = lire_csv(FICHIER_VENTES)
                nb_produits_terminal = lire_meta_terminal().get("nb_produits")
                resultats, resume = exporter_analyse(
                    donnees,
                    nb_produits_saisi=nb_produits_terminal,
                )
                afficher_resume_terminal(resultats, resume)
            elif choix == "4":
                resultats, resume = exporter_analyse(
                    donnees,
                    nb_produits_saisi=nb_produits_terminal,
                )
                afficher_resume_terminal(resultats, resume)
            elif choix in {"q", "quit", "quitter"}:
                print("Fin du mode terminal.")
                break
            else:
                print("Choix inconnu. Reessaie.")
        except FileNotFoundError as erreur:
            print(f"Erreur : {erreur}")
        except ValueError as erreur:
            print(f"Erreur : {erreur}")


def lire_source_dashboard(source, uploaded_file, nb_ventes, nb_produits):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df

    if source in {"Saisie manuelle", "Importer un CSV"}:
        return None

    if source == "Lire exports/ventes.csv":
        if not export_vient_du_terminal():
            raise FileNotFoundError(
                "Aucune donnee du terminal n'a encore ete enregistree."
            )
        return lire_csv(FICHIER_VENTES)

    df = generer_donnees(nb_ventes, nb_produits)
    return df


def export_vient_du_terminal():
    if not FICHIER_ORIGINE_EXPORT.exists():
        return False
    try:
        return FICHIER_ORIGINE_EXPORT.read_text(encoding="utf-8").strip() == "terminal"
    except OSError:
        return False


def compter_donnees_partagees():
    if not FICHIER_VENTES.exists() or not export_vient_du_terminal():
        return 0, 0

    try:
        donnees = lire_csv(FICHIER_VENTES)
        if "ID" not in donnees.columns:
            return 0, 0
        nb_produits = donnees["ID"].nunique()
        meta = lire_meta_terminal() if meta_terminal_a_jour() else {}
        if "nb_produits" in meta:
            nb_produits = int(meta["nb_produits"])
        return len(donnees), nb_produits
    except (FileNotFoundError, ValueError, pd.errors.EmptyDataError):
        return 0, 0


def appliquer_compteurs_terminal(resume, resultats):
    resume["nb_ventes"] = int(len(resultats))
    meta = lire_meta_terminal() if meta_terminal_a_jour() else {}
    if "nb_produits" in meta:
        resume["nb_produits"] = int(meta["nb_produits"])
    return resume


def afficher_sidebar():
    with st.sidebar:
        st.header("Analyse")
        st.caption("Generation, import ou lecture du fichier de ventes.")
        source = st.radio(
            "Source des donnees",
            ["Generer des donnees", "Importer un CSV", "Lire exports/ventes.csv", "Saisie manuelle"],
        )
        st.divider()
        lecture_exports = source == "Lire exports/ventes.csv"
        nb_ventes_partagees, nb_produits_partages = compter_donnees_partagees()

        if lecture_exports:
            st.caption("Valeurs lues depuis le terminal")
            st.metric("Nombre de ventes a analyser", nb_ventes_partagees)
            st.metric("Nombre de produits", nb_produits_partages)
            nb_ventes = nb_ventes_partagees
            nb_produits = nb_produits_partages
        else:
            nb_ventes = st.number_input(
                "Nombre de ventes a analyser",
                min_value=0,
                value=100,
                step=1,
                disabled=source != "Generer des donnees",
                key="nb_ventes_generation",
            )
            nb_produits = st.number_input(
                "Nombre de produits",
                min_value=0,
                value=20,
                step=1,
                disabled=source != "Generer des donnees",
                key="nb_produits_generation",
            )

        st.divider()
        if lecture_exports:
            st.info("Cette vue affiche seulement les donnees enregistrees par le terminal.")
            lancer = True
        else:
            lancer = st.button("Lancer l'analyse", type="primary", use_container_width=True)

    return source, nb_ventes, nb_produits, lancer


def afficher_kpis(resume):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        carte_kpi("CA total net", format_montant(resume["ca_total"]), "Apres remises")
    with col2:
        carte_kpi("TVA totale", format_montant(resume["tva_total"]), "Taux applique : 20%")
    with col3:
        carte_kpi("Total TTC", format_montant(resume["total_ttc"]), "CA net + TVA")
    with col4:
        carte_kpi("Panier moyen", format_montant(resume["panier_moyen"]), "Moyenne par vente")
    with col5:
        produit_top = "-" if resume["produit_top"] is None else f"ID {resume['produit_top']}"
        carte_kpi(
            "Produit leader",
            produit_top,
            f"CA net : {format_montant(resume['ca_top'])}",
        )


def afficher_un_graphique(titre, resume, type_graphique):
    st.markdown('<div class="section-panel">', unsafe_allow_html=True)
    st.subheader(titre)
    fig = afficher_graphique_barres(resume["ca_par_produit"], type_graphique)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    st.markdown("</div>", unsafe_allow_html=True)


def afficher_vue_generale(resume):
    ligne1_gauche, ligne1_droite = st.columns(2)
    with ligne1_gauche:
        afficher_un_graphique("Barres horizontales", resume, "Barres horizontales")
    with ligne1_droite:
        afficher_un_graphique("Rectangles", resume, "Rectangles")

    ligne2_gauche, ligne2_droite = st.columns(2)
    with ligne2_gauche:
        afficher_un_graphique("Cylindres", resume, "Cylindres")
    with ligne2_droite:
        afficher_un_graphique("Diagramme en points", resume, "Points")

    ligne3_gauche, ligne3_droite = st.columns([1, 1])
    with ligne3_gauche:
        afficher_un_graphique("Diagramme circulaire", resume, "Cercle")
    with ligne3_droite:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        st.subheader("Classement")
        classement = resume["ca_par_produit"].reset_index()
        classement.columns = ["ID", "CA_Net_Total"]
        classement["CA_Net_Total"] = classement["CA_Net_Total"].round(2)
        st.dataframe(
            classement.head(10),
            use_container_width=True,
            hide_index=True,
            height=386,
            column_config={
                "ID": st.column_config.NumberColumn("ID produit", format="%d"),
                "CA_Net_Total": st.column_config.NumberColumn("CA net total", format="%.2f EUR"),
            },
        )
        st.markdown("</div>", unsafe_allow_html=True)


def afficher_resultats_detailles(resultats):
    st.subheader("Donnees detaillees avec colonnes calculees")
    st.dataframe(
        resultats,
        use_container_width=True,
        hide_index=True,
        height=520,
        column_config={
            "Prix": st.column_config.NumberColumn("Prix", format="%.2f EUR"),
            "Quantite": st.column_config.NumberColumn("Quantite", format="%d"),
            "Remise": st.column_config.NumberColumn("Remise", format="%d %%"),
            "CA_Brut": st.column_config.NumberColumn("CA brut", format="%.2f EUR"),
            "Montant_Remise": st.column_config.NumberColumn("Montant remise", format="%.2f EUR"),
            "CA_Net": st.column_config.NumberColumn("CA net", format="%.2f EUR"),
            "TVA_20": st.column_config.NumberColumn("TVA 20%", format="%.2f EUR"),
            "Total_TTC": st.column_config.NumberColumn("Total TTC", format="%.2f EUR"),
        },
    )


def afficher_tableau_saisie():
    st.subheader("Saisie des ventes")
    st.session_state["ventes_saisies"] = st.data_editor(
        st.session_state.get("ventes_saisies", tableau_source_vide()),
        key="tableau_saisie_ventes",
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        height=300,
        column_config={
            "ID": st.column_config.NumberColumn("ID produit", min_value=1, step=1),
            "Prix": st.column_config.NumberColumn("Prix", min_value=0.0, format="%.2f EUR"),
            "Quantite": st.column_config.NumberColumn("Quantite", min_value=1, step=1),
            "Remise": st.column_config.NumberColumn("Remise", min_value=0.0, max_value=100.0, format="%.0f %%"),
        },
    )


def convertir_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def afficher_exports(resultats, lecture_exports):
    st.subheader("Fichiers generes")
    if lecture_exports:
        st.write(f"Ces fichiers viennent du terminal et sont presents dans `{DOSSIER_EXPORTS}`.")
    else:
        st.write("Ces fichiers sont generes pour le telechargement sans modifier le dossier `exports`.")

    st.download_button(
        "Telecharger ventes.csv",
        data=convertir_csv(resultats[COLONNES_SOURCE]),
        file_name="ventes.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.download_button(
        "Telecharger resultats_final.csv",
        data=convertir_csv(resultats[COLONNES_EXPORT_RESULTATS]),
        file_name="resultats_final.csv",
        mime="text/csv",
        use_container_width=True,
    )
    if lecture_exports and FICHIER_GRAPHIQUE.exists():
        for type_graphique, chemin in FICHIERS_GRAPHIQUES.items():
            if chemin.exists():
                st.download_button(
                    f"Telecharger {type_graphique.lower()}",
                    data=Path(chemin).read_bytes(),
                    file_name=chemin.name,
                    mime="image/png",
                    use_container_width=True,
                )


def afficher_tabs(resultats, resume, lecture_exports):
    tab_graphique, tab_tableau, tab_exports = st.tabs(
        ["Vue generale", "Resultats detailles", "Exports CSV"]
    )

    with tab_graphique:
        afficher_vue_generale(resume)

    with tab_tableau:
        afficher_resultats_detailles(resultats)

    with tab_exports:
        afficher_exports(resultats, lecture_exports)


def interface_streamlit():
    st.set_page_config(
        page_title="Analyse des ventes",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    appliquer_style()
    afficher_entete()

    source, nb_ventes, nb_produits, lancer = afficher_sidebar()
    uploaded_file = None
    saisie_manuelle = tableau_source_vide()

    generation_auto = source == "Generer des donnees"

    if source == "Importer un CSV":
        uploaded_file = st.file_uploader(
            "Importer un fichier CSV",
            type=["csv"],
            help="Colonnes attendues : ID, Prix, Quantite, Remise",
        )

    if source == "Saisie manuelle":
        afficher_tableau_saisie()
        saisie_manuelle = st.session_state["ventes_saisies"].dropna(how="all")

    lecture_exports = source == "Lire exports/ventes.csv"

    if (
        not generation_auto
        and not lecture_exports
        and not lancer
        and uploaded_file is None
        and saisie_manuelle.empty
    ):
        st.write("")
        afficher_resultats_detailles(tableau_resultats_vide())
        st.info("Ajoute des lignes dans le tableau ou choisis une autre source de donnees.")
        return

    try:
        if source == "Saisie manuelle" and not saisie_manuelle.empty:
            df = saisie_manuelle
        else:
            df = lire_source_dashboard(source, uploaded_file, nb_ventes, nb_produits)
        if df is None:
            st.write("")
            afficher_resultats_detailles(tableau_resultats_vide())
            st.info("Importe un fichier CSV ou genere des donnees pour lancer l'analyse.")
            return

        if lecture_exports:
            resultats = calculer_resultats(df)
            resume = resumer_ventes(resultats)
            resume = appliquer_compteurs_terminal(resume, resultats)
        else:
            resultats, resume = exporter_analyse(df, enregistrer_exports=False)
    except ValueError as erreur:
        st.error(str(erreur))
        return
    except FileNotFoundError as erreur:
        st.error(str(erreur))
        return

    if resultats.empty:
        st.info("Tableau vide : aucune vente n'a ete generee avec les valeurs 0 et 0.")

    if lecture_exports:
        st.success("Donnees du terminal synchronisees depuis exports/ventes.csv.")
    else:
        st.success("Analyse terminee. Les resultats sont affiches dans le dashboard.")
    bandeau_resume(resume)
    afficher_kpis(resume)
    st.write("")
    afficher_tabs(resultats, resume, lecture_exports)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in {"terminal", "--terminal", "-t"}:
        mode_terminal()
    else:
        interface_streamlit()
