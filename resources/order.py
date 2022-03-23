from datetime import datetime

from flask import jsonify

from constant import STATUS_CREATED
from daos.order_dao import OrderDAO
from daos.status_dao import StatusDAO
from db import Session


class Order:
    @staticmethod
    def create(body):
        session = Session()
        order = OrderDAO(body['customer_id'], body['product_id'], datetime.now(),
                               datetime.strptime(body['delivery_time'], '%Y-%m-%d %H:%M:%S.%f'),
                               StatusDAO(STATUS_CREATED, datetime.now()))
        session.add(order)
        session.commit()
        session.refresh(order)
        session.close()
        return jsonify({'order_id': order.id}), 200

    @staticmethod
    def get(o_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        order = session.query(OrderDAO).filter(OrderDAO.id == o_id).first()

        if order:
            status_obj = order.status
            text_out = {
                "customer_id:": order.customer_id,
                "product_id": order.product_id,
                "order_time": order.order_time.isoformat(),
                "delivery_time": order.delivery_time.isoformat(),
                "status": {
                    "status": status_obj.status,
                    "last_update": status_obj.last_update.isoformat(),
                }
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no delivery with id {o_id}'}), 404

    @staticmethod
    def delete(o_id):
        session = Session()
        effected_rows = session.query(OrderDAO).filter(OrderDAO.id == o_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no order with id {o_id}'}), 404
        else:
            return jsonify({'message': 'The delivery was removed'}), 200
