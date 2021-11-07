"""
This is the inventory module and supports all the REST actions for the
inventory data
"""

from flask import make_response, abort
from config import db
from models import Naming, NamingSchema


def read_all():
    """
    This function responds to a request for /inventory
    with the complete lists of items

    :return:        json string of list of items
    """
    # Create the list of servers from our data
    naming = Naming.query.order_by(Naming.name).all()

    # Serialize the data for the response
    naming_schema = NamingSchema(many=True)
    data = naming_schema.dump(naming)
    return data


def read_one(name, prefix=None):
    """
    This function responds to a request for /Naming/{name}
    with one matching item from resourceDefinition
    :param name:   name of resourceDefinition to find
    :return:       resourceDefinition matching name
    """

    # Empty prefix if not defined
    prefix = '' if prefix is None else prefix

    # Get the item requested
    naming = Naming.query.filter(
        Naming.name == name).one_or_none()

    # Did we find a mlw?
    if naming is not None:

        # Serialize the data for the response
        naming_schema = NamingSchema()
        data = naming_schema.dump(naming)
        return f"{prefix}{data['slug']}"

    # Otherwise, nope, didn't find that item
    else:
        abort(
            404,
            "Name Register not found: {name}".format(name=name),
        )
