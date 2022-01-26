run:
	python -m streamlit run app.py

py_format:  ## Run black and isort to format the Python codebase
	isort . --profile black --multi-line 3
	black .
