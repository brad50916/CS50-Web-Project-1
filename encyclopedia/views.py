from django.shortcuts import render
from django.http import HttpResponse
from . import util
from markdown2 import markdown
from django import forms
import random as ran

class SearchForm(forms.Form):
    result = forms.CharField(label="Search Encyclopedia")
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs) 
        self.fields['result'].widget.attrs['style'] = 'width:150px; height:25px;'

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['style'] = 'width:150px; height:25px; display:block'
        self.fields['content'].widget.attrs['style'] = 'width:700px; height:400px; display:block'

class EditForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs) 
        self.fields['content'].widget.attrs['style'] = 'width:700px; height:400px; display:block'

def search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        result = form.cleaned_data["result"]
        if util.get_entry(result) != None:
            content = markdown(util.get_entry(result))
            return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": result,
            "form": SearchForm()
        })
        else:
            result_list = []
            for x in util.list_entries():
                if result.lower() in x.lower():
                    result_list.append(x)
            if len(result_list) == 0:
                c=1
            else:
                c=0
            return render(request, "encyclopedia/search.html", {
            "title": result,
            "form": SearchForm(),
            "data": result_list,
            "condition": c
            })

def index(request):
    if request.method == "POST":
        return search(request)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, name):
    v=0
    if request.method == "POST":
        return search(request)
    if util.get_entry(name) == None:
        content = markdown("# Error \nrequested page was not found")
        return render(request, "encyclopedia/error.html", {
        "content": content,
        "form": SearchForm()
    }) 
    else:
        content = markdown(util.get_entry(name))
    return render(request, "encyclopedia/entry.html", {
        "content": content,
        "title": name,
        "form": SearchForm()
    })

def edit(request, name):
    if request.POST.get("form_type")=="search":
        return search(request)
    form = EditForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data["content"]
        util.save_entry(name, content)
        content = markdown(util.get_entry(name))
        return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": name,
            "form": SearchForm()
        })
    return render(request, "encyclopedia/edit.html", {
        "title": name,
        "form": SearchForm(),
        "form2": EditForm(initial={'content': util.get_entry(name)})
    })

def create(request):
    if request.POST.get("form_type")=="search":
        return search(request)
    form = CreateForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        if util.verify(title):
            content1 = markdown("# Error \n An encyclopedia entry already exists with the provided title") 
            return render(request, "encyclopedia/entry.html", {
            "content": content1,
            "title": title,
            "form": SearchForm()
        })
        else:
            util.save(title, content)
            newcontent = markdown(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
            "content": newcontent,
            "title": title,
            "form": SearchForm() 
        }) 
    return render(request, "encyclopedia/create.html", {
        "form1": CreateForm(),
        "form": SearchForm()
    })

def random(request):
    if request.method == "POST":
        return search(request) 
    l = len(util.list_entries())
    list=util.list_entries()
    r = ran.randint(0,l-1)
    print(r)
    content = markdown(util.get_entry(list[r]))
    return render(request, "encyclopedia/entry.html", {
        "content": content,
        "title": list[r],
        "form": SearchForm()
    })


