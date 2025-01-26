from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
import base64
from flask_cors import CORS
import openai
import traceback

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": "*"}})

# Replace this with your valid OpenAI API key
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file found'}), 400

    try:
        image_file = request.files['image']
        image = Image.open(image_file.stream)

        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Make an API call to OpenAI's image model (GPT-4 Vision Preview)
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What ingredients do you see in this image?"},
                        {"type": "image_url", "image_url": f"data:image/png;base64,{img_str}"}
                    ],
                }
            ],
            max_tokens=300
        )

        # Assuming the response contains a comma-separated list of ingredients
        ingredients = response['choices'][0]['message']['content'].split(',')
        return jsonify({'ingredients': ingredients})

    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
