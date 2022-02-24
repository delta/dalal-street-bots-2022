"""Class manager for all order related action service actions"""

"""Class manager for all bot action service actions"""
import logging
from typing import Tuple, Union
from .base_action_service import BaseActionService

from proto_build.actions.CancelOrder_pb2 import CancelOrderRequest, CancelOrderResponse
from proto_build.actions.PlaceOrder_pb2 import PlaceOrderRequest, PlaceOrderResponse
from proto_build.actions.GetMyOrders_pb2 import (
    GetMyOpenOrdersRequest,
    GetMyOpenOrdersResponse,
    GetMyClosedBidsRequest,
    GetMyClosedAsksRequest,
    GetMyClosedAsksResponse,
    GetMyClosedBidsResponse,
)
from proto_build.models.OrderType_pb2 import OrderType


class OrderActionService(BaseActionService):
    """Helper class to handle all order related grpc requests"""

    async def candel_order(
        self, bot_id: int, order_id: int, is_ask: bool
    ) -> Tuple[Union[CancelOrderResponse, None], Union[Exception, None]]:
        """Cancel order request"""

        order_details = {
            "bot_id": bot_id,
            "is_ask": is_ask,
            "order_id": order_id,
        }

        logging.info(f"Trying to cancel order with {order_details=}")

        try:
            cancelOrderRequest = CancelOrderRequest(order_id=order_id, is_ask=is_ask)

            resp: CancelOrderResponse = await self.action_stub.CancelOrder(
                cancelOrderRequest,
                metadata=self.metadata.get_bot_meta_data_with_given_user_id(order_id),
            )

            if resp.status_code > 0:
                # Some error occurred, sending resp and status_message as response
                logging.info(
                    f"cancel order with {order_details=} failed due to={resp.status_message}"
                )
                return resp, resp.status_message

            logging.info(f"Successfully cancelled order with {order_details=}")
            return resp, None
        except TypeError as e:
            # We get type error when data validation for request fails
            logging.error(f"Type check failed {e}")
            return None, e
        except Exception as e:
            logging.error(
                f"Unable to cancel order with  {order_details=} due to {e}",
                exc_info=True,
            )
            return None, e

    async def place_order(
        self,
        bot_id: int,
        is_ask: bool,
        stock_id: int,
        price: int,
        stock_quantity: int,
        order_type: OrderType,
    ) -> Tuple[Union[PlaceOrderResponse, None], Union[Exception, None]]:
        """place order request"""

        order_details = {
            "bot_id": bot_id,
            "is_ask": is_ask,
            "stock_id": stock_id,
            "price": price,
            "stock_quantity": stock_quantity,
            "order_type": OrderType.Name(order_type),
        }

        logging.info(f"Trying to place order with {order_details=}")

        try:
            placeOrderRequest = PlaceOrderRequest(
                stock_id=stock_id,
                is_ask=is_ask,
                price=price,
                stock_quantity=stock_quantity,
                order_type=order_type,
            )

            resp: PlaceOrderResponse = await self.action_stub.PlaceOrder(
                placeOrderRequest,
                metadata=self.metadata.get_bot_meta_data_with_given_user_id(bot_id),
            )

            if resp.status_code > 0:
                # Some error occurred, sending resp and status_message as response
                logging.info(
                    f"place order with {order_details=}"
                    f"failed due to={resp.status_message}"
                )
                return resp, resp.status_message

            logging.info(f"Successfully placed order with {order_details=}")
            return resp, None
        except TypeError as e:
            # We get type error when data validation for request fails
            logging.error(f"Type check failed {e}")
            return None, e
        except Exception as e:
            logging.error(
                f"Unable to place order with {order_details=} due to {e}",
                exc_info=True,
            )
            return None, e

    async def get_my_open_orders(
        self, bot_id: int
    ) -> Tuple[Union[GetMyOpenOrdersResponse, None], Union[Exception, None]]:
        """Get my open orders request"""

        order_details = {
            "bot_id": bot_id,
        }

        logging.info(f"Trying to my orders with {order_details=}")

        try:
            getMyOpenOrdersRequest = GetMyOpenOrdersRequest()

            resp: GetMyOpenOrdersResponse = await self.action_stub.GetMyOpenOrders(
                getMyOpenOrdersRequest,
                metadata=self.metadata.get_bot_meta_data_with_given_user_id(bot_id),
            )

            if resp.status_code > 0:
                # Some error occurred, sending resp and status_message as response
                logging.info(
                    f"my open orders with {order_details=} failed due to={resp.status_message}"
                )
                return resp, resp.status_message
            logging.info(f"Successfully got my open orders with {order_details=}")
            return resp, None

        except TypeError as e:
            # We get type error when data validation for request fails
            logging.error(f"Type check failed {e}")
            return None, e
        except Exception as e:
            logging.error(
                f"Unable to my open orders  with  {order_details=} due to {e}",
                exc_info=True,
            )
            return None, e

    async def get_my_closed_bids(
        self, bot_id: int, count: int, last_order_id: int
    ) -> Tuple[Union[GetMyClosedBidsResponse, None], Union[Exception, None]]:
        """Get my closed bids request"""

        order_details = {
            "bot_id": bot_id,
            "count": count,
            "last_order_id": last_order_id,
        }

        logging.info(f"Trying to my closed bid orders with {order_details=}")

        try:
            getMyClosedBidsRequest = GetMyClosedBidsRequest(
                last_order_id=last_order_id, count=count
            )

            resp: GetMyClosedBidsResponse = await self.action_stub.GetMyClosedBids(
                getMyClosedBidsRequest,
                metadata=self.metadata.get_bot_meta_data_with_given_user_id(bot_id),
            )

            if resp.status_code > 0:
                # Some error occurred, sending resp and status_message as response
                logging.info(
                    f"my closed bid orders with {order_details=} failed due to={resp.status_message}"
                )
                return resp, resp.status_message

            logging.info(f"Successfully got my closed bid orders with {order_details=}")
            return resp, None

        except TypeError as e:
            # We get type error when data validation for request fails
            logging.error(f"Type check failed {e}")
            return None, e

        except Exception as e:
            logging.error(
                f"Unable to my closed bid orders with  {order_details=} due to {e}",
                exc_info=True,
            )
            return None, e

    async def get_my_closed_asks(
        self, bot_id: int, count: int, last_order_id: int
    ) -> Tuple[Union[GetMyClosedAsksResponse, None], Union[Exception, None]]:
        """Get my closed asks request"""

        order_details = {
            "bot_id": bot_id,
            "count": count,
            "last_order_id": last_order_id,
        }

        logging.info(f"Trying to my closed ask orders with {order_details=}")

        try:
            getMyClosedAsksRequest = GetMyClosedAsksRequest(
                last_order_id=last_order_id, count=count
            )

            resp: GetMyClosedAsksResponse = await self.action_stub.GetMyClosedAsks(
                getMyClosedAsksRequest,
                metadata=self.metadata.get_bot_meta_data_with_given_user_id(bot_id),
            )

            if resp.status_code > 0:
                # Some error occurred, sending resp and status_message as response
                logging.info(
                    f"my closed ask orders with {order_details=} failed due to={resp.status_message}"
                )
                return resp, resp.status_message
            logging.info(f"Successfully got my closed ask orders with {order_details=}")
            return resp, None

        except TypeError as e:
            # We get type error when data validation for request fails
            logging.error(f"Type check failed {e}")
            return None, e

        except Exception as e:
            logging.error(
                f"Unable to my closed ask orders with  {order_details=} due to {e}",
                exc_info=True,
            )
            return None, e
