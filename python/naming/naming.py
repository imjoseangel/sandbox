"""
This is the inventory module and supports all the REST actions for the
inventory data
"""

from flask import abort
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


def read_one(name, prefix=None, suffix=None):
    """
    This function responds to a request for /Naming/{name}
    with one matching item from resourceDefinition
    :param name:   name of resourceDefinition to find
    :return:       resourceDefinition matching name
    """

    # Empty prefix and suffix if not defined
    prefix = '' if prefix is None else prefix
    suffix = '' if suffix is None else suffix

    # Get the item requested
    naming = Naming.query.filter(
        Naming.name == name).one_or_none()

    # Did we find a mlw?
    if naming is not None:

        # Serialize the data for the response
        naming_schema = NamingSchema()
        data = naming_schema.dump(naming)

        dashes = '-' if data['dashes'] else ""

        return f"{prefix}{dashes}{data['slug']}{dashes}{suffix}"

    # Otherwise, nope, didn't find that item
    else:
        abort(
            404, f"Name not found for: {name}",
        )
