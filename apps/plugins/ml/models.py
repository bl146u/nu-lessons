import io
import numpy

from PIL import ImageOps, Image
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

from django.conf import settings


class DigitsModel:
    model: Sequential

    def __init__(self):
        self.model = load_model(f"{settings.ML_MODELS_PATH}/digits.h5")

    def _exif_transpose(self, img: Image):
        if not img:
            return img

        exif_orientation_tag = 274

        if (
            hasattr(img, "_getexif")
            and isinstance(img._getexif(), dict)
            and exif_orientation_tag in img._getexif()
        ):
            exif_data = img._getexif()
            orientation = exif_data[exif_orientation_tag]

            # Handle EXIF Orientation
            if orientation == 1:
                # Normal image - nothing to do!
                pass
            elif orientation == 2:
                # Mirrored left to right
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                # Rotated 180 degrees
                img = img.rotate(180)
            elif orientation == 4:
                # Mirrored top to bottom
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                # Mirrored along top-left diagonal
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                # Rotated 90 degrees
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                # Mirrored along top-right diagonal
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                # Rotated 270 degrees
                img = img.rotate(90, expand=True)

        return img

    def _image_to_byte_array(self, img: Image) -> bytes:
        bio = io.BytesIO()
        img.save(bio, format="JPEG")
        bio = bio.getvalue()
        return bio

    def _processing_image(self, image_uuid: str) -> tuple:
        image_path = f"{settings.MEDIA_ROOT}/{image_uuid}.jpg"
        img = image.load_img(image_path, target_size=(28, 28), color_mode="grayscale")
        if hasattr(ImageOps, "exif_transpose"):
            img = ImageOps.exif_transpose(img)
        else:
            img = self._exif_transpose(img)
        img = ImageOps.invert(img)
        data = image.img_to_array(img).astype("uint8")
        # data[(data < 120)] = 0
        # data[(data >= 160) & (data < 200)] = 127
        # data[(data >= 200)] = 255
        # data = (data.astype("uint8") * 255).reshape((28, 28))
        data = ((data > 160).astype("uint8") * 255).reshape((28, 28))
        return data, Image.fromarray(data, "L")

    def _load_image(self, image_uuid: str) -> numpy.ndarray:
        data_source, img = self._processing_image(image_uuid)
        img.save(f"{settings.MEDIA_ROOT}/{image_uuid}-processed.jpg")
        data = data_source.reshape(1, 28 * 28).astype("float32") / 255
        return data

    def predict(self, image_uuid) -> tuple:
        data = self._load_image(image_uuid)
        predictions = self.model.predict(data)
        dig = numpy.argmax(predictions)
        predictions_list = []
        for index in range(10):
            predictions_list.append(f'{index}: {format(predictions[0][index], ".28f")}')
        return "<br />".join(predictions_list), dig
