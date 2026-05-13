import streamlit as st
import pandas as pd
import altair as alt
import re

st.set_page_config(
    page_title="Sephora Reviews Dashboard",
    page_icon="💄",
    layout="wide"
)

# ======================
# STYLE
# ======================
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Arial', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    background-color: #fcf8f8;
}

h1, h2, h3 {
    color: #1f1f1f;
    letter-spacing: 0.3px;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #f0dede;
    padding: 16px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}

[data-testid="stMetricLabel"] {
    color: #7a4e59;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #1f1f1f;
    font-weight: 700;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #f7e9ec;
    border-radius: 12px 12px 0 0;
    padding: 10px 18px;
    color: #6e4250;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: #1f1f1f !important;
    color: white !important;
}

div[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 14px;
    padding: 8px;
    border: 1px solid #f0dede;
}

section[data-testid="stSidebar"] {
    background-color: #fffafa;
    border-right: 1px solid #f0dede;
}

hr {
    border: none;
    border-top: 1px solid #ead9dd;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

COLORS = {
    "general": "#1F1F1F",
    "skin": "#8E6C88",
    "price": "#B76E79",
    "text": "#C06C84",
    "sentiment_pos": "#6A994E",
    "sentiment_neu": "#A0A0A0",
    "sentiment_neg": "#A63A50"
}


def load_data():
    df = pd.read_csv(r"C:\Users\Utilisateur\data_raw\reviews_0-250.csv")

    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

    for col in ["unnamed:_0", "unnamed_0"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    if "rating" in df.columns:
        df["rating"] = (
            df["rating"]
            .astype(str)
            .str.strip()
            .str.replace(",", ".", regex=False)
        )
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    if "price_usd" in df.columns:
        df["price_usd"] = (
            df["price_usd"]
            .astype(str)
            .str.strip()
            .str.replace(",", ".", regex=False)
        )
        df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")

    if "skin_type" in df.columns:
        df["skin_type_clean"] = (
            df["skin_type"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        skin_mapping = {
            "oil": "oily",
            "oily skin": "oily",
            "very oily": "oily",
            "dry skin": "dry",
            "very dry": "dry",
            "combination skin": "combination",
            "normal skin": "normal",
            "sensitive skin": "sensitive",
            "acne prone": "acne-prone",
            "acne-prone skin": "acne-prone",
            "": pd.NA,
            "nan": pd.NA,
            "none": pd.NA
        }

        df["skin_type_clean"] = df["skin_type_clean"].replace(skin_mapping)

    return df


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def simple_sentiment(text):
    positive_words = {
        "love", "great", "good", "amazing", "perfect", "best", "excellent",
        "nice", "beautiful", "smooth", "soft", "favorite", "recommend"
    }
    negative_words = {
        "bad", "worst", "poor", "awful", "disappointing", "dry", "greasy",
        "breakout", "irritating", "heavy", "expensive", "hate", "sticky"
    }

    text = clean_text(text)
    words = text.split()

    pos_count = sum(word in positive_words for word in words)
    neg_count = sum(word in negative_words for word in words)
    score = pos_count - neg_count

    if score > 0:
        return "positive", score
    elif score < 0:
        return "negative", score
    else:
        return "neutral", score


def make_bar_chart(data, x_col, y_col, color, title=""):
    chart = (
        alt.Chart(data)
        .mark_bar(color=color, cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X(x_col, sort='-y'),
            y=alt.Y(y_col),
            tooltip=[x_col, y_col]
        )
        .properties(title=title, height=340)
    )
    return chart


df = load_data().copy()
df_filtered = df.copy()

# ======================
# HEADER
# ======================
st.markdown("""
<div style="background: linear-gradient(135deg, #1f1f1f 0%, #5c3747 100%);
            padding: 28px; border-radius: 20px; margin-bottom: 24px;">
    <h1 style="color: white; margin-bottom: 8px;">Analyse des avis clients Sephora</h1>
    <p style="color: #f7dfe5; font-size: 16px; margin-bottom: 0;">
        Dashboard portfolio orienté data analyse : satisfaction client, segmentation peau, prix et analyse textuelle des avis.
    </p>
</div>
""", unsafe_allow_html=True)

# ======================
# SIDEBAR
# ======================
st.sidebar.header("Filtres")

if "brand_name" in df.columns:
    brands = sorted(df["brand_name"].dropna().astype(str).str.strip().unique().tolist())
    selected_brands = st.sidebar.multiselect("Marques", options=brands)
    if selected_brands:
        df_filtered = df_filtered[
            df_filtered["brand_name"].astype(str).str.strip().isin(selected_brands)
        ]

if "skin_type_clean" in df.columns:
    skin_types = (
        df["skin_type_clean"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )
    skin_types = sorted(skin_types)
    selected_skin_types = st.sidebar.multiselect("Type de peau", options=skin_types)
    if selected_skin_types:
        df_filtered = df_filtered[
            df_filtered["skin_type_clean"].astype(str).str.strip().isin(selected_skin_types)
        ]

if "rating" in df.columns and df["rating"].notna().any():
    rating_min = float(df["rating"].min())
    rating_max = float(df["rating"].max())

    selected_rating = st.sidebar.slider(
        "Plage de notation",
        min_value=rating_min,
        max_value=rating_max,
        value=(rating_min, rating_max),
    )

    df_filtered = df_filtered[
        (df_filtered["rating"] >= selected_rating[0]) &
        (df_filtered["rating"] <= selected_rating[1])
    ]

tab1, tab2, tab3 = st.tabs(["Vue générale", "Type de peau", "Analyse texte"])

# ======================
# TAB 1
# ======================
with tab1:
    st.subheader("Vue générale")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Nombre d'avis", int(df_filtered.shape[0]))

    if "product_name" in df_filtered.columns:
        col2.metric("Produits uniques", int(df_filtered["product_name"].dropna().nunique()))
    else:
        col2.metric("Produits uniques", "N/A")

    if "rating" in df_filtered.columns and df_filtered["rating"].notna().any():
        col3.metric("Note moyenne", round(df_filtered["rating"].mean(), 2))
    else:
        col3.metric("Note moyenne", "N/A")

    if "is_recommended" in df_filtered.columns:
        reco_series = (
            df_filtered["is_recommended"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
        )
        reco_rate = reco_series.isin(["true", "1", "yes"]).mean() * 100 if len(reco_series) > 0 else 0
        col4.metric("Taux de recommandation", f"{reco_rate:.1f}%")
    else:
        col4.metric("Taux de recommandation", "N/A")

    st.markdown("### Aperçu des données")
    st.dataframe(df_filtered.head(50), use_container_width=True)

    g1, g2 = st.columns(2)

    if "rating" in df_filtered.columns and df_filtered["rating"].notna().any():
        with g1:
            rating_df = df_filtered["rating"].value_counts().sort_index().reset_index()
            rating_df.columns = ["rating", "count"]
            st.altair_chart(
                make_bar_chart(rating_df, "rating:O", "count:Q", COLORS["general"], "Distribution des notes"),
                use_container_width=True
            )

    if "brand_name" in df_filtered.columns and not df_filtered.empty:
        with g2:
            top_brands = (
                df_filtered["brand_name"]
                .dropna()
                .astype(str)
                .str.strip()
                .value_counts()
                .head(10)
                .reset_index()
            )
            top_brands.columns = ["brand_name", "count"]
            st.altair_chart(
                make_bar_chart(top_brands, "brand_name:N", "count:Q", COLORS["general"], "Top 10 marques"),
                use_container_width=True
            )

# ======================
# TAB 2
# ======================
with tab2:
    st.subheader("Analyse par type de peau")

    k1, k2, k3 = st.columns(3)

    if "skin_type_clean" in df_filtered.columns:
        k1.metric("Types de peau couverts", int(df_filtered["skin_type_clean"].dropna().nunique()))
    else:
        k1.metric("Types de peau couverts", "N/A")

    if "price_usd" in df_filtered.columns and df_filtered["price_usd"].notna().any():
        k2.metric("Prix moyen USD", round(df_filtered["price_usd"].mean(), 2))
    else:
        k2.metric("Prix moyen USD", "N/A")

    if "rating" in df_filtered.columns and df_filtered["rating"].notna().any():
        k3.metric("Note moyenne", round(df_filtered["rating"].mean(), 2))
    else:
        k3.metric("Note moyenne", "N/A")

    g3, g4 = st.columns(2)

    if "skin_type_clean" in df_filtered.columns and not df_filtered.empty:
        with g3:
            skin_counts = (
                df_filtered["skin_type_clean"]
                .dropna()
                .astype(str)
                .str.strip()
                .value_counts()
                .reset_index()
            )
            skin_counts.columns = ["skin_type", "count"]
            st.altair_chart(
                make_bar_chart(skin_counts, "skin_type:N", "count:Q", COLORS["skin"], "Répartition des types de peau"),
                use_container_width=True
            )

    if "skin_type_clean" in df_filtered.columns and "rating" in df_filtered.columns:
        tmp = df_filtered.dropna(subset=["skin_type_clean", "rating"]).copy()
        if not tmp.empty:
            with g4:
                avg_by_skin = (
                    tmp.groupby("skin_type_clean")["rating"]
                    .mean()
                    .sort_values(ascending=False)
                    .reset_index()
                )
                avg_by_skin.columns = ["skin_type", "avg_rating"]
                st.altair_chart(
                    make_bar_chart(avg_by_skin, "skin_type:N", "avg_rating:Q", COLORS["skin"], "Note moyenne par type de peau"),
                    use_container_width=True
                )

    st.markdown("### Prix par type de peau")

    if "skin_type_clean" in df_filtered.columns and "price_usd" in df_filtered.columns:
        tmp_price = df_filtered.dropna(subset=["skin_type_clean", "price_usd"]).copy()

        if not tmp_price.empty:
            summary_skin = (
                tmp_price.groupby("skin_type_clean", as_index=False)
                .agg(
                    nb_avis=("skin_type_clean", "size"),
                    prix_moyen_usd=("price_usd", "mean"),
                    note_moyenne=("rating", "mean")
                )
                .sort_values(by="prix_moyen_usd", ascending=False)
            )

            summary_skin = summary_skin.rename(columns={"skin_type_clean": "Type de peau"})
            st.dataframe(summary_skin, use_container_width=True)
            st.altair_chart(
                make_bar_chart(summary_skin, "Type de peau:N", "prix_moyen_usd:Q", COLORS["price"], "Prix moyen par type de peau"),
                use_container_width=True
            )

# ======================
# TAB 3
# ======================
with tab3:
    st.subheader("Analyse de texte et sentiment")

    if "review_text" in df_filtered.columns:
        text_df = df_filtered.copy()

        text_df["review_text_clean"] = text_df["review_text"].fillna("").astype(str).apply(clean_text)
        text_df["review_length"] = text_df["review_text"].fillna("").astype(str).str.len()
        text_df["word_count"] = text_df["review_text_clean"].apply(
            lambda x: len(x.split()) if x.strip() != "" else 0
        )

        sentiment_results = text_df["review_text"].apply(simple_sentiment)
        text_df["sentiment_label"] = sentiment_results.apply(lambda x: x[0])
        text_df["sentiment_score"] = sentiment_results.apply(lambda x: x[1])

        t1, t2, t3, t4 = st.columns(4)
        t1.metric("Longueur moyenne", round(text_df["review_length"].mean(), 1))
        t2.metric("Nombre moyen de mots", round(text_df["word_count"].mean(), 1))
        t3.metric("Avis non vides", int((text_df["review_text_clean"] != "").sum()))
        t4.metric("Score moyen", round(text_df["sentiment_score"].mean(), 2))

        tg1, tg2 = st.columns(2)

        with tg1:
            word_count_dist = (
                text_df["word_count"]
                .value_counts()
                .sort_index()
                .head(50)
                .reset_index()
            )
            word_count_dist.columns = ["word_count", "count"]
            st.altair_chart(
                make_bar_chart(word_count_dist, "word_count:O", "count:Q", COLORS["text"], "Distribution du nombre de mots"),
                use_container_width=True
            )

        with tg2:
            sentiment_counts = (
                text_df["sentiment_label"]
                .value_counts()
                .rename_axis("sentiment")
                .reset_index(name="count")
            )

            sentiment_chart = alt.Chart(sentiment_counts).mark_bar().encode(
                x=alt.X("sentiment:N", sort=["positive", "neutral", "negative"]),
                y="count:Q",
                color=alt.Color(
                    "sentiment:N",
                    scale=alt.Scale(
                        domain=["positive", "neutral", "negative"],
                        range=[
                            COLORS["sentiment_pos"],
                            COLORS["sentiment_neu"],
                            COLORS["sentiment_neg"]
                        ]
                    ),
                    legend=None
                ),
                tooltip=["sentiment", "count"]
            ).properties(height=340, title="Répartition des sentiments")

            st.altair_chart(sentiment_chart, use_container_width=True)

        tg3, tg4 = st.columns(2)

        with tg3:
            if "rating" in text_df.columns:
                tmp_text_rating = text_df.dropna(subset=["rating"]).copy()
                if not tmp_text_rating.empty:
                    avg_words = (
                        tmp_text_rating.groupby("rating")["word_count"]
                        .mean()
                        .sort_index()
                        .reset_index()
                    )
                    avg_words.columns = ["rating", "avg_word_count"]
                    st.altair_chart(
                        make_bar_chart(avg_words, "rating:O", "avg_word_count:Q", COLORS["text"], "Nombre moyen de mots par note"),
                        use_container_width=True
                    )

        with tg4:
            if "rating" in text_df.columns:
                tmp_sent_rating = text_df.dropna(subset=["rating"]).copy()
                if not tmp_sent_rating.empty:
                    avg_sentiment = (
                        tmp_sent_rating.groupby("rating")["sentiment_score"]
                        .mean()
                        .sort_index()
                        .reset_index()
                    )
                    avg_sentiment.columns = ["rating", "avg_sentiment"]
                    st.altair_chart(
                        make_bar_chart(avg_sentiment, "rating:O", "avg_sentiment:Q", COLORS["general"], "Sentiment moyen par note"),
                        use_container_width=True
                    )

        stopwords_basic = {
            "the", "and", "a", "an", "to", "of", "it", "is", "in", "for", "my",
            "this", "that", "i", "me", "was", "are", "on", "with", "but", "so",
            "very", "have", "has", "had", "be", "as", "at", "its", "im", "you",
            "they", "them", "we", "our", "your", "from", "or", "if", "not"
        }

        all_words = (
            text_df["review_text_clean"]
            .str.split()
            .explode()
            .dropna()
        )

        all_words = all_words[
            (all_words.str.len() > 2) &
            (~all_words.isin(stopwords_basic))
        ]

        top_words = all_words.value_counts().head(20).reset_index()
        top_words.columns = ["Mot", "Fréquence"]

        st.markdown("### Top 20 mots les plus fréquents")
        st.altair_chart(
            make_bar_chart(top_words, "Mot:N", "Fréquence:Q", COLORS["text"], "Top 20 mots"),
            use_container_width=True
        )
        st.dataframe(top_words, use_container_width=True)

with st.expander("Diagnostic colonnes"):
    st.write(df.columns.tolist())
    