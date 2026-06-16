import math

from django.core.management import call_command
from django.test import TestCase

from .embedding import cosine_similarity, embed_text


class EmbeddingTests(TestCase):
    def test_embeddings_are_normalized_model_vectors(self):
        vector = embed_text("python django database search")

        self.assertGreater(len(vector), 100)
        self.assertAlmostEqual(
            math.sqrt(sum(value * value for value in vector)),
            1.0,
            places=3,
        )

    def test_similar_text_has_higher_cosine_than_unrelated_text(self):
        query = embed_text("python django database search")
        programming = embed_text("django app vector database")
        dinner = embed_text("tomato pasta dinner")

        self.assertGreater(
            cosine_similarity(query, programming),
            cosine_similarity(query, dinner),
        )


class SearchViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo_data", verbosity=0)

    def test_programming_query_ranks_django_document_first(self):
        response = self.client.get("/", {"q": "python django database search"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["results"][0]["document"].title,
            "Django Vector Search",
        )
        self.assertContains(response, "Django Vector Search")

    def test_empty_page_shows_seed_rows(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fresh Tomato Pasta")
        self.assertContains(response, "Rainy Day Forecast")
