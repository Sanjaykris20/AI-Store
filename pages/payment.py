import reflex as rx
from components.navbar import navbar
from state.cart_state import CartState
from state.user_state import UserState

@rx.page(route="/payment", title="Checkout")
def payment() -> rx.Component:
    """Clean checkout page — shows price summary, redirects to Razorpay."""
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Order Summary", size="8", margin_top="2rem", margin_bottom="1rem", color="white"),
                rx.grid(
                    # Left Column: Shipping & Security Info
                    rx.vstack(
                        rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon(tag="shield-check", size=24, color="blue.400"),
                                    rx.heading("Secure Checkout", size="4", color="white"),
                                    spacing="2",
                                ),
                                rx.divider(opacity="0.1"),
                                rx.text("Your payment is 100% secure and encrypted.", size="2", color="slate.400"),
                                rx.text("Powered by Razorpay Payment Gateway.", size="2", color="slate.400"),
                                rx.badge("Test Mode Active", color_scheme="orange"),
                                width="100%",
                                align_items="start",
                                spacing="4",
                            ),
                            padding="1.5rem",
                            width="100%",
                            background_color="rgba(15, 23, 42, 0.4)",
                            backdrop_filter="blur(15px)",
                            border="1px solid rgba(255, 255, 255, 0.1)",
                            border_radius="xl",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.heading("Shipping Information", size="4", color="white"),
                                rx.divider(opacity="0.1"),
                                rx.text(UserState.customer_display_name, weight="bold", color="white"),
                                rx.text("Standard Delivery (3-5 business days)", size="2", color="slate.300"),
                                rx.text("Free Shipping on this order", size="2", color="green.400"),
                                width="100%",
                                align_items="start",
                                spacing="4",
                            ),
                            padding="1.5rem",
                            width="100%",
                            background_color="rgba(15, 23, 42, 0.4)",
                            backdrop_filter="blur(15px)",
                            border="1px solid rgba(255, 255, 255, 0.1)",
                            border_radius="xl",
                            margin_top="1rem",
                        ),
                        width="100%",
                    ),
                    # Right Column: Price Breakdown + Pay Button
                    rx.card(
                        rx.vstack(
                            rx.heading("Price Summary", size="4", margin_bottom="1rem", color="white"),
                            rx.hstack(
                                rx.text("Subtotal", color="slate.400"),
                                rx.spacer(),
                                rx.text("₹", CartState.total_price, color="white"),
                                width="100%",
                            ),
                            rx.hstack(
                                rx.text("Tax (GST 18%)", color="slate.400"),
                                rx.spacer(),
                                rx.text("₹", CartState.tax_amount, color="white"),
                                width="100%",
                            ),
                            rx.hstack(
                                rx.text("Delivery Charges", color="slate.400"),
                                rx.spacer(),
                                rx.text("FREE", color="green.400", weight="bold"),
                                width="100%",
                            ),
                            rx.divider(margin_y="1rem", opacity="0.1"),
                            rx.hstack(
                                rx.text("Total Payable", size="5", weight="bold", color="white"),
                                rx.spacer(),
                                rx.text(
                                    "₹",
                                    CartState.total_payable,
                                    size="5",
                                    weight="bold",
                                    color="blue.400",
                                ),
                                width="100%",
                            ),
                            # Hint to the user to enter the amount on Razorpay
                            rx.callout(
                                rx.hstack(
                                    rx.icon(tag="info", size=16),
                                    rx.text(
                                        "On the Razorpay page, enter the amount shown above to complete your payment.",
                                        size="2",
                                    ),
                                    spacing="2",
                                    align="center",
                                ),
                                color_scheme="blue",
                                variant="surface",
                                margin_top="1rem",
                                width="100%",
                            ),
                            rx.link(
                                rx.button(
                                    rx.icon(tag="credit-card", size=18),
                                    "Pay Now with Razorpay",
                                    color_scheme="blue",
                                    size="4",
                                    width="100%",
                                    margin_top="1rem",
                                ),
                                href=CartState.direct_payment_url,
                                is_external=True,
                                width="100%",
                            ),
                            rx.text(
                                "You will be redirected to Razorpay's secure payment page in a new tab.",
                                size="1",
                                color="slate.500",
                                text_align="center",
                                margin_top="0.5rem",
                                width="100%",
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        padding="2rem",
                        width="100%",
                        background_color="rgba(15, 23, 42, 0.4)",
                        backdrop_filter="blur(15px)",
                        border="1px solid rgba(255, 255, 255, 0.1)",
                        border_radius="xl",
                    ),
                    columns="2",
                    spacing="6",
                    width="100%",
                    margin_top="1rem",
                ),
                width="100%",
                align_items="center",
                padding_bottom="5rem"
            ),
            size="3",
        ),
        background_color="transparent",
        min_height="100vh",
    )
