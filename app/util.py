"""
Utility Functions
"""
import logging
from math import prod
import socket
from app.models import Products
from app.db import db


def get_ld_non_human_user(request=None):
    """
    Representation of a non human "user" for use with LaunchDarkly
    ref https://docs.launchdarkly.com/sdk/features/user-config#python 
    """
    if request:
        request_ip = request.remote_addr
    else:
        request_ip = None
    user = {
        "key": socket.gethostname(),
        "ip": request_ip,
        "email": 'local@machine.com',
        "custom": {
            "type": "machine"
        }
    }
    logging.debug(user)
    return user

def load_products():
    data = [{
        "description": "Best Iphone at this price",
        "id": 1,
        "image_url": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg",
        "name": "Iphone XR",
        "on_sale": False,
        "price": 999.0,
        "product_type": "electronics",
        "sale_price": 699.0
    },
        {
        "description": "",
        "id": 2,
        "image_url": "https://images.pexels.com/photos/205926/pexels-photo-205926.jpeg",
        "name": "Headphone",
        "on_sale": True,
        "price": 400.0,
        "product_type": "electronics",
        "sale_price": 200.0
    },
        {
        "description": "",
        "id": 3,
        "image_url": "https://images.pexels.com/photos/1298601/pexels-photo-1298601.jpeg",
        "name": "Game Controller",
        "on_sale": False,
        "price": 700.0,
        "product_type": "electronics",
        "sale_price": 500.0
    },
        {
        "description": "",
        "id": 4,
        "image_url": "https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg",
        "name": "Apple Watch 6",
        "on_sale": True,
        "price": 999.0,
        "product_type": "electronics",
        "sale_price": 700.0
    },
        {
        "description": "Best Iphone at this price",
        "id": 5,
        "image_url": "https://images.pexels.com/photos/157675/fashion-men-s-individuality-black-and-white-157675.jpeg",
        "name": "Coat",
        "on_sale": False,
        "price": 20.0,
        "product_type": "fashion",
        "sale_price": 15.0
    },
        {
        "description": "",
        "id": 6,
        "image_url": "https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg",
        "name": "Yellow Hoodie",
        "on_sale": True,
        "price": 50.0,
        "product_type": "fashion",
        "sale_price": 40.0
    },
        {
        "description": "",
        "id": 7,
        "image_url": "https://images.pexels.com/photos/428340/pexels-photo-428340.jpeg",
        "name": "Offwhite T-Shirt",
        "on_sale": False,
        "price": 30.0,
        "product_type": "fashion",
        "sale_price": 15.0
    },
        {
        "description": "",
        "id": 8,
        "image_url": "https://images.pexels.com/photos/3193731/pexels-photo-3193731.jpeg",
        "name": "Nike Shoe",
        "on_sale": True,
        "price": 50.0,
        "product_type": "fashion",
        "sale_price": 47.0
    }
    ]
    for prod in data:
        p = Products(
            name=prod['name'],
            description=prod['description'],
            price=prod['price'],
            image_url=prod['image_url'],
            product_type=prod['product_type'],
            on_sale=prod['on_sale'],
            sale_price=prod['sale_price']
        )
        db.session.add(p)
        db.session.commit()
