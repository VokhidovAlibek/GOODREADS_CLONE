from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='Alibek', first_name="Alibek")
        self.user.set_password('somepass')
        self.user.save()
        self.client.login(username='Alibek', password= 'somepass')

    def test_book_review_detail(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123123123")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very nice book!")

        response = self.client.get(reverse('api:review-detail', kwargs={'id':br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Very nice book!")

        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Book1')
        self.assertEqual(response.data['book']['description'], 'Description1')
        self.assertEqual(response.data['book']['isbn'], "123123123")

        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['username'], 'Alibek')
        self.assertEqual(response.data['user']['first_name'], 'Alibek')

    def test_delete_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123123123")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very nice book!")

        response = self.client.delete(reverse('api:review-detail', kwargs={"id": br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123123123")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.patch(reverse("api:review-detail", kwargs={'id':br.id}), data={'stars_given':4})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)

    def test_put_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123123123")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.patch(reverse("api:review-detail", kwargs={'id': br.id}),
                                     data={
                                         'stars_given': 4,
                                         'comment': 'nice book',
                                         'book_id': book.id,
                                         'user_id': self.user.id
                                     })
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'nice book')

    def test_create_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123123123")
        data = {
            'stars_given': 4,
            'comment': 'nice book',
            'book_id': book.id,
            'user_id': self.user.id
        }

        response = self.client.post(reverse("api:review-list"), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment,'nice book')



    def test_book_review_list(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123123123")
        user_two = CustomUser.objects.create(username='Asom', first_name="Asomiddin")
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very nice book!")
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=4, comment="Not bad book!")

        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(response.data['count'], 2)

        self.assertEqual(response.data['results'][1]['id'], br.id)
        self.assertEqual(response.data['results'][1]['book']['title'], "Book1")
        self.assertEqual(response.data['results'][1]['stars_given'], 5)
        self.assertEqual(response.data['results'][1]['comment'], 'Very nice book!')

        self.assertEqual(response.data['results'][0]['stars_given'], 4)
        self.assertEqual(response.data['results'][0]['comment'], "Not bad book!")
        self.assertEqual(response.data['results'][0]['id'], br_two.id)




