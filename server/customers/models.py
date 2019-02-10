
import sqlalchemy as sa

from db import models
from utils.models import ProtobufModelMixin


class Customer(ProtobufModelMixin, models.Base):
    # Table
    __tablename__ = "customer"

    # Fields
    id = sa.Column(sa.Integer,
                   sa.Sequence('customer_id_seq'),
                   primary_key=True)
    name = sa.Column(sa.String, nullable=False)

    def __repr__(self):
        return "Customer(id={}, name={})".format(self.id, self.name)

