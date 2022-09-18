from config import SERVER, TOP_K
from jina import Client, Document


def get_matches(input, server=SERVER, limit=TOP_K, filters=None):
    print(f"Server: {server}")
    client = Client(host=server)
    response = client.search(
        Document(text=input),
        return_results=True,
        parameters={"limit": limit, "filter": filters},
        show_progress=True,
    )

    return response[0].matches


def get_matches_from_image(input, server=SERVER, limit=TOP_K, filters=None):
    data = input.read()
    query_doc = Document(blob=data)

    client = Client(host=server)
    response = client.search(
        query_doc,
        return_results=True,
        parameters={"limit": limit, "filter": filters},
        show_progress=True,
    )

    return response[0].matches


def print_stars(rating, maximum=5):
    rating = int(rating)
    positive = "★"
    negative = "☆"

    string = rating * positive + (maximum - rating) * negative

    return string


class facets:
    Network = ["Ethereum", "Poygon"]
    season = ["Posersnft", "EtherPoap", "Nkrz", "Renga"]
    Name = [
        "Azuki",
        "Bored Ape",
        "Otherside",
        "Muant APe",
        "Cool cats",
        "Beanz",
        "Cryptopunks",
        "Tykes",
        "Moonbirds",
        "Bull BTC",
        "Pudgy Penguins",
        "Clone X",
        "Angels & Demons",
        "Genuine Undead",
        "Doodles",
        "Khaki",
        "Lavender",
        "Lime Green",
        "Magenta",
        "Maroon",
        "Mauve",
        "Metallic",
        "Multi",
        "Mushroom Brown",
        "Mustard",
        "NA",
        "Navy Blue",
        "Nude",
        "Off White",
        "Olive",
        "Orange",
        "Peach",
        "Pink",
        "Purple",
        "Red",
        "Rose",
        "Rust",
        "Sea Green",
        "Silver",
        "Skin",
        "Steel",
        "Tan",
        "Taupe",
        "Teal",
        "Turquoise Blue",
        "White",
        "Yellow",
    ]
    usage = [
        "",
        "Casual",
        "Ethnic",
        "Formal",
        "Home",
        "NA",
        "Party",
        "Smart Casual",
        "Sports",
        "Travel",
    ]
    masterCategory = [
        "Art",
        "Music",
        "Trading Cards",
        "Collectibles",
        "Photography",
        "Uility",
        "Sports",
    ]