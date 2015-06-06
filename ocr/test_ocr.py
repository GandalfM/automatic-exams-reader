import unittest
from PIL import Image
from ocr import ocr

class TestOcr(unittest.TestCase):

    def test_image(self):
        image = Image.open("testdata/ocr/test-image-four.jpg")
        ocrModule = ocr.Ocr()
        readed = ocrModule.from_image(image)
        print("Recognized {} - should be 4".format(readed))

    def test_file(self):
        ocrModule = ocr.Ocr()
        readed = ocrModule.from_file("testdata/ocr/test-image-nine.jpg")
        print("Recognized {} - should be 9".format(readed))

if __name__ == '__main__':
    unittest.main()