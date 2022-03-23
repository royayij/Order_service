from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from daos.status_dao import StatusDAO
from db import Base


class OrderDAO(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    customer_id = Column(String)
    product_id = Column(String)
    order_time = Column(DateTime)
    delivery_time = Column(DateTime)
    # reference to status as foreign key relationship. This will be automatically assigned.
    status_id = Column(Integer, ForeignKey('status.id'))
    # https: // docs.sqlalchemy.org / en / 14 / orm / basic_relationships.html
    # https: // docs.sqlalchemy.org / en / 14 / orm / backref.html
    status = relationship(StatusDAO.__name__, backref=backref("order", uselist=False))

    def __init__(self, customer_id, product_id, order_time, delivery_time, status):
        self.customer_id = customer_id
        self.product_id = product_id
        self.order_time = order_time
        self.delivery_time = delivery_time
        self.status = status
