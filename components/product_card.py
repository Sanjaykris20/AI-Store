import reflex as rx
from state.wishlist_state import WishlistState
from state.cart_state import CartState

def product_card(product: dict) -> rx.Component:
    """
    A reusable product card component.
    Expects a dictionary representing a product from our dataset.
    """
    # Safe fallback values for UI
    img_url = rx.cond(product.contains("ImageURL"), product["ImageURL"], "/placeholder.jpg")
    brand = rx.cond(product.contains("Brand"), product["Brand"], "Brand")
    display_name = rx.cond(product.contains("Product_Display_Name"), product["Product_Display_Name"], brand)
    
    return rx.card(
        rx.vstack(
            rx.image(
                src=img_url, 
                height="120px", 
                width="auto",
                margin="0 auto",
                object_fit="contain",
                border_radius="lg",
                fallback="https://via.placeholder.com/120"
            ),
            rx.vstack(
                rx.text(display_name, font_weight="bold", font_size="1rem", color="white", text_align="center", width="100%"),
                rx.hstack(
                    rx.text("$", product["Price"], font_weight="bold", color="white", size="2"),
                    rx.spacer(),
                    rx.hstack(
                        rx.icon(tag="star", size=12, color="yellow"),
                        rx.icon(tag="star", size=12, color="yellow"),
                        rx.icon(tag="star", size=12, color="yellow"),
                        rx.icon(tag="star", size=12, color="yellow"),
                        rx.icon(tag="star", size=12, color="yellow"),
                        spacing="1"
                    ),
                    width="100%",
                ),
                rx.button(
                    "Add to Cart",
                    on_click=CartState.add_to_cart(product),
                    width="100%",
                    variant="outline",
                    border="1px solid rgba(255,255,255,0.3)",
                    color="white",
                    _hover={
                        "background": "rgba(59, 130, 246, 0.2)",
                        "border": "1px solid #3b82f6",
                    },
                    padding_y="0.5rem"
                ),
                width="100%",
                spacing="3",
                align_items="center",
            ),
            
            align_items="center",
            spacing="4",
        ),
        padding="1rem",
        style={
            "background": "rgba(15, 23, 42, 0.4)",
            "backdrop_filter": "blur(10px)",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "border_radius": "1rem",
            "transition": "all 0.3s ease",
        },
        _hover={
            "transform": "translateY(-5px)",
            "box_shadow": "0 10px 30px rgba(59, 130, 246, 0.2)",
            "border": "1px solid rgba(59, 130, 246, 0.5)",
        },
        width="100%",
    )
