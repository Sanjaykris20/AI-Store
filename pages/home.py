import reflex as rx
from state.user_state import UserState
from state.recommendation_state import RecommendationState
from state.products_state import ProductsState
from components.navbar import navbar
from components.product_card import product_card

@rx.page(route="/", title="Home - AI Store", on_load=[UserState.check_login_status, RecommendationState.fetch_general_recommendations, ProductsState.fetch_products])
def home() -> rx.Component:
    """The landing page. Shows different headings based on user type, or search results."""
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Welcome to Your AI-Powered Store!", size="9", margin_top="5rem", margin_bottom="1rem", text_align="center", color="white", weight="bold"),
                rx.text("Discover products perfectly tailored for you using Machine Learning.", size="4", color="gray.300", margin_bottom="4rem", text_align="center"),
                
                rx.cond(
                    ProductsState.search_query != "",
                    # If user searched for something
                    rx.box(
                        rx.heading(f"Search Results for '{ProductsState.search_query}'", size="6", margin_bottom="2rem"),
                        rx.grid(
                            rx.foreach(ProductsState.all_products, lambda p: product_card(p)),
                            columns="4",
                            spacing="4",
                            width="100%"
                        ),
                        width="100%"
                    ),
                    # Display recommendations if no search
                    rx.vstack(
                        rx.cond(
                            (~UserState.logged_in) | UserState.is_new_user,
                            # If new user or not logged in -> rating based heading
                            rx.heading("Top Rated Items", size="6", margin_bottom="2rem"),
                            # If existing logged in user -> recommender
                            rx.heading("Your Recommended Products", size="6", margin_bottom="2rem") 
                        ),
                        
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
                        
                        rx.button(
                            "Load My Recommendations", 
                            on_click=RecommendationState.fetch_general_recommendations, 
                            size="3", 
                            background_color="#2563eb",
                            color="white",
                            _hover={"background_color": "#1d4ed8", "box_shadow": "0 0 15px rgba(37, 99, 235, 0.4)"},
                            margin_top="3rem",
                            padding_x="2rem",
                        ),
                        
                        width="100%",
                        align_items="center"
                    )
                ),
                
                padding_bottom="6rem",
                width="100%",
                align_items="center"
            ),
            size="4"
        ),
        # Decorative abstract background pattern (can be refined with an image/svg)
        background="""url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231e293b' fill-opacity='0.2'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")""",
    )
