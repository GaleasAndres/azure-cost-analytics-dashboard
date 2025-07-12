class Resource:

    def __init__(self, id: str, name: str, resource_type: str, region: str, subscription_id: str,
                 tags: dict[str, str], resource_group_id: str):
        self.id = id
        self.name = name
        self.resource_type = resource_type
        self.region = region
        self.subscription_id = subscription_id
        self.tags = tags
        self.resource_group_id = resource_group_id

    def __str__(self):
        return (f"Resource(id={self.id}, name={self.name}, "
                f"type={self.resource_type}, region={self.region}, "
                f"subscription_id={self.subscription_id})")
