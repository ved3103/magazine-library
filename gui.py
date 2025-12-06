# Tkinter GUI for browsing and managing magazines

# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, Any, List, Optional

from client import MagazineClient, format_magazine_for_list
from models import VALID_CATEGORIES


class CreateMagazineDialog(simpledialog.Dialog):
    """
    Dialog window for creating a new magazine.
    """

    def body(self, master):
        self.title("Create new magazine")

        tk.Label(master, text="Title:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Label(master, text="Editor:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tk.Label(master, text="Publication date (YYYY-MM-DD):").grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        tk.Label(master, text="Category:").grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.entry_title = tk.Entry(master, width=30)
        self.entry_editor = tk.Entry(master, width=30)
        self.entry_pub_date = tk.Entry(master, width=30)
        self.combo_category = ttk.Combobox(
            master,
            values=VALID_CATEGORIES,
            state="readonly",
            width=27,
        )
        self.combo_category.current(0)

        self.entry_title.grid(row=0, column=1, padx=5, pady=5)
        self.entry_editor.grid(row=1, column=1, padx=5, pady=5)
        self.entry_pub_date.grid(row=2, column=1, padx=5, pady=5)
        self.combo_category.grid(row=3, column=1, padx=5, pady=5)

        return self.entry_title

    def validate(self) -> bool:
        title = self.entry_title.get().strip()
        editor = self.entry_editor.get().strip()
        pub_date = self.entry_pub_date.get().strip()
        category = self.combo_category.get().strip()

        if not title or not editor or not pub_date or not category:
            messagebox.showerror("Validation error", "All fields are required.")
            return False

        self.result = {
            "title": title,
            "editor": editor,
            "publication_date": pub_date,
            "category": category,
        }
        return True


class MagazineGUI(tk.Tk):
    """
    Tkinter GUI window for the magazine library.
    """

    def __init__(self, client: MagazineClient):
        super().__init__()
        self.client = client
        self.title("Magazine Library")
        self.geometry("850x420")

        # map listbox index -> magazine id
        self._index_to_id: Dict[int, int] = {}

        self._build_layout()

    # -------- layout --------

    def _build_layout(self):
        left = tk.Frame(self)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        center = tk.Frame(self)
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right = tk.Frame(self)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # left controls
        tk.Button(left, text="Load all magazines", command=self.on_load_all).pack(
            fill=tk.X, pady=5
        )

        tk.Label(left, text="Category:").pack(anchor="w")
        self.combo_category = ttk.Combobox(left, values=VALID_CATEGORIES, state="readonly")
        self.combo_category.current(0)
        self.combo_category.pack(fill=tk.X, pady=2)

        tk.Button(left, text="Load by category", command=self.on_load_by_category).pack(
            fill=tk.X, pady=5
        )

        tk.Label(left, text="Search by title:").pack(anchor="w", pady=(10, 0))
        self.entry_search = tk.Entry(left)
        self.entry_search.pack(fill=tk.X, pady=2)

        tk.Button(left, text="Search", command=self.on_search).pack(fill=tk.X, pady=5)

        # center list
        tk.Label(center, text="Magazines:").pack(anchor="w")
        self.listbox_mag = tk.Listbox(center)
        self.listbox_mag.pack(fill=tk.BOTH, expand=True)
        self.listbox_mag.bind("<<ListboxSelect>>", self.on_listbox_select)

        # right details
        tk.Label(right, text="Details:").pack(anchor="w")

        self.lbl_id = tk.Label(right, text="ID: -")
        self.lbl_title = tk.Label(right, text="Title: -")
        self.lbl_editor = tk.Label(right, text="Editor: -")
        self.lbl_date = tk.Label(right, text="Publication date: -")
        self.lbl_cat = tk.Label(right, text="Category: -")

        self.lbl_id.pack(anchor="w", pady=2)
        self.lbl_title.pack(anchor="w", pady=2)
        self.lbl_editor.pack(anchor="w", pady=2)
        self.lbl_date.pack(anchor="w", pady=2)
        self.lbl_cat.pack(anchor="w", pady=2)

        tk.Button(right, text="Create new magazine", command=self.on_create).pack(
            fill=tk.X, pady=(20, 5)
        )
        tk.Button(right, text="Delete selected magazine", command=self.on_delete).pack(
            fill=tk.X, pady=5
        )

    # -------- helpers --------

    def _populate_listbox(self, items: List[Dict[str, Any]]) -> None:
        self.listbox_mag.delete(0, tk.END)
        self._index_to_id.clear()
        for idx, item in enumerate(items):
            txt = format_magazine_for_list(item)
            self.listbox_mag.insert(tk.END, txt)
            self._index_to_id[idx] = item["id"]

    def _clear_details(self) -> None:
        self.lbl_id.config(text="ID: -")
        self.lbl_title.config(text="Title: -")
        self.lbl_editor.config(text="Editor: -")
        self.lbl_date.config(text="Publication date: -")
        self.lbl_cat.config(text="Category: -")

    def _show_details(self, item: Dict[str, Any]) -> None:
        self.lbl_id.config(text=f"ID: {item['id']}")
        self.lbl_title.config(text=f"Title: {item['title']}")
        self.lbl_editor.config(text=f"Editor: {item['editor']}")
        self.lbl_date.config(text=f"Publication date: {item['publication_date']}")
        self.lbl_cat.config(text=f"Category: {item['category']}")

    def _selected_mag_id(self) -> Optional[int]:
        sel = self.listbox_mag.curselection()
        if not sel:
            return None
        idx = sel[0]
        return self._index_to_id.get(idx)

    # -------- event handlers --------

    def on_load_all(self):
        try:
            mags = self.client.get_all_magazines()
            self._populate_listbox(mags)
            self._clear_details()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load magazines: {e}")

    def on_load_by_category(self):
        cat = self.combo_category.get()
        try:
            mags = self.client.get_by_category(cat)
            self._populate_listbox(mags)
            self._clear_details()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load by category: {e}")

    def on_search(self):
        title = self.entry_search.get().strip()
        if not title:
            messagebox.showinfo("Info", "Enter a title to search.")
            return
        try:
            mags = self.client.search_by_title(title)
            if not mags:
                messagebox.showinfo("Not found", "No magazine with that exact title.")
            self._populate_listbox(mags)
            self._clear_details()
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def on_listbox_select(self, _event):
        mag_id = self._selected_mag_id()
        if mag_id is None:
            return
        try:
            mag = self.client.get_by_id(mag_id)
            self._show_details(mag)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load details: {e}")

    def on_create(self):
        dialog = CreateMagazineDialog(self)
        if dialog.result is None:
            return
        try:
            self.client.create_magazine(dialog.result)
            self.on_load_all()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create magazine: {e}")

    def on_delete(self):
        mag_id = self._selected_mag_id()
        if mag_id is None:
            messagebox.showinfo("Info", "Select a magazine to delete.")
            return
        if not messagebox.askyesno("Confirm delete", "Delete this magazine?"):
            return
        try:
            self.client.delete_magazine(mag_id)
            self.on_load_all()
            self._clear_details()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete magazine: {e}")


if __name__ == "__main__":
    client = MagazineClient()
    app = MagazineGUI(client)
    app.mainloop()
