from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2

from . import util

class CreateEntryForm(forms.Form):
    title = forms.CharField(label="Title")

    text = forms.CharField(widget=forms.Textarea, label='Text')

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

"""Create new wiki entry"""
def create(request):
    if request.method == "POST":
        form = CreateEntryForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title'].strip()
            text = form.cleaned_data['text'].strip()
            
            # Check if similar entry exists
            if util.get_entry(title):
                return HttpResponse('<h1>403 Such entry already exists</h1>', status=403)
            
            # Write new entry file into entries directory
            util.save_entry(title, bytes(text, 'utf8'))
            # with open(f'./entries/{title}.md', 'w+') as file:
            #     file.write(text.strip())

    return render(request, "encyclopedia/create.html", {
        "form" : CreateEntryForm()
    })