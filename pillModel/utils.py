import tensorflow as tf
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
from io import BytesIO
from base64 import b64decode

class Model:
    def __init__(self):
        self.model = tf.keras.models.load_model("pillModel/pill_classifier_model_v1.h5")
        self.class_labels = [2, 3, 4, 5]
        self.img_height = 150
        self.img_width = 150
        
    def decode_base64_image(self, base64_image):
        # Decode the Base64 string to image data
        image_data = b64decode(base64_image)
        img = Image.open(BytesIO(image_data))
        return img

    def preprocess_image(self, img):
        # Convert PIL image to NumPy array
        img = img_to_array(img)

        # Resize the image to match model's expected input size
        img = tf.image.resize(img, (self.img_height, self.img_width))
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        img = img / 255.0  # Normalize to [0, 1]
        return img

    def predict(self, base64_image):
        try:
            # Decode the Base64 image and preprocess it
            img = self.decode_base64_image(base64_image)
            print(f"the typeof the decoded base64 image is {type(img)}")
            img = self.preprocess_image(img)

            # Make the prediction
            predictions = self.model.predict(img)
            predicted_index = np.argmax(predictions)  # Get the index of the highest probability
            predicted_label = self.class_labels[predicted_index-1]
            confidence = float(np.max(predictions))  # Confidence score

            return {
                "predicted_label": (predicted_label),
                "confidence": confidence
            }
        except Exception as e:
            raise ValueError(f"Error during prediction: {str(e)}")
