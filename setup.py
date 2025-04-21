from setuptools import setup , find_packages

from typing import List

HYPEN_E_DOT = "-e."
def get_requirements(file_path:str)->List[str]:
    requirements =[]
    with open(file_path) as file_object:
        reuirements = file_object.readlines()
        requirements = [req.replace("\n"," ") for req in requirements]

    if HYPEN_E_DOT in get_requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name ="fault detection",
    version = "0.0.1",
    author ="Anuj",
    author_mail = "anujdangwal20gmail.com",
    install_packages = get_requirements("requirements.txt")
)