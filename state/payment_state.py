import reflex as rx
import random
import string
import os
from dotenv import load_dotenv
from .cart_state import CartState
from .user_state import UserState

load_dotenv()
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_SWFuoAyeu1IQk4")


class PaymentState(rx.State):
    """
    State managing the Razorpay payment flow.
    """
    order_id: str = ""
    payment_id: str = ""
    signature: str = ""
    status: str = "idle"  # idle, processing, success, failed
    error_message: str = ""
    
    def start_payment(self):
        """Initialize payment process and create a mock order ID."""
        if CartState.total_price <= 0:
            self.error_message = "Cart is empty."
            return
            
        self.status = "processing"
        # Mock order creation
        self.order_id = "order_" + "".join(random.choices(string.ascii_letters + string.digits, k=14))
        
        # Trigger the Razorpay modal via JavaScript
        # We pass necessary info to the frontend
        amount_in_paise = int(CartState.total_price * 100)
        
        return rx.call_script(
            f"""
            var options = {{
                "key": "{RAZORPAY_KEY_ID}",
                "amount": "{amount_in_paise}",
                "currency": "INR",
                "name": "Shopio e-Store",
                "description": "Secure Transaction",
                "image": "https://cdn.razorpay.com/logos/7K3s6v1Q7W9B5p_medium.png",
                "order_id": "{self.order_id}",
                "handler": function (response) {{
                    window.reflex.call_state_callback("{self.get_full_name()}.handle_success", {{
                        payment_id: response.razorpay_payment_id,
                        order_id: response.razorpay_order_id,
                        signature: response.razorpay_signature
                    }});
                }},
                "prefill": {{
                    "name": "Customer",
                    "email": "{UserState.email}",
                    "contact": "9999999999"
                }},
                "notes": {{
                    "address": "Corporate Office"
                }},
                "theme": {{
                    "color": "#3399cc"
                }},
                "modal": {{
                    "ondismiss": function() {{
                        window.reflex.call_state_callback("{self.get_full_name()}.handle_dismiss", {{}});
                    }}
                }}
            }};
            var rzp1 = new Razorpay(options);
            rzp1.open();
            """
        )

    def handle_success(self, data: dict):
        """Handle successful payment callback from Razorpay."""
        self.payment_id = data.get("payment_id", "")
        self.order_id = data.get("order_id", "")
        self.signature = data.get("signature", "")
        self.status = "success"
        self.error_message = ""
        
        # Clear the cart after successful payment
        # We can return a transition or other actions
        CartState.clear_cart()
        return rx.redirect("/orders")

    def handle_dismiss(self):
        """Handle modal dismissal without payment."""
        self.status = "idle"
        self.order_id = ""

    def handle_error(self, message: str):
        """Handle payment errors."""
        self.status = "failed"
        self.error_message = message
        self.order_id = ""
