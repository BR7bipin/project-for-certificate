import argparse
import json
import os
from typing import List, Dict, Optional

DATA_FILE = "tasks.json"


class TaskManager:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.tasks: List[Dict] = []
        self.load()

    def add_task(self, description: str) -> None:
        task_id = self._next_id()
        self.tasks.append({"id": task_id, "description": description})
        print(f"Added task #{task_id}: {description}")

    def remove_task(self, task_id: int) -> bool:
        for i, t in enumerate(self.tasks):
            if t["id"] == task_id:
                removed = self.tasks.pop(i)
                print(f"Removed task #{removed['id']}: {removed['description']}")
                return True
        print(f"No task found with id {task_id}.")
        return False

    def list_tasks(self) -> None:
        if not self.tasks:
            print("No tasks found.")
            return
        print("Tasks:")
        for t in self.tasks:
            print(f"  {t['id']}. {t['description']}")

    def search_tasks(self, query: str) -> None:
        found = [t for t in self.tasks if query.lower() in t["description"].lower()]
        if not found:
            print(f"No tasks found matching '{query}'.")
            return
        print(f"Found {len(found)} task(s):")
        for t in found:
            print(f"  {t['id']}. {t['description']}")

    def save(self) -> None:
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.data_file):
            self.tasks = []
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except:
            self.tasks = []

    def clear_all(self) -> None:
        self.tasks = []
        self.save()
        print("All tasks cleared.")

    def _next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(t["id"] for t in self.tasks) + 1


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add")
    a.add_argument("description", type=str)

    sub.add_parser("list")

    r = sub.add_parser("remove")
    r.add_argument("id", type=int)

    s = sub.add_parser("search")
    s.add_argument("query", type=str)

    sub.add_parser("save")
    sub.add_parser("clear")

    return p.parse_args(argv)


def main():
    args = parse_args()
    manager = TaskManager()

    if args.command == "add":
        manager.add_task(args.description)
        manager.save()
    elif args.command == "list":
        manager.list_tasks()
    elif args.command == "remove":
        manager.remove_task(args.id)
        manager.save()
    elif args.command == "search":
        manager.search_tasks(args.query)
    elif args.command == "save":
        manager.save()
    elif args.command == "clear":
        confirm = input("Are you sure? (yes/no): ").lower()
        if confirm == "yes":
            manager.clear_all()
        else:
            print("Cancelled.")


if __name__ == "__main__":
    main()
