import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создаёт продукт в Stripe."""
    stripe_product = stripe.Product.create(name=product.name, description=product.description)
    return stripe_product


def create_stripe_price(stripe_product, amount):
    """Создаёт цену продукта в Stripe."""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=stripe_product.get("id")
    )
    return price


def create_stripe_session(price):
    """ Создаёт цену продукта в Stripe. """
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
