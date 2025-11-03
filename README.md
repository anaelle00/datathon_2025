
# 📊 Spark & Pulse — Analyse Automatisée de l'Impact des Régulations sur les Marchés Financiers

## 🧭 Objectif

Concevoir un pipeline d’analyse réglementaire capable de transformer un texte de loi en un score d’impact sur le S&P 500, permettant à des analystes financiers de comprendre immédiatement quels secteurs et entreprises sont positivement ou négativement affectés.

---

## ⚙️ Structure du projet

```
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
└── main.py              # Script de test exécutant le pipeline complet pour une loi
```

---

## 🔍 Fonctionnalités principales

### 📥 `extract.py`

**Fonction : `extract_measures_from_file(file_path)`**  
- Utilise AWS Bedrock (Claude 3 Sonnet) pour lire et interpréter un texte juridique.
- Retourne une liste de mesures avec :
  - `law_name`, `country`, `type_of_regulation`, `application_date`
  - `sector` (liste choisie parmi 6 secteurs majeurs)
  - `measure_text` (résumé clair)
  - `sentiment_score` (entre -1 et +1)
- Détection automatique de la langue via `langdetect`.

**Fonction : `save_measures_to_csv(measures, output_dir)`**  
- Sauvegarde les mesures extraites dans un fichier CSV dans `shared/measures/`.

---

### 📊 `scoring.py`

**Fonction : `calculate_company_scores()`**
- Compare les secteurs des mesures avec ceux des entreprises.
- Calcule un score pour chaque entreprise :
  ```
  normalized_score = somme des sentiments / nombre de mesures pertinentes
  ```
- Pondération possible avec les poids des entreprises du S&P 500.

**Fonction : `load_all_measures()`**
- Agrège tous les CSVs de `shared/measures/` pour recomputation dynamique.

---

### 🧪 `pipeline.py`

**Fonction principale : `pipeline_add_law_and_recompute(file_path)`**
- Extrait les mesures.
- Enregistre dans `measures/`.
- Recharge les données entreprises.
- Calcule les scores et sauvegarde dans `data/final_company_scores.csv`.

---

### 🧪 `main.py`

Test minimal ciblé sur la directive 4 :  
- ✅ Vérifie que les mesures sont bien générées dans `measures/`
- ✅ Génère un CSV `final_company_scores.csv` dans `data/`
- 🔁 Sert de preuve de fonctionnement du pipeline bout-en-bout

---

## 📈 Exemple de sortie

| Symbol | Company               | nb_matched_measures | normalized_score | Weight   |
|--------|------------------------|----------------------|------------------|----------|
| AAPL   | Apple Inc.             | 5                    | -0.6             | 0.006    |
| JNJ    | Johnson & Johnson      | 3                    | 0.33             | 0.0056   |
| XOM    | ExxonMobil             | 2                    | 1.0              | 0.00003  |

Interprétation :
- `+1.0` → fortement favorisé
- `0.0` → pas d’effet détecté
- `-1.0` → impact réglementaire négatif

---

## 🛠️ Outils utilisés

| Outil / Service        | Rôle                                  |
|------------------------|---------------------------------------|
| **AWS Bedrock**        | Traitement LLM multilingue            |
| **langdetect**         | Détection automatique de langue       |
| **pandas**             | Analyse et nettoyage de données       |
| **Jupyter + EC2**      | Prototypage cloud                     |
| **S3**                 | Persistance automatique               |

---

## 🔮 Roadmap

- 🧠 Apprentissage supervisé sur des signaux de marché réels.
- 🧾 Extraction hiérarchique des lois (par articles).
- 📊 UI React avec Flask pour visualiser :
  - Mesures par secteur
  - Entreprises les plus sensibles
  - Scores pondérés globalement
- 🕒 Historique temporel multi-lois

