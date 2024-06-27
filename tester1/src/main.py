from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import io
import base64
from flask_cors import CORS
from approaches.Approach1 import Approach1
from approaches.Approach2 import Approach2

app = Flask(__name__)
CORS(app)


@app.route("/filter-image", methods=["POST"])
def filter_image():
    data = request.json["image"]
    base64_data = data.split(",")[1]
    image_data = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(image_data))
    image_array = np.array(image)

    # Convert images to bytes and then to base64
    def convert_to_base64(image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    # Approach 1
    approach1 = Approach1(image_array)
    image_approach1 = approach1.process_image()
    image1 = Image.fromarray(image_approach1)

    # Approach 2
    approach2 = Approach2(image_array)
    image_approach2 = approach2.process_image()
    image2 = Image.fromarray(image_approach2)

    image_enhanced1 = convert_to_base64(image1)
    image_enhanced2 = convert_to_base64(image2)

    return jsonify(
        {
            "approach1": f"data:image/png;base64,{image_enhanced1}",
            "approach2": f"data:image/png;base64,{image_enhanced2}",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
