# Sephora Reviews Dashboard

Interactive data analysis project built with **Python, Pandas, Streamlit, and Altair** to explore customer reviews of Sephora products.

This dashboard was designed as a portfolio project to demonstrate an end-to-end analytics workflow: data acquisition, data cleaning, feature engineering, segmentation, exploratory analysis, text analysis, and dashboard storytelling. Streamlit helps structure the app with a sidebar, tabs, and interactive components, while Altair enables customized visualizations and chart colors.

## Project overview

The project aims to answer business-oriented questions such as:
- Which brands receive the most reviews?
- How do ratings vary across products and skin types?
- What is the average price by skin type segment?
- Which words appear most frequently in customer reviews?
- What overall sentiment emerges from review text?

A strong portfolio project should not only display charts; it should also define a clear business problem, provide analytical reasoning, and present results in a polished and readable way.

## Objectives

- Build an interactive dashboard for beauty review exploration.
- Clean and standardize raw data for analysis.
- Segment customers by skin type.
- Compare price, ratings, and recommendation behavior.
- Add text analysis and sentiment exploration.
- Deliver a project suitable for GitHub, Notion, and LinkedIn presentation.

## Data source

The dataset was accessed from **Kaggle** using the Kaggle API / CLI workflow. Kaggle provides official public API documentation and an official CLI package for listing and downloading datasets programmatically.

Typical Kaggle dataset access uses:

```bash
pip install kaggle
kaggle datasets download <owner/dataset-name>
```

Kaggle also documents API authentication through an API token and account configuration.

## Dataset

The dataset contains review-level information including product, brand, price, rating, recommendation behavior, and review text. The final dashboard uses fields such as `brand_name`, `product_name`, `rating`, `price_usd`, `skin_type`, `is_recommended`, and `review_text` after cleaning and normalization with pandas operations such as `read_csv`, `replace`, and `groupby`.

## Main features

### 1. Global analysis
- Review volume KPI
- Unique products KPI
- Average rating KPI
- Recommendation rate KPI
- Rating distribution
- Top brands by number of reviews

Streamlit metrics and layout containers are commonly used to structure these dashboard components.

### 2. Skin type analysis
- Cleaning and harmonization of `skin_type`
- Distribution of reviews by skin type
- Average rating by skin type
- Average price by skin type
- Summary table with review count, average price, and average rating

Dictionary-based replacement is a standard way to normalize categorical values in pandas, and `groupby(...).mean()` is the classic approach for segment-level averages.

### 3. Text analysis
- Review length in characters
- Word count per review
- Most frequent words in reviews
- Average word count by rating

Text exploratory analysis often starts with cleaning, tokenization, word counting, and frequency analysis.

### 4. Sentiment exploration
The final version includes a lightweight sentiment layer based on a dictionary of positive and negative words. This choice keeps the project easy to run locally without heavy NLP dependencies while still demonstrating a useful text interpretation step in a portfolio project. Simple sentiment analysis approaches are commonly used in demo dashboards and review-analysis workflows.
## Data cleaning workflow

Several preparation steps were required before building the dashboard:
- normalizing column names,
- removing index-like columns such as `unnamed_0`,
- converting `rating` and `price_usd` into numeric values,
- cleaning and grouping `skin_type` labels,
- preprocessing `review_text` for text analysis.

These operations align with common pandas data-cleaning patterns using `read_csv`, `replace`, missing-value handling, and grouped aggregations.
## Tools and stack

| Tool | Role in the project |
|------|---------------------|
| Python | Main language |
| Pandas | Data cleaning, feature engineering, aggregations |
| Streamlit | Interactive dashboard and app structure  |
| Altair | Customized visualizations and chart colors  |
| Kaggle API / CLI | Dataset access and download workflow  |
| Regex | Basic text preprocessing |
| GitHub | Versioning and project showcase |
| Notion / LinkedIn | Portfolio presentation |

## Dashboard structure

The final app is organized into three tabs:

| Tab | Content |
|-----|---------|
| Overview | KPIs, rating distribution, top brands |
| Skin type | Skin segmentation, prices, average ratings |
| Text analysis | Word counts, frequent words, sentiment exploration |

Tabs are a good way to separate analytical views and improve readability in Streamlit applications.

## Design choices

The final version follows a premium Sephora-inspired visual direction with a restrained palette, custom CSS, KPI cards, and differentiated chart colors by analytical block. Custom CSS is often used to improve the visual quality of Streamlit apps, especially in portfolio contexts.
## Skills demonstrated

This project highlights the following skills:
- data acquisition through API/CLI workflow,
- data cleaning and transformation,
- categorical normalization,
- KPI design,
- exploratory analysis,
- segmentation,
- text analytics,
- sentiment exploration,
- dashboard design,
- data storytelling.

The strongest data portfolios combine technical execution, business framing, and communication quality.

## Example business questions answered

- Which brands account for the largest review volume?
- Are some skin types associated with more expensive products on average?
- Do some customer segments give lower ratings?
- Are lower-rated reviews longer or more detailed?
- Which words appear most often in customer feedback?
- What sentiment patterns emerge across review groups?

## Project value

This dashboard goes beyond a simple visualization exercise. It demonstrates a full analytics process, from dataset access to a readable and interpretable interface. That makes it a strong portfolio piece for a junior data analyst or a transitioning profile.

## Installation

1. Clone the repository.
2. Install the dependencies:

```bash
pip install streamlit pandas altair kaggle
```

3. Run the application:

```bash
streamlit run app.py
```

Streamlit apps are typically launched this way from a local environment after dependency installation, and Kaggle documents the CLI package installation with `pip install kaggle`.[cite:967][cite:1034]

## Suggested GitHub repository structure

```text
sephora-reviews-dashboard/
├── app.py
├── README.md
├── README_FR.md
├── requirements.txt
├── data/
│   └── reviews_0-250.csv
└── assets/
```

## Portfolio usage

This project can be adapted across several channels:
- **GitHub**: full repository with code and README,
- **Notion**: visual case study with screenshots and insights,
- **LinkedIn**: project post showing the problem, dashboard, and main findings.

A portfolio project becomes stronger when it is repurposed as code, analytical narrative, and visual presentation.

## Example LinkedIn positioning

> Built an interactive Streamlit dashboard to analyze Sephora customer reviews with skin-type segmentation, price analysis, review-text exploration, and sentiment indicators. This project highlights data acquisition with Kaggle API, data cleaning, feature engineering, exploratory analysis, and data storytelling in Python.

## Possible next improvements

Future enhancements could include:
- deploying the app online,
- adding screenshots or a GIF preview,
- enriching sentiment analysis with a dedicated NLP library,
- adding downloadable filtered tables,
- embedding a short methodology section directly in the app.

## Author

**Maïa**  
Data Analyst Portfolio Project
