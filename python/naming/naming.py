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
    data = inventory_schema.dump(naming)
    return data


def read_one(index):
    """
    This function responds to a request for /mlw/{index}
    with one matching item from mlw
    :param index:   Id of mlw to find
    :return:               Mlw matching id
    """
    # Get the item requested
    naming = Naming.query.filter(
        Naming.index == index).one_or_none()

    # Did we find a mlw?
    if naming is not None:

        # Serialize the data for the response
        naming_schema = NamingSchema()
        data = naming_schema.dump(mlw)
        return data

    # Otherwise, nope, didn't find that item
    else:
        abort(
            404,
            "MLW Register not found for Id: {index}".format(
                index=index),
        )
