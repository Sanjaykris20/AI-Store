import reflex as rx
import os
import pandas as pd

def _get_top_products_context(data_path="cleaned_data.csv", top_n=8) -> str:
    """Load top-rated products from CSV and format them as readable context for the AI."""
    try:
        df = pd.read_csv(data_path)
        required = ['ProdID', 'Rating', 'Category', 'Brand']
        if not all(c in df.columns for c in required):
            return ""

        # Compute price from ProdID (same logic as home page)
        def compute_price(pid):
            base = (int(pid) * 137 + 479) % 4500
            return max(199, base)

        agg = {'Rating': 'mean', "User's ID": 'count', 'Category': 'first', 'Brand': 'first'}
        if 'Product_Display_Name' in df.columns:
            agg['Product_Display_Name'] = 'first'

        stats = df.groupby('ProdID').agg(agg).rename(columns={"User's ID": 'Reviews'})
        top = stats.sort_values(by=['Rating', 'Reviews'], ascending=[False, False]).head(top_n).reset_index()

        lines = []
        for _, row in top.iterrows():
            name = str(row.get('Product_Display_Name', f"{row['Brand']} {row['Category']}"))[:55]
            price = compute_price(int(row['ProdID']))
            rating = round(float(row['Rating']), 1)
            lines.append(f"ProdID: {row['ProdID']} | Name: {name} | Brand: {row['Brand']} | Price: ₹{price:,} | Rating: {rating}⭐")

        return "Top-rated products in our dataset:\n" + "\n".join(lines)
    except Exception:
        return ""


class ChatState(rx.State):
    is_open: bool = False
    messages: list[dict[str, str]] = [
        {"role": "assistant", "content": "Hi! I'm your AI shopping assistant. Ask me about best sellers, recommendations, or any product!"}
    ]
    current_input: str = ""

    def set_current_input(self, value: str):
        """Explicit setter for current_input field."""
        self.current_input = value

    def toggle_chat(self):
        self.is_open = not self.is_open

    def send_message(self):
        if not self.current_input.strip():
            return

        user_text = self.current_input
        self.messages.append({"role": "user", "content": user_text})
        self.current_input = ""
        yield

        target_key = os.getenv("GROQ_API_KEY", "")
        if not target_key:
            self.messages.append({"role": "assistant", "content": "⚠️ Please set GROQ_API_KEY in your .env file and restart."})
            return

        try:
            import groq
            client = groq.Groq(api_key=target_key)

            product_context = _get_top_products_context()
            system_prompt = (
                "You are a helpful AI shopping assistant for an Indian e-commerce store. "
                "IMPORTANT RULES:\n"
                "1. Always use Indian Rupees (₹) for ALL prices. NEVER use $ or USD.\n"
                "2. NEVER output raw CSV data, column names, or table formats.\n"
                "3. Present product lists as a clean, readable bulleted list.\n"
                "4. CRITICAL: Every product you list MUST include a clickable Markdown link in the format: [View Product](/product/PROD_ID_HERE).\n"
                "5. Keep text responses friendly and concise.\n"
                "6. When asked about best-selling or top-rated products, use the data below.\n\n"
                + product_context
            )

            api_messages = [{"role": "system", "content": system_prompt}] + self.messages

            chat_completion = client.chat.completions.create(
                messages=api_messages,
                model="llama-3.1-8b-instant",
            )
            bot_response = chat_completion.choices[0].message.content
            self.messages.append({"role": "assistant", "content": bot_response})

        except Exception as e:
            self.messages.append({"role": "assistant", "content": f"API Error: {str(e)}"})

    def handle_key_down(self, key: str):
        """Send message when Enter is pressed."""
        if key == "Enter":
            return ChatState.send_message


def chatbot() -> rx.Component:
    """Floating AI assistant for the E-commerce app with premium design."""
    return rx.box(
        rx.cond(
            ChatState.is_open,
            rx.box(
                rx.vstack(
                    # ── Header ────────────────────────────────────────────
                    rx.hstack(
                        rx.vstack(
                            rx.hstack(
                                rx.icon("sparkles", size=18, color="#60a5fa"),
                                rx.heading("AI Concierge", size="4", color="white", weight="bold"),
                                spacing="2",
                            ),
                            rx.text("Online & Ready to Help", color="#34d399", size="1", font_weight="500"),
                            spacing="0",
                            align_items="start",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon("minus", size=18),
                            size="1",
                            variant="ghost",
                            on_click=ChatState.toggle_chat,
                            color="rgba(255,255,255,0.4)",
                            _hover={"background": "rgba(255,255,255,0.1)", "color": "white"},
                        ),
                        width="100%",
                        padding="1.5rem",
                        background="rgba(255,255,255,0.03)",
                        border_bottom="1px solid rgba(255,255,255,0.1)",
                    ),

                    # ── Messages ──────────────────────────────────────────
                    rx.vstack(
                        rx.foreach(
                            ChatState.messages,
                            lambda m: rx.box(
                                rx.vstack(
                                    rx.text(
                                        rx.cond(m["role"] == "user", "You", "Concierge"),
                                        size="1",
                                        color="rgba(255,255,255,0.4)",
                                        margin_bottom="0.2rem",
                                        text_align=rx.cond(m["role"] == "user", "right", "left"),
                                        width="100%",
                                    ),
                                    rx.box(
                                        rx.markdown(m["content"]),
                                        background=rx.cond(
                                            m["role"] == "user", 
                                            "linear-gradient(135deg, #3b82f6, #1d4ed8)", 
                                            "rgba(255,255,255,0.05)"
                                        ),
                                        color="white",
                                        padding="0.8rem 1.2rem",
                                        border_radius=rx.cond(
                                            m["role"] == "user", 
                                            "20px 20px 4px 20px", 
                                            "20px 20px 20px 4px"
                                        ),
                                        border=rx.cond(
                                            m["role"] == "user",
                                            "none",
                                            "1px solid rgba(255,255,255,0.1)"
                                        ),
                                        box_shadow=rx.cond(
                                            m["role"] == "user",
                                            "0 4px 15px rgba(59,130,246,0.3)",
                                            "none"
                                        ),
                                    ),
                                    align_items=rx.cond(m["role"] == "user", "end", "start"),
                                ),
                                align_self=rx.cond(
                                    m["role"] == "user", "flex-end", "flex-start"
                                ),
                                max_width="85%",
                                sx={
                                    "p": {"margin": "0", "font_size": "0.9rem", "line_height": "1.5"},
                                    "ul": {"padding_left": "1.2em", "margin": "0.5em 0"},
                                    "a": {"color": "#60a5fa", "font_weight": "bold", "text_decoration": "underline"},
                                }
                            ),
                        ),
                        width="100%",
                        height="420px",
                        overflow_y="auto",
                        padding="1.5rem",
                        align_items="stretch",
                        spacing="4",
                        css={
                            "&::-webkit-scrollbar": {
                                "width": "4px",
                            },
                            "&::-webkit-scrollbar-thumb": {
                                "background": "rgba(255,255,255,0.1)",
                                "border-radius": "10px",
                            },
                        },
                    ),

                    # ── Input ─────────────────────────────────────────────
                    rx.box(
                        rx.hstack(
                            rx.input(
                                placeholder="Whisper your desires...",
                                value=ChatState.current_input,
                                on_change=ChatState.set_current_input,
                                on_key_down=ChatState.handle_key_down,
                                border="1px solid rgba(255,255,255,0.1)",
                                background="rgba(0,0,0,0.2)",
                                color="white",
                                border_radius="xl",
                                _focus={"border": "1px solid #3b82f6", "box_shadow": "0 0 10px rgba(59,130,246,0.2)"},
                                height="2.8rem",
                            ),
                            rx.button(
                                rx.icon("send", size=18),
                                on_click=ChatState.send_message,
                                background="linear-gradient(135deg, #3b82f6, #1d4ed8)",
                                color="white",
                                border_radius="xl",
                                height="2.8rem",
                                _hover={"transform": "scale(1.05)", "box_shadow": "0 0 15px rgba(59,130,246,0.4)"},
                            ),
                            width="100%",
                            padding="1.5rem",
                            spacing="3",
                        ),
                        border_top="1px solid rgba(255,255,255,0.1)",
                        width="100%",
                    ),

                    width="100%",
                    spacing="0",
                ),
                position="fixed",
                bottom="6rem",
                right="2rem",
                width="400px",
                background="rgba(15, 23, 42, 0.85)",
                backdrop_filter="blur(25px)",
                border="1px solid rgba(59,130,246,0.2)",
                border_radius="3xl",
                box_shadow="0 25px 60px rgba(0,0,0,0.6), 0 0 40px rgba(59,130,246,0.1)",
                z_index="2000",
                overflow="hidden",
            ),
        ),

        # ── FAB toggle ──────────────────────────────────────────────────
        rx.button(
            rx.cond(
                ChatState.is_open,
                rx.icon("chevron-down", size=24),
                rx.hstack(
                    rx.box(
                        background="#3b82f6",
                        width="8px",
                        height="8px",
                        border_radius="full",
                        box_shadow="0 0 10px #3b82f6",
                    ),
                    rx.icon("message-square", size=22),
                    rx.text("AI Help", size="2", weight="bold"),
                    spacing="2",
                    padding_x="4px",
                ),
            ),
            position="fixed",
            bottom="2rem",
            right="2rem",
            height="3.5rem",
            px=rx.cond(ChatState.is_open, "1rem", "1.5rem"),
            border_radius="2rem",
            background="linear-gradient(135deg, #1e293b, #0f172a)",
            color="white",
            border="1px solid rgba(59,130,246,0.4)",
            box_shadow="0 10px 30px rgba(0,0,0,0.4), 0 0 20px rgba(59,130,246,0.2)",
            _hover={
                "transform": "translateY(-4px) scale(1.05)",
                "box_shadow": "0 15px 40px rgba(0,0,0,0.5), 0 0 30px rgba(59,130,246,0.3)",
                "border_color": "#3b82f6",
            },
            transition="all 0.3s ease",
            on_click=ChatState.toggle_chat,
            z_index="2000",
        ),
    )
