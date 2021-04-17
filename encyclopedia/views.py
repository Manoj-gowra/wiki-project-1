from django.forms.widgets import Textarea
import markdown2
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
from django import forms
from re import match
from django.urls import reverse
import random


class NewPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return HttpResponse("<h1>Page not found</h1>")
    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {"entry": markdown2.markdown(entryPage), "entryTitle": entry},
        )


def search(request):
    value = request.GET["q"]
    entries = util.list_entries()
    if value in entries:
        return redirect(entry, entry=value)
    else:
        filtered_values = list(
            sorted(filter(lambda v: match("^" + value.lower(), v.lower()), entries))
        )
        if filtered_values == []:
            # return HttpResponse("<h1>Page Not Found</h1>")
            return redirect(index)
        else:
            return render(
                request, "encyclopedia/search.html", {"values": filtered_values}
            )


def createNewPage(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["message"]
            code = False
            if title in util.list_entries():
                print("try with another")
                code = True
                return render(
                    request, "encyclopedia/createNewPage.html", {"form": form,"code":code}
                )
            else:
                util.save_entry(title, content)
                return redirect("entry",entry=title)
        else:
            return render(request, "encyclopedia/createNewPage.html", {"form": form})
    return render(request, "encyclopedia/createNewPage.html", {"form": NewPage()})


def editPage(request,entry):
    print(entry)
    print(request)
    existPage = util.get_entry(entry)
    print(existPage)
    data = {"title":entry,"message":existPage}
    form = NewPage(initial=data)
    print(form)
    return render(request,"encyclopedia/edit.html",{"form":form})


def updatePage(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["message"]
            util.save_entry(title, content)
            return redirect("entry",entry=title)
        else:
            return render(request, "encyclopedia/createNewPage.html", {"form": form})
    return render(request, "encyclopedia/createNewPage.html", {"form": NewPage()})


def RandomPage(request):
    entries = util.list_entries()
    num = random.randint(0, len(entries) - 1)
    page_random = entries[num]
    return redirect(entry, entry=page_random)