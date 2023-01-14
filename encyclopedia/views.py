from django.shortcuts import render
from django.http import HttpResponseNotFound
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    content = util.get_entry(entry)
    if content:
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "content": content
        })
    else:
        return HttpResponseNotFound("<h1>404 Not found</h1>")