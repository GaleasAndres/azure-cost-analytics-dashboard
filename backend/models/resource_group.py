class ResourceGroup:

    def __init__(self, name: str, location: str, tags: dict[str, str], id: str):
        self.id = id
        self.name = name
        self.location = location
        self.tags = tags

    def __str__(self):
        return f"ResourceGroup(id={self.id}, name={self.name}, location={self.location})"