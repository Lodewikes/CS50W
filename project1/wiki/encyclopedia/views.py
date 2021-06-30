from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from markdown2 import Markdown
import random
from . import util


class InputForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"id": "title-field"}))
    text_area = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20, "id": "text-field"}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


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


def edit_entry(request, title):
    # TODO implement
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/entryNotExists.html", {
            "title": title
        })
    else:
        form = InputForm()
        form.fields["title"].initial = title
        form.fields["text_area"].initial = entry
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/createEntry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "title": form.fields["title"].initial
        })


def new_entry(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text_area"]
            if util.get_entry(title) is None or form.cleaned_data["edit"] is True:
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse("get_wiki", kwargs={"title": title}))
            else:
                return render(request, "encyclopedia/createEntry.html", {
                    "form": form,
                    "exist": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/createEntry.html", {
                "form": form,
                "exist": False,
            })
    else:
        return render(request, "encyclopedia/createEntry.html", {
            "form": InputForm(),
            "exist": False
        })


def search(request):
    user_input = request.GET.get("q", "")
    if util.get_entry(user_input) is not None:
        return HttpResponseRedirect(reverse("get_wiki", kwargs={"title": user_input}))
    else:
        substring = []
        for entry in util.list_entries():
            if user_input.upper() in entry.upper():
                substring.append(entry)

        return render(request, "encyclopedia/index.html", {
            "entries": substring,
            "characters:": user_input
        })


def random_entry(request):
    markdowner = Markdown()

    entries_list = util.list_entries()
    entries = random.choice(entries_list)
    entry = util.get_entry(entries)

    return render(request, "encyclopedia/wikiPage.html", {
        "entry": markdowner.convert(entry),
        "title": entries
    })
