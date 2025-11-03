📊 Spark & Pulse — Analyse Automatisée de l'Impact des Régulations sur les Marchés Financiers
🧭 Objectif

Concevoir un pipeline d’analyse réglementaire capable de transformer un texte de loi en un score d’impact sur le S&P 500, permettant à des analystes financiers de comprendre immédiatement quels secteurs et entreprises sont positivement ou négativement affectés.
⚙️ Structure du projet
shared/
├── app/
│   ├── extract.py       # Extraction des mesures à partir d’un texte législatif (Claude via Bedrock)
│   ├── scoring.py       # Calcul des scores des entreprises en fonction des mesures
│   └── pipeline.py      # Pipeline principal combinant extraction + scoring
│
├── data/
│   ├── merged_company_data.csv     # Données consolidées entreprises + secteur + poids
│   └── final_company_scores.csv    # Résultat final du scoring
│
├── measures/
│   └── *.csv                       # Mesures extraites automatiquement depuis les lois
│
├── directives/
│   └── *.html / *.xml              # Textes législatifs bruts à analyser
│
└── main.py              # Script de test exécutant le pipeline complet pour chaque loi

🔍 Fonctionnalités principales
📥 extract.py

Fonction : extract_measures_from_file(file_path)

Utilise AWS Bedrock (Claude 3 Sonnet) pour lire et interpréter un texte juridique.

Retourne une liste de mesures sous forme de dictionnaires JSON avec :

law_name, country, type_of_regulation, application_date

sector (liste choisie parmi 6 secteurs majeurs)

measure_text (résumé)

sentiment_score (entre -1 et +1)

⚠️ Gère également la détection de langue avec langdetect.

Fonction : save_measures_to_csv(measures, output_dir)

Sauvegarde proprement les mesures extraites dans un fichier CSV dans le dossier shared/measures/.

📊 scoring.py

Fonction calculate_company_scores() :

Associe les mesures aux entreprises en comparant les secteurs.

Calcule un score normalisé :

score
=
somme des sentiments
nombre de mesures pertinentes
score=
nombre de mesures pertinentes
somme des sentiments
	​

Fonction load_all_measures() :

Fusionne tous les fichiers dans shared/measures/ pour mise à jour cumulative.


🧪 pipeline.py

Fonction principale : pipeline_add_law_and_recompute(file_path)

Étapes :

Extrait les mesures d’une nouvelle loi.

Enregistre les mesures dans shared/measures/.

Recharge toutes les mesures existantes.

Charge les données d’entreprise (merged_company_data.csv).

Calcule les scores avec calculate_company_scores.

Sauvegarde le CSV final_company_scores.csv.

🧪 main.py (script de test)
Le fichier main.py exécute un test ciblé en appliquant le pipeline complet à une seule directive (en l’occurrence : 4.REGULATION (EU) 20241689...). Ce test permet de :

Vérifier le bon fonctionnement du pipeline bout-en-bout, depuis l’analyse du texte brut jusqu’à la génération du score final.

Valider l’intégration entre les modules extract.py, scoring.py, et pipeline.py.

S’assurer que les fichiers sont correctement enregistrés :

Les mesures extraites sont bien sauvegardées dans shared/measures/.

Le fichier de résultats globaux est mis à jour dans shared/data/final_company_scores.csv.

🔍 Ce test minimal est une preuve de robustesse du pipeline pour des cas individuels, et constitue une première brique essentielle avant d’automatiser l’analyse d’un lot complet de lois via une interface ou une boucle.

📈 Exemple de sortie
Symbol	Company	nb_matched_measures	normalized_score	Weight
AAPL	Apple Inc.	5	-0.6	0.006
JNJ	Johnson & Johnson	3	0.33	0.0056
XOM	ExxonMobil	2	1.0	0.00003

💡 Ces scores sont interprétables :

+1.0 → fortement favorisé par la régulation

0.0 → pas d’effet détecté

-1.0 → impact réglementaire négatif

🛠️ Outils utilisés (AWS & stack technique)
| Outil / Service                  | Utilisation                                 |
| -------------------------------- | ------------------------------------------- |
| **AWS Bedrock (Claude 3)**       | Interprétation multilingue des lois         |
| **langdetect**                   | Détection automatique de langue             |
| **pandas**                       | Traitement des données                      |
| **Jupyter + EC2**                | Environnement de prototypage                |
| *(S3 prévu mais non implémenté)* | Pour automatiser l’upload ou la persistance |

🔮 Ce qu’on aurait voulu faire (roadmap)

🧠 Apprentissage par renforcement ou fine-tuning des sentiments à partir de vraies décisions de marché.

🧾 Extraction de la structure hiérarchique des articles et sous-mesures.

📊 Dashboard React + Flask pour visualiser :

Mesures par secteur

Entreprises les plus sensibles

Impact global pondéré (type « ESG Risk Indicator »)

🕒 Historique temporel : suivi de l'évolution de scores après plusieurs lois.

🔁 Comparaison automatique entre projets de loi et lois finales.

🧩 Cross-matching avec chaînes d'approvisionnement (type SEC 10-K) pour meilleure exposition réelle.
