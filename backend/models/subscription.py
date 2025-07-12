class Subscription:

    def __init__(self, id: str, name: str, state: str):
        self.id = id
        self.name = name
        self.state = state

    def __Str__(self):
        return f"Subscription(id={self.id}, name={self.name}, state={self.state})"
