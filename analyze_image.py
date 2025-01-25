from flask import Flask, request, jsonify
import openai
from PIL import Image
import io
import base64

app = Flask(__name__)

# Replace with your OpenAI API key
OPENAI_API_KEY = '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'

openai.api_key = OPENAI_API_KEY

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file found'}), 400
    
    image_file = request.files['image']
    image = Image.open(image_file.stream)

    # Convert image to base64 for API
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Send to GPT-4o for analysis
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Identify all edible foods and ingredients in the given image."},
            {"role": "user", "content": [{"type": "image", "data": img_str}]}
        ]
    )

    ingredients = response['choices'][0]['message']['content']
    return jsonify({'ingredients': ingredients.split('\n')})

if __name__ == '__main__':
    app.run(debug=True)
