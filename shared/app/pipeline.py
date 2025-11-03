import pandas as pd
import os
from app.extract import extract_measures_from_file, save_measures_to_csv
from app.scoring import load_all_measures, calculate_company_scores

def pipeline_add_law_and_recompute(file_path):
    # Étape 1 : extraire les mesures depuis la loi
    new_measures = extract_measures_from_file(file_path)

    # Étape 2 : enregistrer ces mesures dans un CSV dédié dans shared/measures/
    save_measures_to_csv(new_measures, output_dir="shared/measures")

    # Étape 3 : charger les données d'entreprises
    company_df = pd.read_csv("shared/data/merged_company_data.csv")

    # Étape 4 : recharger toutes les mesures
    all_measures = load_all_measures("shared/measures")

    # Étape 5 : calculer les scores d'impact pour chaque entreprise
    scores = calculate_company_scores(all_measures, company_df)

    # Étape 6 : sauvegarder le score final
    scores.to_csv("shared/data/final_company_scores.csv", index=False)
    print("✅ Scores mis à jour dans shared/data/final_company_scores.csv")
