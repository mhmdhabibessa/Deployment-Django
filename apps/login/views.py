from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "login/index.html")



def register(request):
    errors = User.objects.validator(request.POST, "registration")
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        
        hasPassword = bcrypt.hashpw(request.POST['reg-pword'].encode(), bcrypt.gensalt()).decode() 
        User.objects.create(first_name=request.POST['reg-fname'], last_name=request.POST['reg-lname'], email=request.POST['reg-email'], password=hasPassword)
        thisUser = User.objects.last()
        request.session['user_id'] = thisUser.id
        request.session['user_fname'] = thisUser.first_name
        return redirect("/wall")


def login(request):
    user = User.objects.filter(email=request.POST['log-email'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['log-pword'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            request.session['user_fname'] = logged_user.first_name
            return redirect("/wall")
        else:
            messages.error(request, "The email and password combination entered do not match a record in our database")
            return redirect('/')  
    messages.error(request, "The email and password combination entered do not match a record in our database")   
    return redirect ('/')
    

def wall(request):
    if 'user_id' not in request.session:
        return redirect("/")
    else:
        data = {
            "pies" : Pie.objects.all()
        }
        return render(request, "login/wall.html",data)

def craetePie(request):
    name_pie = request.POST['name']
    filling_pie = request.POST['filling']
    crust_pie = request.POST['crust']
    user =  User.objects.get(id=request.session['user_id'])
    Pie.objects.create(name=name_pie,filling=filling_pie,crust=crust_pie,user=user)
    return redirect('/wall')

def edit(request,uid):
    data = {
        "pie" : Pie.objects.get(id=uid)
    }
    return render(request,"login/edit.html",data)

def update(request,uid):
    pie_to_update= Pie.objects.get(id=uid)
    pie_to_update.name = request.POST['name']
    pie_to_update.filling = request.POST['filling']
    pie_to_update.crust = request.POST['crust']
    pie_to_update.save()
    return redirect('/wall')


def delete(request,uid):
    pie_deleted = Pie.objects.get(id=uid)
    pie_deleted.delete()
    return redirect('/wall')
def pieDerby(request):
    data = {
        "pies" : Pie.objects.all
    }
    return render(request,"login/pieDerby.html",data)

def votePie(request,uid):
    data ={
        "user" : User.objects.get(id=request.session['user_id']),
        "pie" : Pie.objects.get(id=uid)
    }
    return render(request,"login/pageVote.html",data)

def addVote(request,uid):
    user_voted= User.objects.get(id = request.session['user_id'])
    pie = Pie.objects.get(id=uid)
    pie.vote.add(user_voted)
    pie.save()
    return redirect('/pie-derby')
   
def unvote(request,uid):
    user_voted= User.objects.get(id = request.session['user_id'])
    pie = Pie.objects.get(id=uid)
    pie.vote.remove(user_voted)
    pie.save()
    return redirect('/pie-derby')
def logout(request):
    request.session.clear()
    return redirect("/")