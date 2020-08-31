from decouple import config
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest, OrdersGetRequest
from paypalhttp import HttpError


class PayPal:
    def __init__(self):
        self.secret_id = config('paypal_secret_id')
        self.client_id = config('paypal_client_id')
        self.sandbox_secret_id = config('sandbox_paypal_secret_id')
        self.sandbox_client_id = config('sandbox_paypal_client_id')

    def sandbox(self):
        environment = SandboxEnvironment(client_id=self.sandbox_client_id, client_secret=self.sandbox_secret_id)
        client = PayPalHttpClient(environment)
        return client

    def create_order(self, product_list, grand_total, subtotal, shipping_cost, shipping_discount, tax, shipping_name, shipping_method, address_line_1,
                     address_line_2, city, state, zip_code, country="US", handling_cost=0, currency="USD"):

        order_id = None
        request = OrdersCreateRequest()

        request.prefer('return=representation')

        request.request_body(
            {
                "intent": "CAPTURE",
                "application_context": {
                    "return_url": "https://www.tcgfirst.com/orders/complete-order",
                    "cancel_url": "https://www.tcgfirst.com/cart/",
                },

                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": currency,
                            "value": grand_total,
                            "breakdown": {
                                "item_total": {
                                    "currency_code": currency,
                                    "value": subtotal,
                                },
                                "shipping": {
                                    "currency_code": currency,
                                    "value": shipping_cost,
                                },
                                "handling": {
                                    "currency_code": currency,
                                    "value": handling_cost,
                                },
                                "tax_total": {
                                    "currency_code": currency,
                                    "value": tax,
                                },
                                "shipping_discount": {
                                    "currency_code": currency,
                                    "value": shipping_discount,
                                }
                            },
                        },

                        "shipping": {
                            "method": shipping_method,
                            "name": {
                                "full_name": shipping_name,
                            },
                            "address": {
                                "address_line_1": address_line_1,
                                "address_line_2": address_line_2,
                                "admin_area_2": city,
                                "admin_area_1": state,
                                "postal_code": zip_code,
                                "country_code": country,
                            }
                        },

                        "items": product_list,
                    }
                ],
            }
        )

        try:
            # Call API with your client and get a response for your call
            response = self.sandbox().execute(request)

            # print('Status Code:', response.status_code)

            # print('Status:', response.result.status)

            # print('Order ID:', response.result.id)
            order_id = response.result.id

            # print('Intent:', response.result.intent)

            print('Links:')

            for link in response.result.links:
                # print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
                # print('Total Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code, response.result.purchase_units[0].amount.value))

                # If call returns body in response, you can get the deserialized version from the result attribute of the response
                # order = response.result
                pass
        except IOError as ioe:
            print(ioe)
            if isinstance(ioe, HttpError):
                # Something went wrong server-side
                print(ioe.status_code)

        return order_id

    def capture_order(self, order_id):
        # Here, OrdersCaptureRequest() creates a POST request to /v2/checkout/orders
        # Replace APPROVED-ORDER-ID with the actual approved order id.
        request = OrdersCaptureRequest(order_id)
        try:
            # Call API with your client and get a response for your call
            response = self.sandbox().execute(request)

            # If call returns body in response, you can get the deserialized version from the result attribute of the response
            order = response.result
            print(order.id)
            print(order.status)

            print("Processed")
        except IOError as ioe:
            if isinstance(ioe, HttpError):
                # Something went wrong server-side
                print(ioe.status_code)

                print(ioe.headers)

                print(ioe)

            else:
                # Something went wrong client side
                print(ioe)

    def get_order(self, order_id):
        request = OrdersGetRequest(order_id=order_id)
        response = self.sandbox().execute(request)
        status = response.result.status

        return status


