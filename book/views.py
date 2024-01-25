from django.shortcuts import render ,redirect
from django.views.generic import View
from book.forms import BookForm,RegistrationForm,LoginForm
from book.models import Books
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs) 
    return wrapper           
@method_decorator(signin_required,name="dispatch")
class BookListView(View):
    def get(self,request,*args,**kwargs):
        qs=Books.objects.all()
 
        if "price_lt" in request.GET:
            amount=request.GET.get("price_lt")
            qs=qs.filter(price__lte=amount)
        if "price_gt" in request.GET:
            amount=request.GET.get("price_gt")  
            qs=qs.filter(price__gte=amount) 
        return render(request,"book_list.html",{"data":qs})
@method_decorator(signin_required,name="dispatch")
class BookDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)
        return render(request,"book_detail.html",{"data":qs})    
    
#localhost:8000/books/{id}/remove
@method_decorator(signin_required,name="dispatch")
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")  
        Books.objects.get(id=id).delete() 
        messages.success(request,"book deleted successfully")
        return redirect("book-all")
@method_decorator(signin_required,name="dispatch")        
class BookCreateView(View):
    def get(self,request,*args,**kwargs):
        form=BookForm()
        return render(request,"book_add.html",{"form":form})    
    def post(self,request,*args,**kwargs):
        form=BookForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"book created successfully")
            return redirect("book-all")
        else:
            messages.error(request,"failed to create book")
            return render(request,"book_add.html",{"form":form})
@method_decorator(signin_required,name="dispatch")
class BookUpdateView(View):
    def get (self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookForm(instance=obj)
        return render(request,"book_edit.html",{"form":form}) 
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"book updated successfully")
            return redirect("book-all")
        else:
            messages.error(request,"failed to update the book")
            return render(request,"book_edit.html",{"form":form})
        
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})        
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            #form.save()
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"account has been created successfully")
            return redirect("signin")
        else:
            messages.error(request,"failed to create the account")
            return render(request,"register.html",{"form":form})  

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})   
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                print("valid credentials")
                login(request,user_object)
                print(request.user)
                return redirect("book-all")
            else:
                print("invalid credentials")    

                return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})
@method_decorator(signin_required,name="dispatch")
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")




