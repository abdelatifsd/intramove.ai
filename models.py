class StripeCustomer:
    def __init__(self,hashed_api_key,calls,active,customer_id,customer_email):
        self.hashed_api_key = hashed_api_key
        self.calls:int = calls
        self.active = active
        self.customer_id = customer_id
        self.customer_email = customer_email