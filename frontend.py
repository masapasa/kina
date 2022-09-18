import streamlit as st
from helper import (
    get_matches,
    print_stars,
    get_matches_from_image,
    facets,
)
from config import TOP_K, SERVER, DEBUG

filters = {
    "$and": {
        # "price": {},
        "rating": {},
        "season": {},
        "masterCategory": {},
        # "gender": {},
        # "baseColour": {},
        # "year": {},
    }
}

title = "Search your favorite NFT"

st.set_page_config(page_title=title, layout="wide")

# Sidebar
st.sidebar.title("Options")

input_media = st.sidebar.radio(label="Search with...", options=["text", "image"])


filters["$and"]["masterCategory"]["$in"] = st.sidebar.multiselect(
    "Category", facets.masterCategory, default=facets.masterCategory
)

# filters["$and"]["gender"]["$in"] = st.sidebar.multiselect(
# "Gender", facets.gender, default=facets.gender
# )
filters["$and"]["season"]["$in"] = st.sidebar.multiselect(
    "season", facets.season, default=facets.season
)
# (
# filters["$and"]["price"]["$gte"],
# filters["$and"]["price"]["$lte"],
# ) = st.sidebar.slider("Price", 0, 200, (0, 200))

filters["$and"]["rating"]["$gte"] = st.sidebar.slider("Minimum rating", 0, 5, 0)
limit = st.sidebar.slider(
    label="Maximum results",
    min_value=int(TOP_K / 3),
    max_value=TOP_K * 3,
    value=TOP_K,
)
# filters["$and"]["baseColour"]["$in"] = st.sidebar.multiselect(
# "Color", facets.color, default=facets.color
# )
# (
# filters["$and"]["year"]["$gte"],
# filters["$and"]["year"]["$lte"],
# ) = st.sidebar.slider("Year", 2007, 2019, (2007, 2019))


if DEBUG:
    with st.sidebar.expander("Debug"):
        server = st.text_input(label="Server", value=SERVER)
else:
    server = SERVER

st.sidebar.title("About")

st.sidebar.markdown(
    """Do not get left behind on the latest web3 trend, Our search engine provides the latest trend"""
)

st.sidebar.markdown(
    "[Repo link](https://github.com/jina-ai/jina-multimodal-fashion-search)"
)

# Main area
st.title(title)

if input_media == "text":
    text_query = st.text_input(label="Search term", placeholder="Blue dress")
    text_search_button = st.button("Search")
    if text_search_button:
        matches = get_matches(
            input=text_query,
            limit=limit,
            filters=filters,
            server=server,
        )

elif input_media == "image":
    image_query = st.file_uploader(label="Image file")
    image_search_button = st.button("Search")
    if image_search_button:
        matches = get_matches_from_image(
            input=image_query,
            limit=limit,
            filters=filters,
            server=server,
        )

if "matches" in locals():
    for match in matches:
        pic_cell, desc_cell, price_cell = st.columns([1, 6, 1])
        pic_cell.image(match.tags["image_url"])
        desc_cell.markdown(
            f"##### {match.tags['productDisplayName']} {print_stars(match.tags['rating'])}"
        )
        desc_cell.markdown(
            f"*{match.tags['masterCategory']}*, *{match.tags['subCategory']}*, *{match.tags['articleType']}*, *{match.tags['baseColour']}*, *{match.tags['season']}*, *{match.tags['usage']}*, *{match.tags['year']}*"
        )
        price_cell.button(key=match.id, label=str(match.tags["price"]))