import reflex as rx

# Import Application States to ensure they register
from state.user_state import UserState
from state.cart_state import CartState
from state.recommendation_state import RecommendationState
from state.payment_state import PaymentState
from state.products_state import ProductsState
from state.wishlist_state import WishlistState

# Import pages (as we build them)
import pages.profile
import pages.home
import pages.login
import pages.signup
import pages.product_detail
import pages.cart
import pages.checkout
import pages.payment
import pages.wishlist
import pages.orders

# Create main Reflex App
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
        accent_color="blue",
        gray_color="slate",
    ),
    style={
        "body": {
            "background": "radial-gradient(circle at top right, #1e293b 0%, #020617 100%)",
            "color": "white",
            "min_height": "100vh",
            "background_attachment": "fixed",
            "font_family": "Outfit, sans-serif"
        }
    },
    head_components=[
        rx.script(src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"),
        rx.script(src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"),
    ]
)
 
