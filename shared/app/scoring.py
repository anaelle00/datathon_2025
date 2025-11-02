import os 
import pandas as pd

def load_all_measures(folder="measures"):
    all_files = [f for f in os.listdir(folder) if f.endswith(".csv")]
    dfs = [pd.read_csv(os.path.join(folder, f)) for f in all_files]
    return pd.concat(dfs, ignore_index=True)


def safe_eval_list(x):
    if isinstance(x, str):
        try:
            return eval(x)
        except:
            return []
    return x

def calculate_company_scores(measures_df, company_df):
    # Sécurise les colonnes liste
    measures_df["sector"] = measures_df["sector"].apply(safe_eval_list)
    company_df["Sectors"] = company_df["Sectors"].apply(safe_eval_list)

    # Conversion sûre du score
    measures_df["sentiment_score"] = pd.to_numeric(measures_df["sentiment_score"], errors="coerce").fillna(0).astype(int)

    results = []

    for _, company in company_df.iterrows():
        sectors = set(company["Sectors"])
        symbol = company["Symbol"]
        name = company["Company"]
        weight = company["Weight"]

        matched = measures_df[measures_df["sector"].apply(lambda x: bool(sectors & set(x)))]

        raw_score = matched["sentiment_score"].sum()
        nb_measures = len(matched)
        normalized = raw_score / nb_measures if nb_measures > 0 else 0

        results.append({
            "Symbol": symbol,
            "Company": name,
            "Sectors": list(sectors),
            "nb_matched_measures": nb_measures,
            "raw_score": raw_score,
            "normalized_score": round(normalized, 3),
            "Weight": weight
        })

    return pd.DataFrame(results)