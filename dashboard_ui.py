import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.patches import Ellipse


def styliser_axes_graphique(fig, ax):
    ax.grid(axis="y", color="#334155", alpha=0.28)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")
    ax.tick_params(colors="#cbd5e1", labelsize=10)
    ax.title.set_color("#f8fafc")
    ax.xaxis.label.set_color("#cbd5e1")
    ax.yaxis.label.set_color("#cbd5e1")
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    fig.tight_layout()


def afficher_graphique_horizontal(ca_par_produit):
    fig, ax = plt.subplots(figsize=(11, 6))
    top10 = ca_par_produit.head(10).sort_values()

    couleurs = ["#334155"] * len(top10)
    if len(couleurs) > 0:
        couleurs[-1] = "#14b8a6"

    ax.barh(top10.index.astype(str), top10.values, color=couleurs, height=0.62)
    ax.set_title("Top 10 des produits par CA net", fontsize=14, weight="bold", pad=18)
    ax.set_xlabel("CA net (EUR)", labelpad=10)
    ax.set_ylabel("ID produit", labelpad=10)
    ax.grid(axis="x", color="#334155", alpha=0.28)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")
    ax.tick_params(colors="#cbd5e1", labelsize=10)
    ax.title.set_color("#f8fafc")
    ax.xaxis.label.set_color("#cbd5e1")
    ax.yaxis.label.set_color("#cbd5e1")

    for index, valeur in enumerate(top10.values):
        ax.text(
            valeur,
            index,
            f"  {valeur:,.0f}".replace(",", " "),
            va="center",
            fontsize=9,
            color="#e2e8f0",
        )

    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    fig.tight_layout()

    return fig


def afficher_graphique_rectangles(ca_par_produit):
    fig, ax = plt.subplots(figsize=(11, 6))
    top10 = ca_par_produit.head(10)

    couleurs = ["#38bdf8"] * len(top10)
    if len(couleurs) > 0:
        couleurs[0] = "#14b8a6"

    ax.bar(top10.index.astype(str), top10.values, color=couleurs, width=0.66)
    ax.set_title("Top 10 des produits par CA net", fontsize=14, weight="bold", pad=18)
    ax.set_xlabel("ID produit", labelpad=10)
    ax.set_ylabel("CA net (EUR)", labelpad=10)

    for index, valeur in enumerate(top10.values):
        ax.text(
            index,
            valeur,
            f"{valeur:,.0f}".replace(",", " "),
            ha="center",
            va="bottom",
            fontsize=9,
            color="#e2e8f0",
        )

    styliser_axes_graphique(fig, ax)
    return fig


def afficher_graphique_cylindres(ca_par_produit):
    fig, ax = plt.subplots(figsize=(11, 6))
    top10 = ca_par_produit.head(10)

    barres = ax.bar(
        top10.index.astype(str),
        top10.values,
        color="#0f766e",
        edgecolor="#5eead4",
        linewidth=1.2,
        width=0.62,
    )
    ax.set_title("Top 10 des produits par CA net", fontsize=14, weight="bold", pad=18)
    ax.set_xlabel("ID produit", labelpad=10)
    ax.set_ylabel("CA net (EUR)", labelpad=10)

    hauteur_max = max(top10.max(), 1) if not top10.empty else 1
    for barre in barres:
        centre_x = barre.get_x() + barre.get_width() / 2
        hauteur = barre.get_height()
        largeur = barre.get_width()
        ellipse_haut = Ellipse(
            (centre_x, hauteur),
            width=largeur,
            height=hauteur_max * 0.035,
            facecolor="#2dd4bf",
            edgecolor="#ccfbf1",
            linewidth=1,
            zorder=4,
        )
        ellipse_bas = Ellipse(
            (centre_x, 0),
            width=largeur,
            height=hauteur_max * 0.035,
            facecolor="#115e59",
            edgecolor="#5eead4",
            linewidth=1,
            zorder=3,
        )
        ax.add_patch(ellipse_bas)
        ax.add_patch(ellipse_haut)
        ax.text(
            centre_x,
            hauteur,
            f"{hauteur:,.0f}".replace(",", " "),
            ha="center",
            va="bottom",
            fontsize=9,
            color="#e2e8f0",
        )

    styliser_axes_graphique(fig, ax)
    return fig


def afficher_graphique_points(ca_par_produit):
    fig, ax = plt.subplots(figsize=(11, 6))
    top10 = ca_par_produit.head(10)
    labels = top10.index.astype(str)
    valeurs = top10.values

    ax.scatter(labels, valeurs, s=130, color="#f59e0b", edgecolor="#fde68a", linewidth=1.4)
    ax.plot(labels, valeurs, color="#fbbf24", alpha=0.55, linewidth=2)
    ax.set_title("Points du CA net par produit", fontsize=14, weight="bold", pad=18)
    ax.set_xlabel("ID produit", labelpad=10)
    ax.set_ylabel("CA net (EUR)", labelpad=10)

    for index, valeur in enumerate(valeurs):
        ax.text(
            index,
            valeur,
            f"{valeur:,.0f}".replace(",", " "),
            ha="center",
            va="bottom",
            fontsize=9,
            color="#e2e8f0",
        )

    styliser_axes_graphique(fig, ax)
    return fig


def afficher_graphique_cercle(ca_par_produit):
    fig, ax = plt.subplots(figsize=(11, 6))
    top10 = ca_par_produit.head(10)

    if top10.empty or top10.sum() == 0:
        ax.text(
            0.5,
            0.5,
            "Aucune donnee",
            ha="center",
            va="center",
            fontsize=13,
            color="#e2e8f0",
        )
        ax.set_axis_off()
    else:
        couleurs = ["#14b8a6", "#38bdf8", "#f59e0b", "#a78bfa", "#f87171"]
        ax.pie(
            top10.values,
            labels=top10.index.astype(str),
            autopct="%1.1f%%",
            startangle=90,
            colors=(couleurs * 2)[: len(top10)],
            textprops={"color": "#e2e8f0", "fontsize": 9},
            wedgeprops={"linewidth": 1, "edgecolor": "#111827"},
        )
        ax.axis("equal")

    ax.set_title("Repartition du CA net par produit", fontsize=14, weight="bold", pad=18)
    ax.title.set_color("#f8fafc")
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    fig.tight_layout()
    return fig


def afficher_graphique_barres(ca_par_produit, type_graphique="Barres horizontales"):
    if type_graphique == "Rectangles":
        return afficher_graphique_rectangles(ca_par_produit)
    if type_graphique == "Cylindres":
        return afficher_graphique_cylindres(ca_par_produit)
    if type_graphique == "Points":
        return afficher_graphique_points(ca_par_produit)
    if type_graphique == "Cercle":
        return afficher_graphique_cercle(ca_par_produit)
    return afficher_graphique_horizontal(ca_par_produit)


def appliquer_style():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #070b13;
            --panel: #111827;
            --panel-soft: #151f2e;
            --panel-raised: #1f2937;
            --line: #263244;
            --line-strong: #334155;
            --text: #f8fafc;
            --muted: #94a3b8;
            --muted-strong: #cbd5e1;
            --accent: #14b8a6;
            --accent-2: #38bdf8;
            --danger: #f87171;
            --success-bg: rgba(20, 184, 166, 0.12);
        }

        html, body, [class*="css"] {
            font-family: Inter, Arial, sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(20, 184, 166, 0.13), transparent 30rem),
                radial-gradient(circle at top right, rgba(56, 189, 248, 0.10), transparent 28rem),
                linear-gradient(180deg, #070b13 0%, #0b1220 56%, #070b13 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 0.75rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }

        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: inherit;
        }

        section[data-testid="stSidebar"] {
            background: #0b1220;
            border-right: 1px solid var(--line);
        }

        section[data-testid="stSidebar"] * {
            color: var(--text);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            font-weight: 800;
        }

        div[data-testid="stSidebarContent"] {
            padding-top: 0.75rem;
        }

        .stRadio label,
        .stNumberInput label,
        .stFileUploader label {
            color: var(--muted-strong) !important;
            font-weight: 700;
        }

        .stNumberInput input,
        .stTextInput input,
        textarea {
            background: var(--panel) !important;
            border: 1px solid var(--line-strong) !important;
            color: var(--text) !important;
            border-radius: 6px !important;
        }

        .stButton > button,
        .stDownloadButton > button {
            background: linear-gradient(135deg, var(--accent), #0f766e);
            color: #04111d;
            border: 1px solid rgba(45, 212, 191, 0.65);
            border-radius: 6px;
            font-weight: 800;
            min-height: 2.75rem;
            box-shadow: 0 10px 22px rgba(20, 184, 166, 0.18);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #2dd4bf, #14b8a6);
            border-color: #5eead4;
            color: #04111d;
        }

        .main-title {
            padding: 1.45rem 1.65rem;
            background:
                linear-gradient(135deg, rgba(20, 184, 166, 0.26), rgba(56, 189, 248, 0.10)),
                var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            margin-bottom: 1.2rem;
            box-shadow: 0 18px 42px rgba(0, 0, 0, 0.24);
        }

        .main-title h1 {
            color: var(--text);
            font-size: 1.9rem;
            font-weight: 800;
            margin: 0 0 0.35rem 0;
            letter-spacing: 0;
        }

        .main-title p {
            color: var(--muted-strong);
            margin: 0;
            font-size: 1rem;
        }

        .kpi-card,
        .summary-item,
        .section-panel {
            background: rgba(17, 24, 39, 0.92);
            border: 1px solid var(--line);
            border-radius: 8px;
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.22);
        }

        .kpi-card {
            padding: 1.05rem 1.15rem;
            min-height: 124px;
            position: relative;
            overflow: hidden;
        }

        .kpi-card::before {
            content: "";
            position: absolute;
            inset: 0 0 auto 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
        }

        .kpi-label,
        .summary-label {
            color: var(--muted);
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.05rem;
            margin-bottom: 0.45rem;
            font-weight: 800;
        }

        .kpi-value {
            color: var(--text);
            font-size: 1.45rem;
            font-weight: 800;
            line-height: 1.2;
            word-break: break-word;
        }

        .kpi-note {
            color: var(--muted);
            font-size: 0.86rem;
            margin-top: 0.45rem;
        }

        .section-panel {
            padding: 1.05rem 1.15rem;
        }

        .section-panel h3 {
            margin-top: 0;
            color: var(--text);
        }

        .summary-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 0.2rem 0 1rem 0;
        }

        .summary-item {
            padding: 0.8rem 0.9rem;
        }

        .summary-value {
            color: var(--text);
            font-size: 1.12rem;
            font-weight: 800;
            margin-top: 0.15rem;
        }

        div[data-testid="stTabs"] {
            background: transparent;
        }

        div[data-testid="stTabs"] button {
            color: var(--muted-strong);
            font-weight: 700;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--text);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            overflow: hidden;
            background: var(--panel);
        }

        div[data-testid="stAlert"] {
            background: var(--success-bg);
            border-radius: 8px;
            border: 1px solid rgba(20, 184, 166, 0.35);
            color: var(--text);
        }

        hr {
            border-color: var(--line) !important;
        }

        @media (max-width: 900px) {
            .summary-strip {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .main-title h1 {
                font-size: 1.55rem;
            }
        }

        @media (max-width: 640px) {
            .summary-strip {
                grid-template-columns: 1fr;
            }

            .kpi-card {
                min-height: 108px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def afficher_entete():
    st.markdown(
        """
        <div class="main-title">
            <h1>Analyse des ventes e-commerce</h1>
            <p>Controle du chiffre d'affaires, des remises, de la TVA et des produits les plus rentables.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def carte_kpi(label, valeur, note=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{valeur}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bandeau_resume(resume):
    st.markdown(
        f"""
        <div class="summary-strip">
            <div class="summary-item">
                <div class="summary-label">Ventes analysees</div>
                <div class="summary-value">{resume["nb_ventes"]:,}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Produits actifs</div>
                <div class="summary-value">{resume["nb_produits"]:,}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Articles vendus</div>
                <div class="summary-value">{resume["quantite_totale"]:,}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Remise moyenne</div>
                <div class="summary-value">{resume["remise_moyenne"]:.1f}%</div>
            </div>
        </div>
        """.replace(",", " "),
        unsafe_allow_html=True,
    )
