gen_ai_classification_template = """
You are an expert assistant that identifies if a technology news article is related to generative AI (GenAI) innovations.

Analyze the article below:

Title: "{title}"
Summary: "{summary}"

Answer these questions:

1. Is this article about generative AI innovations? (Answer "True" or "False")
2. If True, how many distinct GenAI innovations does it describe? (Number only)

Return your answer strictly as a JSON string. Do NOT wrap it in a code block or Markdown formatting. Only output the JSON, nothing else.

{{
  "is_genai_related": "True" or "False",
  "innovation_count": <number>
}}
"""