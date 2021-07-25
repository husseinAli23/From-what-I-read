from django.shortcuts import render , HttpResponse , redirect
from django.http import JsonResponse
from datetime import datetime
from .models import Book , Profile , Comment , Rating
from .forms import BookForm, UserForm , Profile , CommentForm, RegisterForm, ProfileForm , SettingForm , PasswordChangeingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm ,  PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.urls import path ,reverse_lazy, include


# Create your views here.

# Get to HOME page
def home(request):
    # book= Book.objects.all()
    return render(request, 'home.html')

def signin(request):
    return render(request,"user/signin.html")

def search_by_type(request,mtype):
    book= Book.objects.filter(book_type=mtype)
    return render(request, 'book/searchbytype.html', {'books': book} ) 


#profile
def profile(request,pk):    
    profile = Profile.objects.get(pk=pk)

    return render(request , 'profile/profile_show.html',{'profile':profile} )

def Profile_edit(request,pk):
    profile_edit = Profile.objects.get(pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile_edit)
        if form.is_valid():
            profile_edit = form.save()
            messages.add_message(request , messages.SUCCESS , "Update profile successfully")
            return redirect('profile', pk=profile_edit.pk)
    else:
        form = ProfileForm(instance=profile_edit)
    return render(request, 'profile/profile_edit.html', {'form': form})




# ------------------------------ book route ----------------------------
# To display all the books
def books(request):
    all_books = Book.objects.all()
    horrorBook= Book.objects.filter(book_type="horror")
    actionBook= Book.objects.filter(book_type="action")
    return render(request , 'book/index.html', {"all_books" : all_books, 'horrorBook': horrorBook, 'actionBook': actionBook})

# To view a selector book
def view_book(request, pk):
 
    total= 0
    count1=0
    count2=0
    count3=0
    count4=0
    count5=0
    id_ = pk
    rate= Rating.objects.filter(book=pk)
    if rate.count() == 0:
        total=1
    else: 
        total=rate.count()
    for rete in rate:
        if rete.score == 1:
            count1 += 1
        if rete.score == 2:
            count2 += 1
        if rete.score == 3:
            count3 += 1
        if rete.score == 4:
            count4 += 1
        if rete.score == 5:
            count5 += 1
    # count1=count1/total*100
    # count2=count2/total*100
    # count3=count3/total*100
    # count4=count4/total*100
    # count5=count5/total*100
    try:
        one_book = Book.objects.get(pk=pk)
    except Exception:
        return HttpResponse("error")

    return render(request , 'book/view.html', {"book" : one_book, "count1" : count1, "count2" : count2, "count3" : count3 , "count4" : count4, "count5" : count5})


def show_books(request):
    book= Book.objects.all()
    
    return render(request, 'home.html', {'all_book': book} ) 

# To add a new book
@login_required()
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request , messages.SUCCESS , "Update book successfully")
            return redirect('/book/')
    else:
        if request.user.profile.user_status:
            form = BookForm()
            return render(request , 'book/book_form.html', {'form': form})
        else:
            return redirect('/home/')

# To Update the book
@login_required()
def edit_book(request,pk):
    edit_book= Book.objects.get(pk=pk)
    form = BookForm(instance=edit_book)
    if (request.method == "POST"):
        Edit_book =BookForm(request.POST,instance=edit_book) 
        if Edit_book.is_valid() :
            Edit_book.save()
            messages.add_message(request , messages.SUCCESS , "Added book successfully")
            return redirect (f'/book/{pk}')
    return render(request , 'book/book_form.html' , {"form" : form})

# To Delete the book
@login_required()
def delete_book(request , pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    messages.add_message(request , messages.SUCCESS , "Deleted book successfully")
    return redirect('/book/')

# Add a book to a favoriate list
@login_required()
def favorite_book(request , pk):
    user = User.objects.get(pk = request.user.id)
    book = Book.objects.get(pk=pk)
    print(user.profile.fav_books.all)
    if book in user.profile.fav_books.all():
        user.profile.fav_books.remove(book)
    else:
        user.profile.fav_books.add(book)

    request.user = user
    print( user.profile.fav_books.all())
    return redirect(f'/book/{pk}/')

# Add a book to a wantToRead
@login_required()
def wantToRead(request , pk):
    user = User.objects.get(pk = request.user.id)
    book = Book.objects.get(pk=pk)
    if book in user.profile.wantToRead.all():
        user.profile.wantToRead.remove(book)
    else:
        user.profile.wantToRead.add(book)
    request.user = user
    print( user.profile.wantToRead.all())
    return redirect(f'/book/{pk}/')
    
#----------------------- Auth ----------------------------------
def singin(request):
    messages.add_message(request , messages.SUCCESS , "Login successfully")
    return render(request,"user/singin.html")

def register(request):
    form = RegisterForm()
    if( request.method == "POST"):
        user = RegisterForm(request.POST)
        if(user.is_valid()):
            user.save()
            messages.add_message(request , messages.SUCCESS , "Register successfully")
            return redirect('/home/')
        else:
            form = user
            messages.add_message(request, messages.ERROR, 'Register failure')
    return render(request, "user/register.html", { "form": form })


class PasswordChangeView(PasswordChangeView):
    from_class= PasswordChangeingForm
    success_url=reverse_lazy('password_change_success')

def PasswordChangeDone(request):
        return render(request,"auth/password_change_done.html")

#----------------------- profile ----------------------------------
#show profile 
def profile(request,pk):    
    profile = Profile.objects.get(pk=pk)

    return render(request , 'profile/profile_show.html',{'profile':profile} )

#Edit profile 
@login_required()
def Profile_edit(request,pk):
    profile_edit = Profile.objects.get(pk=pk)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES,instance=profile_edit)
        if form.is_valid():
            profile_edit = form.save()
            messages.add_message(request , messages.SUCCESS , "Update profile successfully")
            return redirect('profile', pk=profile_edit.pk)
    else:
        form = ProfileForm(instance=profile_edit)
    return render(request, 'profile/profile_edit.html', {'form': form})




@login_required()
def Setting(request,pk):
    if request.method == "POST":
        form = SettingForm(request.POST, instance=request.user)
        if form.is_valid():
            profile_Setting = form.save()
            return redirect('profile', pk=request.user.id)
    else:
        form = SettingForm(instance=request.user)
    return render(request, 'profile/setting.html', {'form': form})

# To add a new cooment
@login_required()
def add_comment(request,pk):
    book1=Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment = Comment.objects.create(
                user =request.user,
                name=comment.name,
                comment=comment.comment,
                )
            comment.book.add(book1)
            comment.save()
            return redirect(f'/book/{pk}/')
    else:
        form = CommentForm()
        """ messages.add_message(request, messages.WARNING,  "Failed to add your comment") """

    return render(request , 'comment/add_comment.html', {'form': form})

#To edit the comment
@login_required()
def edit_comment(request,pk,pkb):
    edit_comment= Comment.objects.get(pk=pk)
    if edit_comment.user == request.user:
        form = CommentForm(instance=edit_comment)
        if (request.method == "POST"):
            Edit_comment =CommentForm(request.POST,instance=edit_comment) 
            if Edit_comment.is_valid() :
                Edit_comment.save()
                return redirect (f'/book/{pkb}')
        else:
            return render(request , 'comment/add_comment.html' , {"form" : form})
    else: 
        html = "<h1>you can't do it </h1>" 
        return HttpResponse(html)

# To Delete the comment
@login_required()
def delete_comment(request , pk):
    comment = Comment.objects.get(pk=pk)
    if comment.user == request.user:
        comment.delete()
        messages.add_message(request , messages.SUCCESS , "The comment deleted successfully")
        return redirect('home')
    else: 
        messages.add_message(request, messages.WARNING,  "Failed to add your comment")


def Search(request):
    book= Book.objects.all()
    query = request.GET.get("q")
    if query:
        book = Book.objects.filter(Q(name__icontains=query) )

    return render(request,'book/Search.html',{'all_books': book})

# To add a new reting for a book
@login_required()
def add_rate(request,pk):
    book1=Book.objects.get(pk=pk)
    val = request.POST['rate']
    print ("rate : "+request.POST['rate'])
    print ("----------------------------")
    print ( request.user)

    if request.method == 'POST':
        rate = Rating.objects.create(
                user =request.user,
                book=book1,
                score  =  request.POST['rate']
                )
        rate.save()
        messages.add_message(request , messages.SUCCESS , "Added your rating successfully")
        return redirect(f'/book/{pk}/')
    messages.add_message(request , messages.WARNING,"There is an error please try again")
    return redirect(f'/book/{pk}/')


