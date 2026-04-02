import reflex as rx
from components.navbar import navbar
from state.cart_state import CartState
from state.recommendation_state import RecommendationState
from components.product_card import product_card
from config import DATA_PATH
import pandas as pd
import os

class ProductDetailState(rx.State):
    """Local state for product details. Typically queries ID from URL Params."""
    current_product: dict = {
        "ProdID": 999, 
        "Brand": "Loading...", 
        "Category": "...", 
        "Price": "0.00", 
        "ImageURL": "/placeholder.jpg", 
        "Description": "Please wait while we fetch product details."
    }

    def load_product(self):
        try:
            if not self.pid:
                return
            target_id = int(self.pid)
            if os.path.exists(DATA_PATH):
                df = pd.read_csv(DATA_PATH)
                match = df[df['ProdID'] == target_id]
                if not match.empty:
                    item = match.iloc[0].fillna('').to_dict()
                    if "ImageURL" in item and item["ImageURL"]:
                        item["ImageURL"] = str(item["ImageURL"]).split(" | ")[0]
                    else:
                        item["ImageURL"] = "/placeholder.jpg"
                    
                    item["Price"] = f"{(int(item['ProdID']) % 2500) + 499}.00"
                    
                    if "Rating" in item and item["Rating"] != "":
                        try:
                            item["Rating"] = f"{float(item['Rating']):.1f}"
                        except:
                            item["Rating"] = "N/A"
                            
                    if not item.get("Description"):
                        item["Description"] = "No detailed description available for this product."
                    self.current_product = item
                    return
        except Exception as e:
            print(f"Error loading product detail: {e}")
            
        self.current_product = {
            "ProdID": 999, 
            "Brand": "Product Not Found", 
            "Category": "N/A", 
            "Price": "0.00", 
            "ImageURL": "/placeholder.jpg", 
            "Description": "Could not locate this product in the dataset."
        }

    def load_product_with_recommendations(self):
        """Loads product details then auto-fetches recommendations for this product."""
        self.load_product()
        product_id = self.current_product.get("ProdID")
        if product_id and product_id != 999:
            yield RecommendationState.fetch_recommendations(int(product_id))

@rx.page(route="/product/[pid]", title="Product Detail", on_load=ProductDetailState.load_product_with_recommendations)
def product_detail() -> rx.Component:
    """Dynamic routing page for individual product inspection."""
    return rx.box(
        navbar(),
        rx.container(
            rx.hstack(
                rx.image(
                    src=ProductDetailState.current_product["ImageURL"], 
                    height="400px", 
                    width="400px", 
                    object_fit="contain", 
                    border_radius="2xl",
                    background_color="rgba(255, 255, 255, 0.05)",
                    border="1px solid rgba(255, 255, 255, 0.1)",
                    shadow="2xl",
                    fallback="https://via.placeholder.com/400"
                ),
                
                rx.vstack(
                    rx.heading(
                        rx.cond(
                            ProductDetailState.current_product.contains("Product_Display_Name"),
                            ProductDetailState.current_product["Product_Display_Name"],
                            ProductDetailState.current_product["Brand"]
                        ), 
                        size="9",
                        color="white",
                        weight="bold"
                    ),
                    rx.text("Price: ", "$", ProductDetailState.current_product["Price"], size="8", font_weight="bold", color="blue.400", margin_bottom="1.5rem"),
                    
                    rx.box(
                        rx.vstack(
                            rx.heading("Product Overview", size="4", margin_bottom="0.5rem", color="blue.300"),
                            rx.divider(margin_bottom="1rem", opacity="0.1"),
                            rx.text(ProductDetailState.current_product["Description"], color="slate.300", size="4", line_height="1.6"),
                            align_items="start",
                        ),
                        padding="2rem",
                        background_color="rgba(15, 23, 42, 0.4)",
                        backdrop_filter="blur(15px)",
                        border="1px solid rgba(255, 255, 255, 0.1)",
                        border_radius="xl",
                        margin_bottom="2rem",
                        width="100%"
                    ),
                    
                    rx.hstack(
                        rx.button(
                            rx.icon(tag="shopping-cart"),
                            " Add to Cart", 
                            size="4", 
                            color_scheme="blue",
                            on_click=lambda: CartState.add_to_cart(ProductDetailState.current_product),
                            padding_x="2rem"
                        ),
                        rx.link(rx.button("Buy Now", size="4", variant="outline", color_scheme="gray", padding_x="2rem"), href="/checkout"),
                        spacing="4"
                    ),
                    
                    align_items="start",
                    width="100%",
                    padding_left="3rem"
                ),
                width="100%",
                margin_top="4rem",
                align_items="center"
            ),
            
            rx.divider(margin_top="5rem", margin_bottom="3rem", opacity="0.1"),
            
            rx.vstack(
                rx.heading("You May Also Like", size="7", margin_bottom="2rem", color="white", weight="bold"),
                rx.cond(
                    RecommendationState.is_loading,
                    rx.spinner(size="3"),
                    rx.grid(
                        rx.foreach(RecommendationState.recommendations, lambda p: product_card(p)),
                        columns="4",
                        spacing="5",
                        width="100%"
                    )
                ),
                align_items="center",
                width="100%",
                padding_bottom="6rem"
            ),
            
            size="4"
        )
    )
