# shared/main.py

import os
from app.pipeline import pipeline_add_law_and_recompute

if __name__ == "__main__":
    law_file = "shared/directives/4.REGULATION (EU) 20241689 OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL.html"

    if os.path.exists(law_file):
        pipeline_add_law_and_recompute(law_file)
    else:
        print(f"❌ Fichier introuvable : {law_file}")
