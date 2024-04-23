from flask import Flask, render_template, request, jsonify
import os
import base64
from dotenv import load_dotenv
import google.generativeai as genai
#AIzaSyDruxxPPJiOskvUtaVrs8snyzDirMSlu6k GMAPS
load_dotenv()  # Load your API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

app = Flask(__name__)

# Separate dictionaries for locations and videos
material_locations = {
    'plastic': ['Boyd E. Diller Transfer Station Drop-Off Recycling, 6820 Wertzville Road, Enola, PA 17025'],
    'glass': ['New Hope Recycling, 415 Three Square Hollow Road, Newburg, PA 17240'],
    'paper': ['Waste Management of Central Pennsylvania Transfer Station Drop-Off Recycling, 4300 Industrial Park Road, Camp Hill, PA 17011'],
    'metal': ['Cumberland County Landfill Drop-Off Recycling, 620 Newville Road, Newburg, PA 17240'],
}

material_videos = {
    'plastic bottle': ['Tzi_uTNT9_E', '8mVpl34OOHA', '0bl-pfdYaEk'],
    'plastic': ['j-7grMXIXs0', 'qTrsFgGBwcs', 'zz4P39WeTV8'],
    'glass jar': ['8f2l2rSwedI', '7pVn1DfkgCE', '0kbnzmyf6ME'],
    'paper': ['p7tR5uIqX6o', 'Yss3-upCVWM', 'z67q-hbfoUQ'],
    'aluminum can': ['bM6g9_lgxNk', 'gJIChIs4g6A', 'mfoFLx67tWk']
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

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

        # Image model setup
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

        # Text model for further analysis
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

        text_prompt = f"Based on the image analysis, determine the recyclability of the objects and make the response as useful as possible in terms of sustaiability, ensuring the response stays below 300 characters: {image_analysis_result}"
        text_response = text_model.generate_content([text_prompt])
        text_analysis_result = text_response.text

        # Check for keywords and assign videos and map locations
        recommended_videos = []
        map_locations = []
        for material, info in material_videos.items():
            if material in text_analysis_result.lower():
                recommended_videos.extend(info)
        for material, locations in material_locations.items():
            if material in text_analysis_result.lower():
                map_locations.extend(locations)

        return jsonify({
            'result': text_analysis_result,
            'videoIDs': recommended_videos,
            'locations': map_locations
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
