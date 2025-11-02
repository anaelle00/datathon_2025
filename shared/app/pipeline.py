import pandas as pd
import os
from app.extract import extract_measures_from_file, save_measures_to_csv
from app.scoring import load_all_measures, calculate_company_scores

def pipeline_add_law_and_recompute(file_path):
    # Utiliser /tmp/ pour Lambda ou le répertoire courant pour local
    base_dir = "/tmp" if os.path.exists("/tmp") else "/mnt/custom-file-systems/s3/shared"
    
    # Extraire les mesures depuis le fichier
    new_measures = extract_measures_from_file(file_path)

    # Sauver dans un CSV unique dans measures/
    measures_dir = f"{base_dir}/measures"
    os.makedirs(measures_dir, exist_ok=True)
    save_measures_to_csv(new_measures, output_dir=measures_dir)

    # Charger données entreprises (copier depuis shared si nécessaire)
    company_data_path = f"{base_dir}/merged_company_data.csv"
    if not os.path.exists(company_data_path):
        # Copier depuis shared
        import shutil
        shutil.copy("/mnt/custom-file-systems/s3/shared/data/merged_company_data.csv", company_data_path)
    
    company_df = pd.read_csv(company_data_path)

    # Recharger toutes les mesures
    all_measures = load_all_measures(measures_dir)

    # Calculer les scores
    scores = calculate_company_scores(all_measures, company_df)

    # Sauver dans /tmp/
    scores.to_csv(f"{base_dir}/final_company_scores.csv", index=False)
    print(f"✅ Scores mis à jour dans {base_dir}/final_company_scores.csv")
