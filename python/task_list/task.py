class Task:
    def __init__(self, id_: int, description: str, done: bool) -> None:
        self.id = id_
        self.description = description
        self.done = done

    def set_done(self, done: bool) -> None:
        self.done = done

    def is_done(self) -> bool:
        return self.done

    @property
    def summary(self) -> str:
        checkbox = "[x]" if self.done else "[ ]"

        return f"  {checkbox} {self.id}: {self.description}"
