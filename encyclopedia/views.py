from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    content = util.get_entry(entry)
    
    # Check if entry exists
    if content:
        # Convert markdown to HTML format
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "content": content
        })

    # Raise 404 if no such entry        
    return HttpResponseNotFound("<h1>404 Not found</h1>")

def search(request):
    query = request.GET.get('q')
    
    # If query matches the name of entry, redirect to that entry
    if util.get_entry(query):
        return HttpResponseRedirect(reverse('wiki', kwargs={'entry': query}))
    
    # Else return similar entries
    entries = filter(lambda entry: query.lower() in entry.lower(), util.list_entries())
    
    # Render items
    return render(request, 'encyclopedia/search.html', {
        'entries': entries
    })
