class StripeCustomer:
    def __init__(
        self,
        api_key,
        credits,  # active credits
        number_of_payments,
        active,
        stripe_customer_id,
        email,
        name,
        postal_code,
        country,
        total_spend,
        credits_consumed,
    ):
        self.api_key = api_key
        self.credits: int = credits
        self.number_of_payments: int = number_of_payments
        self.active = active
        self.stripe_customer_id = stripe_customer_id
        self.email = email
        self.name = name
        self.postal_code = postal_code
        self.country = country
        self.total_spend = total_spend
        self.credits_consumed = credits_consumed

    def generate_dict(self):
        return {
            "api_key": self.api_key,
            "credits": self.credits,
            "number_of_payments": self.number_of_payments,
            "active": self.active,
            "stripe_customer_id": self.stripe_customer_id,
            "email": self.email,
            "name": self.name,
            "postal_code": self.postal_code,
            "country": self.country,
            "total_spend": self.total_spend,
            "credits_consumed": self.credits_consumed,
        }
