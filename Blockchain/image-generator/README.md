## About
Python Notebook in Jupyter that will generate a series of unique images using a collection of layers.

## Getting Started
1. Install [Python](https://www.python.org/downloads/)

2. Install Python Jupyter
pip install jupyter

3. Install Python Pillow
```
pip install pillow
```

4. Install Python display
```
pip install display
```

5. First time you run notebook, it will ask you to install ipykernel, accept this.
 
6. If the program executes successfully, it will output all the generated images to the /images folder, and the metadata to the /metadata folder. The filenames will refer to tokenIds.

## commando para ejecutar el programita
jupyter nbconvert --to notebook --execute generate.ipynb
