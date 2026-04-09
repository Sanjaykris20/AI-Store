"""Main Application Entry Point."""

import reflex as rx

# Application State Imports
from state.user_state import UserState
from state.cart_state import CartState
from state.recommendation_state import RecommendationState
from state.wishlist_state import WishlistState

# Import all pages to ensure their routes are registered via their decorators
import pages.home
import pages.login
import pages.signup
import pages.product_detail
import pages.cart
import pages.checkout
import pages.payment
import pages.profile
import pages.wishlist
import pages.orders
import pages.products
import pages.top_deals

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
            "background": "#080c19",
            "color": "white",
            "min_height": "100vh",
            "font_family": "'Inter', system-ui, sans-serif",
            "margin": "0",
            "padding": "0",
        },
        "*": {
            "box_sizing": "border-box",
        },
    },
    head_components=[
        rx.script(src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"),
        rx.script(src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"),
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"),
    ]
)
