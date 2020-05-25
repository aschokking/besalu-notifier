# Requires twine to be installed and having creds to the pypi project
python setup.py sdist bdist_wheel
python -m twine upload --skip-existing dist/*
