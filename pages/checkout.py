import reflex as rx
from components.navbar import navbar

@rx.page(route="/checkout", title="Checkout")
def checkout() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Secure Checkout", size="8", margin_top="3rem", margin_bottom="2rem", color="white"),
                
                rx.card(
                    rx.vstack(
                        rx.input(placeholder="Full Name", width="100%", size="3"),
                        rx.input(placeholder="Phone Number", width="100%", size="3"),
                        rx.text_area(placeholder="Delivery Address", width="100%", size="3", height="120px"),
                        
                        rx.link(
                            rx.button("Proceed to Payment", color_scheme="blue", size="3", width="100%", margin_top="1rem"),
                            href="/payment",
                            width="100%"
                        ),
                        width="100%",
                        spacing="4"
                    ),
                    padding="3rem",
                    width="100%",
                    max_width="500px",
                    background_color="rgba(15, 23, 42, 0.4)",
                    backdrop_filter="blur(15px)",
                    border="1px solid rgba(255, 255, 255, 0.1)",
                    border_radius="2xl",
                    shadow="2xl"
                ),
                
                width="100%",
                align_items="center",
                padding_bottom="5rem"
            ),
            size="3"
        )
    )
