# UK-COVID19-Stats

A simple Flask app showing how the COVID-19 (SARS-CoV-2) pandemic is developing in the UK.

## Dependencies

```pipfile
[dev-packages]
autopep8 = "*"

[packages]
uk-covid19 = "*"
flask = "*"

[requires]
python_version = "3.8"
```

### Dependency installation

`pipenv install` or `pip install -r requirements.txt`

## Usage

### Development

1. Execute the following command to from the project directory to start the app locally:

#### PowerShell

`$Env:SECRET_KEY = $(python -c 'import os; print(os.urandom(16))'); $Env:FLASK_APP = 'app'; flask run`

#### Linux

`export SECRET_KEY=$(python -c 'import os; print(os.urandom(16))'); export FLASK_APP=app; flask run`

## Authors -- Contributors

* **dbrennand** - *Author* - [dbrennand](https://github.com/dbrennand)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details.
