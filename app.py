from flask import Flask, render_template, request, jsonify
import os
import base64
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load your API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.get_json()
    base64_image = data['image']
    img_data = base64.b64decode(base64_image)

    try:
        genai.configure(api_key=GOOGLE_API_KEY)

        image_model = genai.GenerativeModel(
            model_name="gemini-1.0-pro-vision-latest",
            generation_config={
                "temperature": 0.4,
                "top_p": 1,
                "top_k": 32,
                "max_output_tokens": 4096,
            },
            safety_settings=[{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}]
        )

        image_parts = [{"mime_type": "image/jpeg", "data": img_data}]
        image_prompt_parts = [
            """
            Analyze the image in detail and provide a clear description of everything present. Include the following:
            Objects: List all identifiable objects (e.g., plastic bottle, cardboard box, apple core).
            Materials: Describe the materials of objects when possible (e.g., glass, metal, paper, steel, aluminum).
            Context: Mention any relevant context clues (e.g., objects on a kitchen counter, items in a garbage bin).
            State and Condition: Note the state of objects (e.g., whole, broken, clean, dirty). 
            """,
            image_parts[0],
            "\n"
        ]

        image_response = image_model.generate_content(image_prompt_parts)
        image_analysis_result = image_response.text

        text_model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config={
                "temperature": 0.8,
                "top_p": 1,
                "top_k": 40,
                "max_output_tokens": 2048,
            },
            safety_settings=[{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}]
        )

        text_prompt = f"""Based on the image analysis, determine the recyclability of the objects based on the meterials and the items: {image_analysis_result}"""
        text_response = text_model.generate_content([text_prompt])
        text_analysis_result = text_response.text

         # Extract materials and map to video IDs
        recommended_videos = []
        for material, ids in project_videos.items():
            if material in text_analysis_result.lower():
                recommended_videos.extend(ids)

        return jsonify({'result': text_analysis_result, 'videoIDs': recommended_videos})
    except Exception as e:
        return jsonify({'error': str(e)})

# A dictionary mapping materials to YouTube video IDs
project_videos = {
    'plastic bottle': ['Tzi_uTNT9_E', '8mVpl34OOHA', '0bl-pfdYaEk','rsnNciAnY9Y'],
    'plastic bag': ['j-7grMXIXs0','qTrsFgGBwcs','zz4P39WeTV8'],
    'container': ['KYj1f3c_re4', 'xwgX888Kn1Q', 'YoaCQ7CtCA0', 'W4_zew8yNug'],
    'tupperware': ['wGNi5Y3JX2Q', 'W4_zew8yNug', '0UMmG_sYKsI', 'OV6RUa5ceSU'],
    'pens': ['sY2sX96nORI', 'X9Fx9fxhNJQ', 'FEd0C_m6i7E', 'S8t9sHXBf_8'],
    'shirt': ['5KzN8oLMjBI', 'cTQ0_rLrhMc', 'I2CrkTE8NSI', 'bN7J4fJCxqM'],
    'cloth': ['SNMHT7kTuI8', '1xVcdOYn2ac', 'LTB-jWWbBGc', '6hPQp4RzyMQ'],
    'paper': ['p7tR5uIqX6o', 'Yss3-upCVWM', 'z67q-hbfoUQ', 'b9qUu4NAgkY'],
    'fabric': ['87q81l-n5uU', '1xVcdOYn2ac', 'jZQDeOEDnms', 'LclnmAmtGEI'],
    'glass': ['8f2l2rSwedI', '7pVn1DfkgCE', '0kbnzmyf6ME', 'I8YbZIFLJZk'],
    'steel': ['nV4pmosgq2w', 'ozrYIv_z6gI', 'NE72xupoUps'],
    'aluminum': ['bM6g9_lgxNk', 'gJIChIs4g6A', 'mfoFLx67tWk', 'BMg37tRZauI']
}

if __name__ == "__main__":
    app.run(debug=True)

