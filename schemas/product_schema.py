product_schema = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "price": {"type": "number"},
        "stock": {"type": "integer"},
        "description": {"type": "string"},
        "animal_type": {"type": "string"},
        "expiration_date": {"type": "string"},
    },
    "required": ["product_name", "price", "stock"],
}
