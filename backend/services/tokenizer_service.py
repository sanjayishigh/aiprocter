import os
from flask import request
from openai import OpenAI
from utils.constants import HF_TOKEN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
api_key = HF_TOKEN
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)


class tokenizer_service:
    @staticmethod
    def run_inference():
        
        data = request.get_json()
        question = data.get('question', '')

        completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3.2:novita",
        messages=[
            {
                "role": "user",
                "content": question + " give only code in one method"
            }
            ],
        )
        content = completion.choices[0].message.content

        if content.startswith("```"):
            content = content.split("```")[1]
            
        return content.strip()
    @staticmethod
    def add_inference(question_text ):
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2:novita",
            messages=[
                {
                    "role": "user",
                    "content": question_text +" give only code in one method"
                }
            ],
        )

        content = completion.choices[0].message.content

        if content.startswith("```"):
            content = content.split("```")[1]
            
        return content.strip()
    @staticmethod
    def clean_code(code: str):
        """Remove language headers, backticks, comments, and normalize whitespace"""

        # Remove ```python or ``` or ```java etc.
        code = re.sub(r"```.*?\n", "", code)
        code = re.sub(r"```", "", code)

        # Remove single-line comments (#, //)
        code = re.sub(r"#.*", "", code)
        code = re.sub(r"//.*", "", code)

        # Remove multi-line comments (/* */)
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)

        # Normalize whitespace
        code = code.strip().lower()

        # Split into lines and remove empty lines
        lines = [line.strip() for line in code.split("\n") if line.strip()]

        return lines


    @staticmethod
    def check_code():
        """
        Convert codes into normalized arrays of strings,
        clean them, then compute cosine similarity
        """

        # Step 1: Clean & convert codes into line arrays
        data = request.json() 
        code1 , code2 = data.get("code1") , data.get("code2")
        c1_lines = tokenizer_service.clean_code(code1)
        c2_lines = tokenizer_service.clean_code(code2)

        # Step 2: Join lines because TF-IDF works on full text
        text1 = " ".join(c1_lines)
        text2 = " ".join(c2_lines)

        # Step 3: TF–IDF Vectorization
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([text1, text2])

        # Step 4: Cosine similarity
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

        return {
            "similarity_score": float(similarity),
            "percentage": round(similarity * 100, 2),
            "code1_cleaned": c1_lines,
            "code2_cleaned": c2_lines
        }


