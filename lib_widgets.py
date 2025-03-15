from textual.binding import Binding
from textual.canvas import HorizontalLine
from textual.widgets import ListView, Static, Markdown, Rule, Label
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll, Container
from textual.screen import Screen
from markdownify import markdownify as md
from dateutil.parser import parse as dparse
import timeago
import datetime
import textwrap

from enums import BASE_URL
import lib


def parse(date_str):
    d = dparse(date_str, ignoretz=True)
    now = datetime.datetime.now()
    return timeago.format(d, now)


class Post(VerticalGroup):
    def __init__(self, *args, **kwargs):
        self.post = kwargs.get("post")
        del kwargs["post"]
        super().__init__(*args, **kwargs)

    def compose(self):
        yield Markdown(md(self.post.get("cooked")))
        created_at = parse(self.post.get("created_at"))
        username = self.post.get("username")
        footer = f""" [blue]@{username}[/blue] created {created_at} """
        yield Label(footer)
        yield Rule()


class TopicHeader(VerticalGroup):
    def __init__(self, *args, **kwargs):
        self.post = kwargs.get("post")
        del kwargs["post"]
        super().__init__(*args, **kwargs)

    def compose(self):
        post = self.post
        url = f"{BASE_URL}/t/{post.get('slug')}"
        title = textwrap.dedent(
            f"""
        [bold]{post.get("title")}[/bold]
        {url} 
        Posts {post.get("posts_count")}  created {parse(post.get("created_at"))}
        """
        )
        yield Label(title)
        yield Rule(line_style="dashed")


class CustomVerticalScroll(VerticalScroll):
    BINDINGS = VerticalScroll.BINDINGS + [
        Binding("k", "scroll_up", "Scroll Up", show=False),
        Binding("j", "scroll_down", "Scroll Down", show=False),
    ]


class Topic(VerticalGroup):
    def __init__(self, *args, **kwargs):
        self.post_id = kwargs.get("post_id")
        del kwargs["post_id"]
        super().__init__(*args, **kwargs)

    def compose(self):
        self.headers = lib.get_headers()
        topic_id = self.post_id.split("_")[-1]
        post = lib.get_topic_id(topic_id, self.headers)
        with CustomVerticalScroll():
            yield TopicHeader(post=post)
            for i in post.get("post_stream").get("posts"):
                yield Post(post=i)


class PostScreen(Screen):
    BINDINGS = [
        Binding("h", "cursor_left", "Cursor left", show=False),
        Binding("left", "cursor_left", "Cursor left", show=False),
    ]

    def __init__(self, *args, **kwargs):
        self.post_id = kwargs.get("post_id")
        del kwargs["post_id"]
        super().__init__(*args, **kwargs)

    def action_cursor_left(self):
        self.app.pop_screen()

    def compose(self):
        with Container(id="post_content"):
            yield Topic(post_id=self.post_id)


class ListViewCustom(ListView):
    BINDINGS = [
        Binding("enter", "select_cursor", "Select", show=True),
        Binding("l", "select_cursor", "Select", show=False),
        Binding("up", "cursor_up", "Cursor up", show=False),
        Binding("k", "cursor_up", "Cursor up", show=False),
        Binding("down", "cursor_down", "Cursor down", show=False),
        Binding("j", "cursor_down", "Cursor down", show=False),
    ]

    def compose(self):
        self.headers = lib.get_headers()
        return super().compose()

    def on_list_view_selected(self, item):
        post_id = item.item.id
        post_screen = PostScreen(post_id=post_id)
        self.app.push_screen(post_screen)
