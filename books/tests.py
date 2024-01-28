from django.test import TestCase
from django.urls import reverse

from books.models import Book, Author, BookAuthor
from users.models import CustomUser


# Create your tests here.

class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="123123123")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="222222222")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="333333333")

        response = self.client.get(reverse("books:list")+"?page_size=2")

        books = Book.objects.all()
        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list")+"?page=2")

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123123123")
        author = Author.objects.create(first_name="Agata", last_name='Christie', bio="Author of the book 'Puaro'")
        book_author = BookAuthor.objects.create(book=book, author=author)

        response = self.client.get(reverse("books:detail", kwargs={'pk':book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, author.first_name)
        self.assertContains(response, author.last_name)

    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="Description1", isbn="123123123")
        book2 = Book.objects.create(title="Detective", description="Description2", isbn="222222222")
        book3 = Book.objects.create(title="Drama", description="Description3", isbn="333333333")

        response = self.client.get(reverse("books:list")+"?q=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=detective")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=drama")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='Book1', description="Description", isbn='1234567890')
        user = CustomUser.objects.create(
            username='avokhidov',
            first_name='Alibek',
            last_name='Vokhidov',
            email='avokhidov@mail.com'
        )
        user.set_password('somepass')
        user.save()

        self.client.login(username='avokhidov',password='somepass')

        self.client.post(reverse("books:reviews", kwargs={'id':book.id} ), data={
            'stars_given': 3,
            'comment': "Nice book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book )