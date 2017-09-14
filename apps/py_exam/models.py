from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime

pass_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = []

        if len(post_data['first_name']) < 1 or len(post_data['last_name']) < 1:
            errors.append("First and Last Name fields cannot be empty")
        if not post_data['last_name'].isalpha or not post_data['last_name'].isalpha:
            errors.append("First and Last Name must only include letters")
        if len(post_data['username']) < 1:
            errors.append("Username field cannot be empty")
        if len(User.objects.filter(username = post_data['username'])) > 0:
            errors.append("Username already exists. Please try another username.")
        if len(post_data['email']) < 1:
            errors.append("Email field cannot be empty")
        if len(User.objects.filter(email = post_data['email'])) > 0:
            errors.append("Email address already exists. Please login if you are a returning User.")
        if not email_regex.match(post_data['email']):
            errors.append("Email address format is not valid")
        if len(post_data['dob']) < 1:
            errors.append("Date of Birth field cannot be empty")
        if not pass_regex.match(post_data['pw']):
            errors.append("Password format is not valid")
        if not post_data['pw'] == post_data['pw_confirm']:
            errors.append("Passwords do not match")
        
        if not errors:
            hashed = bcrypt.hashpw(post_data['pw'].encode(), bcrypt.gensalt(5))
            user = User(
                first_name = post_data['first_name'],
                last_name = post_data['last_name'],
                username = post_data['username'],
                email = post_data['email'],
                DOB = post_data['dob'],
                password = hashed
            )
            user.save()
            return user
        else:
            return errors

    def login_validator(self, post_data):
        errors = []

        if len(self.filter(username = post_data['username'])) > 0:
            user = self.filter(username = post_data['username'])[0]
            if not bcrypt.checkpw(post_data['pw'].encode(), user.password.encode()):
                errors.append("Password is not valid")
        else:
            errors.append("Username is not valid")

        if errors:
            return errors
        else:
            return user

class QuoteManager(models.Manager):
    def quote_validator(self, post_data):
        errors = []

        if len(post_data['author']) < 1:
            errors.append("Author field cannot be empty")
        if len(post_data['quote']) < 1:
            errors.append("Quote field cannot be empty")
        
        if not errors:
            if len(Author.objects.filter(name = post_data['author'])) > 0:
                author = Author.objects.filter(name = post_data['author'])[0]
                print author
            else:
                author = Author(
                    name = post_data['author']
                )
                author.save()
                print author
            user = User.objects.get(id=post_data['user_id'])
            quote = Quote(
                quote = post_data['quote'],
                author = author,
                posted_by = user
            )
            quote.save()
            print quote

            if 'add_favs' in post_data:
                quote.favorites.add(user)

        else:
            print errors

    def others_favorites(self, user_id):
        quotes = (self.exclude(favorites__id=user_id).order_by("-created_at"), self.filter(favorites__id=user_id).order_by("-created_at"))
        return quotes

    def remove_favorite(self, quote_id, user_id):
        quote = self.get(id=quote_id)
        user = User.objects.get(id=user_id)
        quote.favorites.remove(user)

    def add_favorite(self, quote_id, user_id):
        quote = self.get(id=quote_id)
        user = User.objects.get(id=user_id)
        quote.favorites.add(user)

    def posts_favs(self, user_id):
        quotes = (self.filter(posted_by__id=user_id).order_by("-created_at"), self.filter(favorites__id=user_id).order_by("-created_at"))
        return quotes

class User(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    DOB = models.DateTimeField()
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):     
        return "%s" % (self.username)

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):     
        return "%s" % (self.name)

class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, related_name="author_quotes")
    posted_by = models.ForeignKey(User, related_name="posted_quotes")
    favorites = models.ManyToManyField(User, related_name="favs_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __str__(self):     
        return "%s %s %s %s" % (self.quote, self.author.name, self.posted_by.username, self.favorites.count())

# class Author(models.Model):
#     name = models.CharField(max_length=128)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):     
#         return "%s" % (self.name)

# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     author = models.ForeignKey(Author, related_name="books")

#     def __str__(self):     
#         return "%s %s %s" % (self.title, self.author.name, self.uploaded_by.username)

# class Review(models.Model):
#     review = models.TextField()
#     rating = models.SmallIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     reviewed_by = models.ForeignKey(User, related_name="user_reviews")
#     book = models.ForeignKey(Book, related_name="book_reviews")
#     objects = ReviewManager()

#     def __str__(self):     
#         return "%s %s %s" % (self.reviewed_by.username, self.book.title, self.review)


# class ReviewManager(models.Manager):
#     def book_review_validator(self, post_data):
#         errors = []
#         print post_data
#         if len(post_data['title']) < 1:
#             errors.append("Title field cannot be empty")
#         if len(post_data['author_new']) < 1 and not 'author_exist' in post_data:
#             errors.append("Must select an existing author or add a new author")
#         if len(post_data['author_new']) > 0 and len(Author.objects.filter(name = post_data['author_new'])) > 0:
#             errors.append("Author already exists in the database. Select from Existing Authors.")
#         if len(post_data['review']) < 1:
#             errors.append("Review field cannot be empty")
        
#         if not errors:
#             if len(post_data['author_new']) > 0:
#                 author = Author(
#                     name = post_data['author_new']
#                 )
#                 author.save()
#             else:
#                 author = Author.objects.filter(name = post_data['author_exist'])[0]
            
#             if len(Book.objects.filter(title = post_data['title'])) > 0:
#                 book = Book.objects.filter(title = post_data['title'])[0]
#             else:
#                 book = Book(
#                     title = post_data['title'],
#                     author = author
#                 )
#                 book.save()

#             user = User.objects.get(id=post_data['user_id'])
#             review = Review(
#                 review = post_data['review'],
#                 rating = post_data['rating'],
#                 reviewed_by = user,
#                 book = book
#             )
#             review.save()
#             return book
#         else:
#             return errors
    
#     def review_validator(self, post_data):
#         errors = []

#         if len(post_data['review']) < 1:
#             errors.append("Review field cannot be empty")
#             return errors
#         else:
#             book = Book.objects.get(id=post_data['book_id'])
#             user = User.objects.get(id=post_data['user_id'])
#             review = Review(
#                 review = post_data['review'],
#                 rating = post_data['rating'],
#                 reviewed_by = user,
#                 book = book
#             )
#             review.save()
        
#     def recent_and_not(self):
#         reviews = (self.all().order_by('-created_at')[:3], self.all().order_by('-created_at')[3:])
#         return reviews