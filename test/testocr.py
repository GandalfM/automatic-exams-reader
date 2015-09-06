import unittest
from PIL import Image
from ocr import ocr

class TestOcr(unittest.TestCase):

    def test_image(self):
        image = Image.open("data/ocr/test-image-four.jpg")
        ocrModule = ocr.Ocr()
        readed = ocrModule.from_image(image)
        self.assertEqual(4, readed)

    def test_file(self):
        ocrModule = ocr.Ocr()
        readed = ocrModule.from_file("data/ocr/test-image-nine.jpg")
        self.assertEqual(9, readed)

if __name__ == '__main__':
    unittest.main()
