class StripeCustomer:
    def __init__(
        self,
        api_key,
        headline_credits_available,
        article_credits_available,
        number_of_payments,
        headline_active,
        article_active,
        stripe_customer_id,
        email,
        name,
        postal_code,
        country,
        total_spend,
        headline_credits_consumed,
        article_credits_consumed,
    ):
        self.api_key = api_key
        self.headline_credits_available: int = headline_credits_available
        self.article_credits_available: int = article_credits_available
        self.number_of_payments: int = number_of_payments
        self.headline_active = headline_active
        self.article_active = article_active
        self.stripe_customer_id = stripe_customer_id
        self.email = email
        self.name = name
        self.postal_code = postal_code
        self.country = country
        self.total_spend = total_spend
        self.headline_credits_consumed = headline_credits_consumed
        self.article_credits_consumed = article_credits_consumed

    def generate_dict(self):
        return {
            "api_key": self.api_key,
            "headline_credits_available": self.headline_credits_available,
            "article_credits_available": self.article_credits_available,
            "number_of_payments": self.number_of_payments,
            "headline_active": self.headline_active,
            "article_active": self.article_active,
            "stripe_customer_id": self.stripe_customer_id,
            "email": self.email,
            "name": self.name,
            "postal_code": self.postal_code,
            "country": self.country,
            "total_spend": self.total_spend,
            "headline_credits_consumed": self.headline_credits_consumed,
            "article_credits_consumed": self.article_credits_consumed,
        }
