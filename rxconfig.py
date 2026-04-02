import os
import reflex as rx
from reflex.plugins import SitemapPlugin

# Use REFLEX_API_URL when provided by deployed environments.
# Fall back to local Reflex runtime in development.
api_url = os.environ.get("REFLEX_API_URL") or "http://127.0.0.1:8000"

config = rx.Config(
    app_name="ai_recommendation",
    api_url=api_url,
    plugins=[SitemapPlugin()],
)
