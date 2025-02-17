from textual.app import App
from textual.binding import Binding
from textual.widgets import Label, ListView, ListItem
import list_posts

import lib


class ListViewCustom(ListView):
    BINDINGS = [
        Binding("enter", "select_cursor", "Select", show=False),
        Binding("l", "select_cursor", "Select", show=False),
        Binding("up", "cursor_up", "Cursor up", show=False),
        Binding("k", "cursor_up", "Cursor up", show=False),
        Binding("down", "cursor_down", "Cursor down", show=False),
        Binding("j", "cursor_down", "Cursor down", show=False),
    ]


class TableApp(App):
    def compose(self):
        self.headers = lib.get_headers()
        self.categories = lib.list_categories(self.headers)
        posts = list_posts.latest_post(self.headers)
        with ListViewCustom():
            for i in posts[:30]:
                text = lib.get_post_formated(i, self.categories, self.headers)
                yield ListItem(Label(text))


app = TableApp()
if __name__ == "__main__":
    app.run()
