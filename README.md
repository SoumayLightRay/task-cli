# 🛠️ Task CLI

A simple, clean command-line tool to manage your tasks, built in Python.

---

## 🚀 Features
- Add new tasks
- Update existing tasks
- Delete tasks
- List all tasks in a pretty table
- Mark tasks as "In Progress" or "Done"
- Clear all tasks with confirmation
- Save tasks persistently in a local JSON file

---

## 📦 Requirements
- Python 3.7+
- [tabulate](https://pypi.org/project/tabulate/) package

Install tabulate if you don't have it:

```bash
pip install tabulate


# Add a new task
python task_cli.py add "Buy groceries"

# List all tasks
python task_cli.py list

# Update a task
python task_cli.py update 1 "Buy groceries and cook dinner"

# Mark a task as done
python task_cli.py mark-done 1

# Delete a task
python task_cli.py delete 1


---

✅ After you create the README:

```bash
git add README.md
git commit -m "Added README file"
git push
