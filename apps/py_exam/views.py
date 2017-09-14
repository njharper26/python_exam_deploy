from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

def index(request):
    return render(request, 'py_exam/index.html')

def process_register(request):
    result = User.objects.register_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    else:
        messages.success(request, "Congrats, you have successfully registered!")
        request.session['id'] = result.id
        return redirect('/success')

def process_login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    else:
        messages.success(request, "You have successfully logged in.")
        request.session['id'] = result.id
        return redirect('/success')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

def success(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
    }
    return render(request, 'py_exam/success.html', context)

def quotes_dashboard(request):
    quotes = Quote.objects.others_favorites(request.session['id'])
    context = {
        'user': User.objects.get(id=request.session['id']),
        'others': quotes[0],
        'favorites': quotes[1]
    }
    print context
    return render(request, 'py_exam/dashboard.html', context)

def proccess_add_quote(request):
    result = Quote.objects.quote_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/quotes')
    else:
        messages.success(request, "New quote posted successfully!")
        return redirect('/quotes')

def proccess_add_favorite(request, id):
    Quote.objects.add_favorite(id, request.session['id'])
    return redirect('/quotes')

def proccess_remove_favorite(request, id):
    Quote.objects.remove_favorite(id, request.session['id'])
    return redirect('/quotes')

def user_profile(request, id):
    quotes = Quote.objects.posts_favs(id)
    context = {
        'user': User.objects.get(id=id),
        'posts': quotes[0],
        'favs': quotes[1],
        'p': quotes[0].count(),
        'f': quotes[1].count()
    }
    return render(request, 'py_exam/user_profile.html', context)










# def add(request):
#     context = {
#         'authors': Author.objects.all()
#     }
#     return render(request, 'py_exam/add.html', context)

# def process_add_book_review(request):
#     result = Review.objects.book_review_validator(request.POST)
#     if type(result) == list:
#         for error in result:
#             messages.error(request, error)
#         return redirect('/books/add')
#     else:
#         messages.success(request, "You successfully added a review!")
#         id = result.id
#         return redirect('/books/' + str(id))

# def process_review(request, id):
#     result = Review.objects.review_validator(request.POST)
#     if type(result) == list:
#         for error in result:
#             messages.error(request, error)
#         return redirect('/books/' + str(id))
#     else:
#         messages.success(request, "You successfully added a review!")
#         return redirect('/books/' + str(id))

# def book(request, id):
#     context = {
#         'book': Book.objects.get(id=id),
#         'reviews': Book.objects.get(id=id).book_reviews.all().order_by('-created_at')
#     }
#     return render(request, 'py_exam/book.html', context)

# def user(request, id):
#     user = User.objects.get(id=id)
#     context = {
#         'user': user,
#         'reviews': user.user_reviews.all().order_by('-created_at'),
#         'count': user.user_reviews.count()
#     }
#     return render(request, 'py_exam/user.html', context)