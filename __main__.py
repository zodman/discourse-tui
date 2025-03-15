from textual.app import App
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Label, ListView, ListItem, Placeholder, Pretty
import list_posts
import lib_widgets

import lib


class TableApp(App):
    SCREENS = {"post": lib_widgets.PostScreen}

    def compose(self):
        self.headers = lib.get_headers()
        self.categories = lib.list_categories(self.headers)
        with Container(id="content"):
            for i in self.__load_posts():
                yield i

    def __load_posts(self):
        posts = list_posts.latest_post(self.headers)
        with lib_widgets.ListViewCustom():
            for i in posts:
                text = lib.get_post_formated(i, self.categories, self.headers)
                id = i["id"]
                yield ListItem(Label(text), id=f"post_{id}_{i['topic_id']}")


app = TableApp()
if __name__ == "__main__":
    app.run()
