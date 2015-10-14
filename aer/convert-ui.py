import os

os.chdir("views")
for file in os.listdir("."):
    if file.endswith(".ui"):
        os.system("pyuic5 {} -o {}".format(file, file.replace(".ui", ".py")))
