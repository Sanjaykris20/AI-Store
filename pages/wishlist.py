import reflex as rx
from components.navbar import navbar
from components.product_card import product_card
from state.wishlist_state import WishlistState

@rx.page(route="/wishlist", title="My Wishlist")
def wishlist() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("My Wishlist", size="8", margin_top="3rem", color="white"),
                rx.text(
                    WishlistState.wishlist_count.to_string() + " item(s) saved",
                    color="slate.300",
                    margin_top="0.5rem",
                    margin_bottom="2rem"
                ),
                rx.cond(
                    WishlistState.wishlist_count > 0,
                    rx.grid(
                        rx.foreach(
                            WishlistState.wishlist_items,
                            lambda p: product_card(p)
                        ),
                        columns="4",
                        spacing="4",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.icon("heart", size=48, color="slate.500"),
                        rx.text("Your wishlist is empty.", color="slate.400", size="4"),
                        rx.link(
                            rx.button("Browse Products", color_scheme="blue", variant="surface"),
                            href="/"
                        ),
                        align="center",
                        spacing="4",
                        padding_top="4rem",
                        width="100%"
                    )
                ),
                width="100%",
                align_items="start"
            ),
            size="4"
        )
    )
