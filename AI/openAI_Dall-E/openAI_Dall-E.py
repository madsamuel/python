import sys
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Function to generate the image based on the user's prompt
def generate_image(prompt, window):
    if not prompt:
        QMessageBox.critical(window, "Error", "Please enter a prompt.")
        return

    try:
        response = client.images.generate(prompt=prompt)
        image_url = response.data[0].url
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            save_path, _ = QFileDialog.getSaveFileName(window, "Save Image", "", "PNG files (*.png)")
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(image_response.content)
                QMessageBox.information(window, "Success", f"Image saved to {save_path}")
            else:
                QMessageBox.warning(window, "Warning", "Save operation cancelled.")
        else:
            QMessageBox.critical(window, "Error", "Failed to download the image.")
    except Exception as e:
        QMessageBox.critical(window, "Error", f"An error occurred: {e}")

class ImageGeneratorApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ImageGeneratorApp, self).__init__()
        uic.loadUi("image_generator.ui", self)

        # Connect the button to the function
        self.generateButton.clicked.connect(self.on_generate_button_click)

    def on_generate_button_click(self):
        prompt = self.promptInput.text()
        generate_image(prompt, self)

# Run the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImageGeneratorApp()
    window.show()
    sys.exit(app.exec_())
