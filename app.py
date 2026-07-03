from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os
import json
import urllib.parse

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


@app.route("/generate", methods=["POST"])
def generate():

    try:

        data = request.json

        planet = data["planet"]
        habitat = data["habitat"]
        iq = data["iq"]
        body = data["body"]

        prompt = f"""
Generate ONE completely original alien species.

Planet Type: {planet}
Habitat: {habitat}
IQ Level: {iq}
Body Type: {body}

RULES

- Name: maximum 2 words
- Home World: maximum 3 words
- Life Span: maximum 4 words
- Threat Level: ONE word
- Body Type: ONE word
- Special Trait: maximum 2 words
- Description: 80-190 words
- Biology: 80-150 words
- Quote: 4-12 words

Return ONLY valid JSON.

{{
"name":"",
"home_world":"",
"life_span":"",
"threat_level":"",
"body_type":"",
"special_trait":"",
"description":"",
"biology":"",
"quote":""
}}
"""

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.9

        )

        text = response.choices[0].message.content.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        species = json.loads(text)

      

        alien_prompt = f"""
            Realistic alien portrait of {species['name']},
            {species['description']},
            highly detailed,
            concept art,
            black background,
            centered,
            cinematic lighting
            """

        planet_prompt = f"""
            Realistic alien planet called {species['home_world']},
            Planet Type: {planet},
            Habitat: {habitat},
            beautiful landscape,
            cinematic,
            science fiction,
            concept art
            """

        species["alien_image"] = (
            "https://image.pollinations.ai/prompt/"
            + urllib.parse.quote(alien_prompt)
        )

        species["planet_image"] = (
            "https://image.pollinations.ai/prompt/"
            + urllib.parse.quote(planet_prompt)
        )

        return jsonify(species)

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)