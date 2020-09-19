from flask import Flask, render_template, url_for, flash, redirect
from uk_covid19 import Cov19API

__version__ = "0.0.1"

# Init Flask app
app = Flask(__name__)
app.secret_key = b''


def get_latest_covid_stats():
    """
    Obtain current statistics from Public Health Englands COVID-19 API.
    :return: A Python dictionary object containing the response from the Public Health England API.
    """
    # Declare response structure to retrieve
    structure = {
        "date": "date",
        "name": "areaName",
        "code": "areaCode",
        "stats": {
            "cases": {
                "New cases": {
                    "value": "newCasesByPublishDate"
                },
                "Cumulative cases": {
                    "value": "cumCasesByPublishDate"
                },
                "Male cases": {
                    "value": "maleCases"
                },
                "Female cases": {
                    "value": "femaleCases"
                },
                "Hospital cases": {
                    "value": "hospitalCases"
                },
                "COVID-19 occupied beds with mechanical ventilators": {
                    "value": "covidOccupiedMVBeds"
                }
            },
            "deaths": {
                "Daily deaths": {
                    "value": "newDeaths28DaysByDeathDate",
                },
                "Cumulative deaths": {
                    "value": "cumDeaths28DaysByDeathDate"
                }
            },
            "admissions": {
                "New admissions": {
                    "value": "newAdmissions"
                },
                "Cumulative admissions": {
                    "value": "cumAdmissions"
                }
            },
            "tests": {
                "New pillar one tests by publish date": {
                    "metadata": "Pillar 1 (NHS and, in England, PHE)",
                    "value": "newPillarOneTestsByPublishDate"
                },
                "Cumulative pillar one tests by publish date": {
                    "metadata": "Pillar 1 (NHS and, in England, PHE)",
                    "value": "cumPillarOneTestsByPublishDate"
                },
                "New pillar two tests by publish date": {
                    "metadata": "Pillar 2 (Commercial partners)",
                    "value": "newPillarTwoTestsByPublishDate"
                },
                "Cumulative pillar two tests by publish date": {
                    "metadata": "Pillar 2 (Commercial partners)",
                    "value": "cumPillarTwoTestsByPublishDate"
                },
                "New pillar three tests by publish date": {
                    "metadata": "Pillar 3 (Antibody)",
                    "value": "newPillarThreeTestsByPublishDate"
                },
                "Cumulative pillar three tests by publish date": {
                    "metadata": "Pillar 3 (Antibody)",
                    "value": "cumPillarThreeTestsByPublishDate"
                },
                "New pillar four tests by publish date": {
                    "metadata": "Pillar 4 (Surveillance)",
                    "value": "newPillarFourTestsByPublishDate"
                },
                "Cumulative pillar four tests by publish date": {
                    "metadata": "Pillar 4 (Surveillance)",
                    "value": "cumPillarFourTestsByPublishDate"
                }
            }
        }
    }

    # Instantiate API object
    api = Cov19API(
        filters=["areaType=nation"],
        structure=structure,
        latest_by="newCasesByPublishDate"
    )

    # Obtain JSON from the API
    response = api.get_json()
    return response


@app.route("/error", methods=["GET"])
def error():
    """
    Error page.
    """
    return render_template("error.html")


@app.route("/", methods=["GET"])
def index():
    """
    Serve index page.
    """
    try:
        data = get_latest_covid_stats()
    except:
        flash("An error occurred obtaining latest COVID-19 stats from the Public Health England API.")
        return redirect(url_for("error"))
    return render_template("index.html", data=data)
