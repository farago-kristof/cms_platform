import os
from json import loads

import google.generativeai as genai

from common.db import CMSDataBase
from common.utils import retry_with_exponential_backoff
from config import POSTGRES_CONNECTION
from templates import gen_ai_classification_template

MODEL = "models/gemini-1.5-flash-latest"


def classify_article(article_id):
    with CMSDataBase(POSTGRES_CONNECTION) as db:
        article = db.get_article_by_id(article_id)
        if article is not None:
            title = article['title']
            content = article['content']
            prompt = gen_ai_classification_template.format(title=title, summary=content)
            genai.configure(api_key=os.environ['GEMINI_API_KEY'])
            model = genai.GenerativeModel(model_name=MODEL)
            response = retry_with_exponential_backoff(
                func=model.generate_content,
                args=(prompt,),
                exceptions=(Exception,)
            )
            raw_text = response.candidates[0].content.parts[0].text
            response_dict = loads(raw_text)
            db.insert_article_classification(
                article_id=article_id,
                is_genai_related=response_dict.get('is_genai_related', False),
                innovation_count=response_dict.get('innovation_count', 0)
            )
