import reflex as rx
from components.navbar import navbar

@rx.page(route="/orders", title="Order History")
def orders() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Order History", size="8", margin_top="3rem", color="white"),
                rx.box(
                    rx.vstack(
                        rx.icon(tag="package-open", size=60, color="slate.500"),
                        rx.text("No orders found yet.", color="slate.400", size="4"),
                        rx.link(rx.button("Explore Store", size="3", variant="surface"), href="/"),
                        spacing="4",
                        align_items="center"
                    ),
                    width="100%",
                    padding="5rem",
                    background_color="rgba(15, 23, 42, 0.4)",
                    backdrop_filter="blur(15px)",
                    border="1px solid rgba(255, 255, 255, 0.1)",
                    border_radius="2xl",
                    display="flex",
                    justify_content="center",
                    margin_top="2rem",
                ),
                width="100%",
                align_items="center"
            ),
            size="3"
        )
    )
