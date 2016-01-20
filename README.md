# automatic-exams-reader

### Dependencies
* Python 3.4
* OpenCV 3.0 compiled with Python3 wrapper
* PyQt 5 with pyuic5 command
* Tesseract engine (https://github.com/tesseract-ocr/tesseract)

All python requirements are listed in `requirements.txt` file (you can install them via `pip`)


### First run
    export PYTHONPATH=$PYTHONPATH:`pwd`
	cd aer
	python3 convert-ui.py
	python3 learn_classifier.py
	python3 main.py

### Additional learning methods
Please, type `python3 learn_classifier.py --help` for more learning methods and help (e.g. including additional files).

The best (empiric) solution is `RandomForestClassifier` with additional data (not only MNIST database).

### Run
    cd aer
    python3 main.py
