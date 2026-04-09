import reflex as rx
from state.user_state import UserState
from components.footer import footer
from components.bg import page_background


@rx.page(route="/signup", title="AI Store - Sign Up")
def signup() -> rx.Component:
    """Sign up page matching the login page and store aesthetic."""
    return rx.box(
        page_background(),

        # ── Navbar-style header (consistent with login) ────────────────
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.box(
                        rx.icon(tag="atom", size=26, color="#60a5fa"),
                        background="linear-gradient(135deg, #3b82f6, #1d4ed8)",
                        padding="0.45rem",
                        border_radius="50%",
                        box_shadow="0 0 18px rgba(59,130,246,0.35)",
                    ),
                    rx.heading("AI Store", size="5", color="white", weight="bold"),
                    spacing="2",
                    align_items="center",
                ),
                href="/login",
                underline="none",
            ),
            rx.spacer(),
            # decorative icons to match login page
            rx.hstack(
                rx.icon(tag="user", size=22, color="rgba(255,255,255,0.7)"),
                rx.icon(tag="shopping-cart", size=22, color="rgba(255,255,255,0.7)"),
                spacing="4",
            ),
            width="100%",
            padding="0.85rem 2rem",
            background="linear-gradient(135deg, rgba(8,12,25,0.97), rgba(13,27,42,0.97))",
            backdrop_filter="blur(20px)",
            border_bottom="1px solid rgba(59,130,246,0.2)",
            position="fixed",
            top="0",
            left="0",
            z_index="100",
            box_shadow="0 4px 30px rgba(0,0,0,0.4)",
        ),

        # ── Main body ──────────────────────────────────────────────────
        rx.box(
            rx.hstack(
                # Left panel — features
                rx.box(
                    rx.vstack(
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="user-plus", size=20, color="#60a5fa"),
                                rx.text("Start Your ML Journey", size="4", color="white", font_weight="500"),
                                spacing="3",
                                align_items="center",
                            ),
                            rx.hstack(
                                rx.icon(tag="trending-up", size=20, color="#60a5fa"),
                                rx.text("Personalized Daily Picks", size="4", color="white", font_weight="500"),
                                spacing="3",
                                align_items="center",
                            ),
                            rx.hstack(
                                rx.icon(tag="gift", size=20, color="#60a5fa"),
                                rx.text("Exclusive Early Access", size="4", color="white", font_weight="500"),
                                spacing="3",
                                align_items="center",
                            ),
                            spacing="5",
                            align_items="start",
                        ),
                        justify_content="center",
                        align_items="start",
                        height="100%",
                        spacing="6",
                    ),
                    padding="2rem 2.5rem",
                    background="linear-gradient(135deg, rgba(10,15,30,0.65), rgba(15,23,42,0.45))",
                    border="1px solid rgba(59,130,246,0.3)",
                    border_radius="2xl",
                    backdrop_filter="blur(20px)",
                    box_shadow="0 12px 40px rgba(0,0,0,0.3)",
                    min_width="280px",
                ),

                rx.spacer(),

                # Right panel — Signup card
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Create Account",
                            size="7",
                            text_align="center",
                            color="#60a5fa",
                            font_weight="bold",
                            margin_bottom="0.25rem",
                        ),
                        rx.text(
                            "Join the future of personalized AI shopping today.",
                            size="3",
                            text_align="center",
                            color="rgba(255,255,255,0.7)",
                            margin_bottom="1.5rem",
                            max_width="260px",
                        ),

                        rx.input(
                            placeholder="Full Name",
                            width="100%",
                            padding="1.1rem 1.2rem",
                            height="auto",
                            line_height="1.5",
                            background="rgba(255,255,255,0.06)",
                            color="white",
                            _placeholder={"color": "white", "opacity": "0.8"},
                            border="1px solid rgba(59,130,246,0.35)",
                            border_radius="lg",
                            _focus={
                                "border": "1px solid #3b82f6",
                                "box_shadow": "0 0 16px rgba(59,130,246,0.3)",
                                "background": "rgba(255,255,255,0.1)",
                            },
                        ),
                        rx.input(
                            placeholder="Email Address",
                            width="100%",
                            padding="1.1rem 1.2rem",
                            height="auto",
                            line_height="1.5",
                            background="rgba(255,255,255,0.06)",
                            color="white",
                            _placeholder={"color": "white", "opacity": "0.8"},
                            border="1px solid rgba(59,130,246,0.35)",
                            border_radius="lg",
                            on_change=UserState.set_email,
                            _focus={
                                "border": "1px solid #3b82f6",
                                "box_shadow": "0 0 16px rgba(59,130,246,0.3)",
                                "background": "rgba(255,255,255,0.1)",
                            },
                        ),
                        rx.input(
                            placeholder="Password",
                            type="password",
                            width="100%",
                            padding="1.1rem 1.2rem",
                            height="auto",
                            line_height="1.5",
                            background="rgba(255,255,255,0.06)",
                            color="white",
                            _placeholder={"color": "white", "opacity": "0.8"},
                            border="1px solid rgba(59,130,246,0.35)",
                            border_radius="lg",
                            on_change=UserState.set_password,
                            _focus={
                                "border": "1px solid #3b82f6",
                                "box_shadow": "0 0 16px rgba(59,130,246,0.3)",
                                "background": "rgba(255,255,255,0.1)",
                            },
                        ),

                        rx.cond(
                            UserState.auth_error != "",
                            rx.callout(
                                UserState.auth_error,
                                icon="triangle_alert",
                                color_scheme="red",
                                background="rgba(239,68,68,0.08)",
                                border="1px solid rgba(239,68,68,0.3)",
                            ),
                        ),

                        # Create Account button
                        rx.button(
                            "Create Account",
                            on_click=UserState.signup_with_firebase,
                            width="100%",
                            background="linear-gradient(135deg, #10b981, #059669)",
                            color="white",
                            size="3",
                            border_radius="lg",
                            font_weight="600",
                            _hover={
                                "background": "linear-gradient(135deg, #059669, #047857)",
                                "box_shadow": "0 0 22px rgba(16,185,129,0.5)",
                                "transform": "translateY(-1px)",
                            },
                            box_shadow="0 4px 18px rgba(16,185,129,0.3)",
                            transition="all 0.25s ease",
                        ),

                        # Google sign up
                        rx.button(
                            rx.hstack(
                                rx.box(
                                    rx.text("G", font_weight="bold", color="white", font_size="1rem"),
                                    background="linear-gradient(135deg, #4285f4, #34a853)",
                                    border_radius="full",
                                    width="1.6rem",
                                    height="1.6rem",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                ),
                                rx.text("Sign Up with Google"),
                                spacing="2",
                                align_items="center",
                                justify_content="center",
                                width="100%",
                            ),
                            on_click=UserState.trigger_google_login,
                            width="100%",
                            background="linear-gradient(135deg, rgba(66,133,244,0.2), rgba(52,168,83,0.15))",
                            color="white",
                            border="1px solid rgba(66,133,244,0.4)",
                            size="3",
                            border_radius="lg",
                            font_weight="500",
                            _hover={
                                "background": "linear-gradient(135deg, rgba(66,133,244,0.3), rgba(52,168,83,0.2))",
                                "box_shadow": "0 0 18px rgba(66,133,244,0.3)",
                            },
                            transition="all 0.25s ease",
                        ),
                        rx.text("(Demo)", color="rgba(255,255,255,0.4)", font_size="0.75rem", text_align="center"),

                        rx.cond(
                            UserState.logged_in,
                            rx.callout(
                                "Account Created Successfully! Redirecting...",
                                icon="circle_check",
                                color_scheme="green",
                                width="100%",
                                background="rgba(16,185,129,0.08)",
                                border="1px solid rgba(16,185,129,0.3)",
                            ),
                            rx.hstack(
                                rx.text("Already have an account?", color="rgba(255,255,255,0.5)", size="2"),
                                rx.link("Log In", href="/login", color="#60a5fa", size="2", weight="bold"),
                                spacing="1",
                                justify_content="center",
                            ),
                        ),

                        align_items="center",
                        spacing="3",
                        width="100%",
                    ),
                    padding="2.5rem",
                    width="340px",
                    background="linear-gradient(135deg, rgba(10,15,30,0.88), rgba(15,23,42,0.80))",
                    border="1px solid rgba(59,130,246,0.35)",
                    border_radius="2xl",
                    backdrop_filter="blur(24px)",
                    box_shadow="0 20px 50px rgba(0,0,0,0.5), 0 0 40px rgba(59,130,246,0.1)",
                ),

                width="100%",
                align_items="center",
                justify_content="center",
                spacing="8",
                padding_x="4rem",
            ),
            flex="1",
            display="flex",
            align_items="center",
            justify_content="center",
            padding_top="5rem",
            padding_bottom="4rem",
        ),

        footer(),

        display="flex",
        flex_direction="column",
        min_height="100vh",
        position="relative",
    )
