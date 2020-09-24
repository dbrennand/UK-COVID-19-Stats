from flask import Flask, render_template, url_for, flash, redirect
from uk_covid19 import Cov19API
from uk_covid19.exceptions import FailedRequestError
import os
from feedparser import parse
from re import findall, IGNORECASE
# Logging and debug imports
from loguru import logger
from pprint import pprint

__version__ = "0.0.2"

# Init Flask app
app = Flask(__name__)
# Set application secret key from environment variable
# If environment is not present, generate a random secret key
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(16))


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

    logger.debug(
        "Attempting to make request to the Public Health England COVID-19 API.")
    # Obtain JSON from the API
    response = api.get_json()
    # Log JSON response to logger
    logger.debug(pprint(response))
    return response


def get_health_feed():
    """
    Parse BBC news health feed and remove articles not related to COVID-19.
    """
    feed = parse("http://feeds.bbci.co.uk/news/health/rss.xml")
    # log parsed feed for debugging purposes
    logger.debug(pprint(feed.entries))
    logger.debug(f"Feed items before removal: {len(feed.entries)}.")
    # Remove all feed items not related to COVID-19
    for index, article in enumerate(feed.entries):
        if any(findall(r'Coronavirus|COVID|Covid|Covid-19', article.title, IGNORECASE)):
            continue
        else:
            logger.debug(f"Removing item at index: {index}.")
            feed.entries.pop(index)
    return feed


@app.route("/error", methods=["GET"])
def error():
    """
    Error page.
    """
    return render_template("error.html")


@app.route("/news", methods=["GET"])
def news():
    """
    Health news related to COVID-19.
    """
    feed = get_health_feed()
    return render_template("news.html", feed=feed)


@app.route("/", methods=["GET"])
def index():
    """
    Serve index page.
    """
    try:
        data = get_latest_covid_stats()
    except FailedRequestError as err:
        # Log error response to logger
        logger.debug(
            f"Request to Public Health England COVID-19 API failed: {err}.")
        flash("An error occurred obtaining latest COVID-19 stats from the Public Health England API.")
        return redirect(url_for("error"))
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(host=os.environ.get("FLASK_HOST", "127.0.0.1"))
