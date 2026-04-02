import reflex as rx
from state.user_state import UserState
from components.navbar import navbar

@rx.page(route="/profile", title="User Profile")
def profile() -> rx.Component:
    """
    Displays user info and mock order history.
    """
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("User Profile", size="8", margin_top="3rem", margin_bottom="2rem", color="white"),
                
                rx.cond(
                    UserState.logged_in,
                    rx.card(
                        rx.vstack(
                            rx.avatar(fallback="U", size="5", margin_bottom="1rem"),
                            
                            rx.hstack(
                                rx.text("Internal User ID:", font_weight="bold", color="slate.300"),
                                rx.text(UserState.user_id.to_string(), color="white"),
                            ),
                            
                            rx.hstack(
                                rx.text("Firebase UID:", font_weight="bold", color="slate.300"),
                                rx.text(UserState.firebase_uid, color="white", size="1"),
                            ),
                            
                            rx.hstack(
                                rx.text("Status:", font_weight="bold", color="slate.300"),
                                rx.badge(
                                    rx.cond(UserState.is_new_user, "New User", "Returning User"), 
                                    color_scheme=rx.cond(UserState.is_new_user, "green", "blue")
                                )
                            ),
                            
                            rx.divider(margin_top="1rem", margin_bottom="1rem", opacity="0.1"),
                            
                            rx.button("Log Out", on_click=UserState.logout, color_scheme="red", width="100%", variant="soft"),
                            
                            align_items="start",
                            width="100%",
                            spacing="4"
                        ),
                        width="100%",
                        max_width="450px",
                        padding="2.5rem",
                        background_color="rgba(15, 23, 42, 0.4)",
                        backdrop_filter="blur(15px)",
                        border="1px solid rgba(255, 255, 255, 0.1)",
                        border_radius="2xl",
                        shadow="2xl"
                    ),
                    
                    rx.box(
                        rx.vstack(
                            rx.icon(tag="user-x", size=48, color="slate.500"),
                            rx.text("You are not logged in.", color="slate.400", size="4"),
                            rx.link(rx.button("Go to Login", size="3"), href="/login"),
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
                    )
                ),
                
                padding_top="2rem",
                align_items="center",
                width="100%",
                padding_bottom="5rem"
            ),
            size="3",
            margin="auto"
        )
    )
