"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import redirect


def home():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    return redirect("./ui", code=302)
