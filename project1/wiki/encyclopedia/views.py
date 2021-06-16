from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
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


def edit_entry():
    return None


def new_entry():
    return None


def search(request):
    characters = request.GET.get("q", "")
    if util.get_entry(characters) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": characters}))
    else:
        substring = []
        for entry in util.list_entries():
            if characters.upper() in entry.upper():
                substring.append(entry)

        return render(request, "encyclopedia/index.html", {
            "entries": substring,
            "search": True,
            "characters:": characters
        })


def random():
    # adding this comment to test something
    return None
