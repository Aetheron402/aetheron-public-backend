"""
Aetheron — Web Search Utility Template
--------------------------------------

This module provides a structural template for project-related
information lookup used within the backend.

The template illustrates:
- Function naming
- Input/output structure
- Expected keys in returned dictionaries

All network calls and content extraction steps are replaced with
placeholder logic suitable for public repositories.
"""

def search_project_info(query: str, api_key: str = None):
    """
    Template project information lookup.

    Parameters:
        query (str): The search query.
        api_key (str): Included for structural compatibility.

    Returns:
        dict: Structured information containing:
            - website_candidates
            - twitter_candidates
            - telegram_candidates
            - discord_candidates
            - description_extract
            - team_extract
            - roadmap_extract
    """

    # Template output with placeholder values
    return {
        "website_candidates": [
            "https://example.com"
        ],
        "twitter_candidates": [
            "https://twitter.com/example"
        ],
        "telegram_candidates": [
            "https://t.me/example"
        ],
        "discord_candidates": [
            "https://discord.gg/example"
        ],
        "description_extract": "Example project description text.",
        "team_extract": "Example team section text.",
        "roadmap_extract": "Example roadmap or milestones text.",
    }
