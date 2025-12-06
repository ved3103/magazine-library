# Magazine Library

A small Python application to manage magazines using a **Flask backend**, a **Tkinter GUI frontend**, and **JSON** for storage.

The app allows you to:
- View all magazines
- Filter by category
- Search by exact title
- View details (title, date, author, category)
- Add new magazines
- Delete existing magazines

---

## Requirements

- Python 3.x installed
- The following Python packages:
  - flask
  - requests

Install dependencies with:

```bash
pip install flask requests
Make sure all project files are in the same folder:
backend.py
gui.py
client.py
models.py
storage.py
magazines.json
(optional) tests_backend.py, tests_frontend.py
How to Run the Project (Step by Step)
1. Open a terminal in the project folder

Example on Windows (PowerShell / CMD):

cd path\to\project\folder

Start the backend (Flask API)

In the terminal, run:

python backend.py


You should see output similar to:

* Running on http://127.0.0.1:5000
Start the GUI (Tkinter app)

Open a second terminal window, go to the same folder, and run:

python gui.py


This will open the Magazine Library window.
From the GUI you can:

Load all magazines – see all entries from magazines.json

Filter by category – choose a category and load only those magazines

Search by title – enter an exact title and search

View details – select a magazine from the list to see its metadata

Add magazine – open a form, fill in fields, and save

Delete magazine – select a magazine and remove it

All changes are stored in magazines.json.
