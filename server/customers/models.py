
import sqlalchemy as sa

from db import models


class Customer(models.Base):
    # Table
    __tablename__ = "customer"

    # Fields
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)

    def __repr__(self):
        return "Customer(id={}, name={})".format(id, name)

