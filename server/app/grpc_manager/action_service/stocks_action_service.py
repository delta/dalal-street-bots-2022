import logging
from .base_action_service import BaseActionService
from proto_build.actions.BuyStocksFromExchange_pb2 import BuyStocksFromExchangeRequest, BuyStocksFromExchangeResponse
from proto_build.actions.PlaceOrder_pb2 import PlaceOrderRequest, PlaceOrderResponse
from proto_build.actions.CancelOrder_pb2 import CancelOrderRequest, CancelOrderResponse

class StockActionService(BaseActionService):
    """Helper Class for all stocks related functions"""

    def buy_stock_from_exchange(self,bot_id: int, stock_id: int, stock_quantity):
        """Buys stocks of a particular stock id for a particular bot from exchange"""

    try:
        req = BuyStocksFromExchangeRequest(stock_id=stock_id, stock_quantity=stock_quantity)

        response: BuyStocksFromExchangeResponse = await self.action_stub.BuyStocksFromExchange(req, metadata=self.getMd(bot_id))

        return response
    
    except Exception as e:
        logging.error(
            f"Error {e} while trying to buy stocks from exchange"
        )

        return "Failed",400
    
    def cancel_order(self,bot_id: int, order_id: int, is_ask: bool):
        """Cancels buy/sell order of a particular bot"""
    
    try:
        req = CancelOrderRequest(order_id=order_id, is_ask=is_ask)

        response: CancelOrderResponse = await self.action_stub.CancelOrder(req, metadata=self.getMd(bot_id))

        return response
    
    except Exception as e:
        logging.error(
            f"Error {e} while trying to cancel order"
        )

        return "Failed",400

    def place_order(self,bot_id: int, stock_id: int, stock_quantity: int, price: int, order_type, is_ask: bool):
        """Buy/Sell order for a particular bot. isAsk = True for sell while isAsk = False for buy"""
        try:
            req = PlaceOrderRequest(stock_id=stock_id, stock_quantity=stock_quantity, price=price, order_type=order_type, is_ask=is_ask)

            response: PlaceOrderResponse = await self.action_stub.PlaceOrder(req, metadata=self.getMd(bot_id))
