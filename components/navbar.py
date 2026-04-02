import reflex as rx
from state.user_state import UserState
from state.cart_state import CartState
from state.products_state import ProductsState
from components.chatbot import chatbot

def navbar() -> rx.Component:
    """A responsive navigation bar for the e-commerce app."""
    return rx.box(
        rx.hstack(
            # Logo Section
            rx.link(
                rx.hstack(
                    rx.icon(tag="atom", size=24, color="white"),
                    rx.heading("AI Store", size="6", color="white"),
                    spacing="2",
                    align_items="center"
                ),
                href="/",
                underline="none",
                _hover={"opacity": 0.8}
            ),
            
            rx.spacer(),
            
            # Centered Search Bar
            rx.box(
                rx.form(
                    rx.hstack(
                        rx.input(
                            placeholder="Search products...",
                            name="q",
                            width="350px",
                            border_radius="lg",
                            background_color="white",
                            color="black",
                            border="none",
                        ),
                        rx.button(
                            rx.icon(tag="search", color="gray"),
                            type="submit",
                            variant="ghost",
                            _hover={"background": "transparent"}
                        ),
                        spacing="0",
                        background_color="white",
                        border_radius="lg",
                        padding_right="0.5rem",
                    ),
                    on_submit=ProductsState.handle_search_submit,
                ),
                display="flex",
                justify_content="center",
                flex="1"
            ),
            
            rx.spacer(),
            
            # Right Action Items
            rx.hstack(
                rx.link(
                    rx.hstack(rx.icon(tag="heart", size=18), rx.text("Wishlist", size="2")),
                    href="/wishlist",
                    color="white",
                    _hover={"color": "blue.400"},
                    transition="all 0.2s"
                ),
                rx.link(
                    rx.hstack(rx.icon(tag="shopping-bag", size=18), rx.text("Orders", size="2")),
                    href="/orders",
                    color="white",
                    _hover={"color": "blue.400"},
                    transition="all 0.2s"
                ),
                
                # Profile Dropdown
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="user", size=18),
                                rx.text("Profile", size="2"),
                                rx.icon(tag="chevron-down", size=14),
                                spacing="2"
                            ),
                            variant="ghost",
                            color="white",
                            _hover={"background": "rgba(255, 255, 255, 0.1)"}
                        ),
                    ),
                    rx.menu.content(
                        rx.menu.item("My Profile", on_click=rx.redirect("/profile")),
                        rx.menu.separator(),
                        rx.menu.item("Log Out", on_click=UserState.logout, color="red"),
                        background_color="#0f172a",
                        color="white",
                        border="1px solid rgba(255,255,255,0.1)"
                    ),
                ),
                
                # Cart
                rx.link(
                    rx.box(
                        rx.icon(tag="shopping-cart", size=22),
                        rx.cond(
                            CartState.cart_items.length() > 0,
                            rx.badge(
                                CartState.cart_items.length(), 
                                color_scheme="red", 
                                variant="solid", 
                                radius="full",
                                position="absolute",
                                top="-0.5rem",
                                right="-0.5rem"
                            ),
                            rx.fragment()
                        ),
                        position="relative",
                        color="white",
                        _hover={"color": "blue.400"},
                    ),
                    href="/cart"
                ),
                spacing="5",
                align_items="center"
            ),
            
            width="100%",
            padding="0.75rem 2rem",
            border_bottom="1px solid rgba(255, 255, 255, 0.05)",
            justify_content="space-between",
            align_items="center",
            position="sticky",
            top="0",
            background_color="rgba(2, 6, 23, 0.8)",
            backdrop_filter="blur(12px)",
            z_index="1000",
            box_shadow="0 4px 20px rgba(0,0,0,0.4)"
        ),
        chatbot()
    )
