from django.shortcuts import render
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# display a wiki
def get_wiki(request, title):
    markdowner = Markdown()
    entry = util.get_entry(title=title)
    if entry is None:
        # TODO render an error page showing the title is unavailable
        return render(request, "encyclopedia/entryNotExists.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/wikiPage.html", {
            "entry": markdowner.convert(entry),
            "title": title
        })
