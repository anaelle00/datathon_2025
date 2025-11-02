def extract_measures_from_file(file_path):
    import os, json, langdetect, re
    from bs4 import BeautifulSoup
    import boto3

    bedrock = boto3.client('bedrock-runtime')

    text = open(file_path, encoding="utf-8").read()
    soup = BeautifulSoup(text, "html.parser")
    content = soup.get_text(separator=" ", strip=True)

    try:
        lang = langdetect.detect(content[:1000])
    except:
        lang = "unknown"

    prompt = f"""
You are a multilingual legal and financial analyst.
Your task is to analyze the following regulation text and translate it into English if needed.

Then extract a list of concrete regulatory MEASURES contained in the law. For each measure, return a JSON object with:

- law_name: title of the law associated with the measure
- country: country or region concerned
- type_of_regulation: type of the regulation (e.g. law, directive, regulation, tax, subsidy, etc.)
- application_date: application date in format YYYY-MM-DD (or "Not specified")
- sector: one or more sectors affected by the measure (choose from ['Technology', 'Finance', 'Energy', 'Healthcare', 'Industrials', 'Public Services'])
- measure_text: one clear sentence summarizing the measure (in English)
- sentiment_score:
    +1 → if the measure is expected to create business opportunities, reduce barriers, or stimulate innovation/investment
    -1 → if the measure imposes compliance costs, limits business activity, or increases financial or legal obligations

When evaluating sentiment, consider the overall economic effect for companies in the affected sectors, not just the wording. Some regulatory requirements (e.g. environmental, consumer protection, safety) may be neutral or even positive if they foster clarity, market efficiency, or long-term competitiveness.

Use keyword guidance only as a hint:
→ Positive indicators: promote, support, enable, facilitate, enhance, simplify, incentivize, invest, protect
→ Negative indicators: impose, restrict, penalize, ban, mandate, tax, enforce, fine

💡 Try to extract at least 5 to 10 distinct measures if present in the text. Avoid merging several provisions into a single vague statement.
Note: Some regulatory frameworks may appear restrictive but still have a positive long-term business impact (e.g. incentives for green technology adoption, clearer rules for AI usage, consumer trust improvements). Take that into account when scoring.

Respond ONLY with a JSON list of dictionaries, one per measure.
Text:
{content[:3000]}
"""

    try:
        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps({
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 850,
                "temperature": 0.2,
                "top_p": 0.9,
                "anthropic_version": "bedrock-2023-05-31"
            })
        )
        body = json.loads(response['body'].read())
        completion = body['content'][0]['text'].strip()
        completion = completion.replace("```json", "").replace("```", "").strip()

        match = re.search(r'\[.*\]', completion, re.DOTALL)
        if not match:
            match = re.search(r'\{.*\}', completion, re.DOTALL)

        if match:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, dict):
                parsed = [parsed]
            for m in parsed:
                m["source_file"] = os.path.basename(file_path)
                m["language_detected"] = lang
            return parsed
        else:
            print(f"⚠️ No JSON found in output from {file_path}")
            return []

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return []

def save_measures_to_csv(measure_list, output_dir="measures"):
    import os
    import pandas as pd

    if not measure_list:
        return

    df = pd.DataFrame(measure_list)

    # Déduire le nom de fichier à partir du champ source_file
    filename = measure_list[0].get("source_file", "law.csv")
    filename = filename.replace(".html", ".csv").replace(".xml", ".csv")
    
    path = os.path.join(output_dir, filename)
    df.to_csv(path, index=False)
    print(f"✅ Saved {len(df)} measures to {path}")
