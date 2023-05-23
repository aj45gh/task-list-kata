from typing import Dict

from task_list.task import Task


class Project:
    def __init__(self, _id: str):
        self.id = _id
        self.tasks: Dict[str, Task] = {}
