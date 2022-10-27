# How To Release & Publish on Pypi


- Update ./setup.py and ./pyproject.toml with correct release number
- Update contributors in ./pyproject.toml and ./AUTHORS
- Prepare the tag and push the commits tagged
- Follow next intructions to build and publish the package

```bash

# Install the necessary tools
python -m pip install build twine

# Build the package
python3 -m build

# Check the package
twine check dist/*

# Upload to Pypi once registred
twine upload -r pypi dist/*
```


https://realpython.com/pypi-publish-python-package/#publish-your-package-to-pypi
