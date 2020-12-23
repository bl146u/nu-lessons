import numpy

from PIL import ImageOps
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

from django.conf import settings


class DigitsModel:
    model: Sequential

    def __init__(self):
        self.model = load_model(f"{settings.ML_MODELS_PATH}/digits.h5")

    def _load_image(self, image_path) -> numpy.ndarray:
        img = image.load_img(image_path, target_size=(28, 28), color_mode="grayscale")
        img = ImageOps.invert(img)
        data = image.img_to_array(img)
        data = data.reshape(1, 28 * 28).astype("float32") / 255
        return data

    def predict(self, image_uuid) -> tuple:
        data = self._load_image(f"{settings.MEDIA_ROOT}/{image_uuid}.jpg")
        predictions = self.model.predict(data)
        dig = numpy.argmax(predictions)
        predictions_list = []
        for index in range(10):
            predictions_list.append(f'{index}: {format(predictions[0][index], ".28f")}')
        return "<br />".join(predictions_list), dig
