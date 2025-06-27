from setuptools import setup, find_packages

readme = open("./README.md", "r")

setup(name="etacad",
      packages=find_packages(),
      version="0.0.14",
      description="A package aimed to simpilfy drawings of structurals elements based on ezdxf library.",
      long_description=readme.read(),
      long_description_content_type="text/markdown",
      author="Kevin Axel Tagliaferri",
      author_email='kevinaxeltagliaferri@hotmail.com',
      url="https://github.com/AxelTAG/etacad.git",
      install_requires=["attrs", "ezdxf"])
