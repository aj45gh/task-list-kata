from typing import Dict, IO, List, Optional

from task_list.exceptions import CommandNotFoundError, ProjectAlreadyExistsError
from task_list.project import Project
from task_list.task import Task


class TaskList:
    QUIT = "quit"

    def __init__(self, console: "Console") -> None:
        self.console = console
        self.last_id: int = 0
        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, List[Task]] = {}

    def run(self) -> None:
        while True:
            command = self.console.input("> ")
            if command == self.QUIT:
                break
            self.execute(command)

    def execute(self, command_line: str) -> None:
        command_rest = command_line.split(" ", 1)
        command = command_rest[0]
        if command == "show":
            self.show()
        elif command == "add":
            self.add(command_rest[1])
        elif command == "check":
            self.check(command_rest[1])
        elif command == "uncheck":
            self.uncheck(command_rest[1])
        elif command == "help":
            self.help()
        else:
            raise CommandNotFoundError(f"Command '{command}' not found")

    def show(self) -> None:
        for project, tasks in self.tasks.items():
            self.console.print(project)
            for task in tasks:
                self.console.print(task.summary)
            self.console.print()

    def add(self, command_line: str) -> None:
        sub_command_rest = command_line.split(" ", 1)
        sub_command = sub_command_rest[0]
        if sub_command == "project":
            self.add_project(sub_command_rest[1])
        elif sub_command == "task":
            project_task = sub_command_rest[1].split(" ", 1)
            self.add_task(project_task[0], project_task[1])

    def add_project(self, name: str) -> None:
        if name in self.projects:
            raise ProjectAlreadyExistsError()

        self.projects[name] = Project(_id=name)
        self.tasks[name] = []

    def add_task(self, project: str, description: str) -> None:
        project_tasks = self.tasks.get(project)
        if project_tasks is None:
            self.console.print(f"Could not find a project with the name {project}.")
            self.console.print()
            return
        project_tasks.append(Task(self.next_id(), description, False))

    def check(self, id_string: str) -> None:
        self.set_done(id_string, True)

    def uncheck(self, id_string: str) -> None:
        self.set_done(id_string, False)

    def set_done(self, id_string: str, done: bool) -> None:
        id_ = int(id_string)
        for project, tasks in self.tasks.items():
            for task in tasks:
                if task.id == id_:
                    task.set_done(done)
                    return
        self.console.print(f"Could not find a task with an ID of {id_}")
        self.console.print()

    def help(self) -> None:
        self.console.print("Commands:")
        self.console.print("  show")
        self.console.print("  add project <project name>")
        self.console.print("  add task <project name> <task description>")
        self.console.print("  check <task ID>")
        self.console.print("  uncheck <task ID>")
        self.console.print()

    def next_id(self) -> int:
        self.last_id += 1
        return self.last_id


class Console:
    COMMANDS = {}

    def __init__(self, input_reader: IO, output_writer: IO) -> None:
        self.input_reader = input_reader
        self.output_writer = output_writer

    def print(
        self, string: Optional[str] = "", end: str = "\n", flush: bool = True
    ) -> None:
        self.output_writer.write(f"{string}{end}")
        if flush:
            self.output_writer.flush()

    def input(self, prompt: Optional[str] = "") -> str:
        self.print(prompt, end="")
        return self.input_reader.readline().strip()
