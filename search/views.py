from django.shortcuts import render

from .embedding import cosine_similarity, embed_text, get_model_name
from .models import SearchDocument

EXAMPLE_QUERIES = (
    "django database search",
    "rainy weather forecast",
    "pasta dinner with tomatoes",
    "travel budget for a trip",
)


def component_rows(vector, limit=12):
    if not vector:
        return []

    largest_components = sorted(
        enumerate(vector),
        key=lambda item: abs(item[1]),
        reverse=True,
    )[:limit]
    scale = max(abs(value) for index, value in largest_components) or 1

    return [
        {
            "label": f"d{index}",
            "value": value,
            "display": f"{value:+.3f}",
            "direction": "negative" if value < 0 else "positive",
            "percent": round((abs(value) / scale) * 100, 1) if value else 0,
        }
        for index, value in largest_components
    ]


def ensure_document_embedding(document, model_name):
    if document.embedding and document.embedding_model == model_name:
        return document

    document.embedding = embed_text(f"{document.title} {document.body}")
    document.embedding_model = model_name
    document.save(update_fields=["embedding", "embedding_model"])
    return document


def ranked_results(query):
    model_name = get_model_name()
    query_vector = embed_text(query)
    results = []

    for document in SearchDocument.objects.all():
        document = ensure_document_embedding(document, model_name)
        score = cosine_similarity(query_vector, document.embedding)
        results.append(
            {
                "document": document,
                "score": score,
                "score_percent": round(max(score, 0) * 100, 1),
                "components": component_rows(document.embedding),
            }
        )

    results.sort(key=lambda result: result["score"], reverse=True)
    return query_vector, results


def search(request):
    query = request.GET.get("q", "").strip()
    documents = SearchDocument.objects.all()
    query_vector = embed_text(query) if query else []
    results = []

    if query:
        query_vector, results = ranked_results(query)

    first_embedding = next(
        (document.embedding for document in documents if document.embedding),
        [],
    )
    vector_dimensions = len(query_vector) or len(first_embedding) or "pending"

    context = {
        "documents": documents,
        "embedding_model_name": get_model_name(),
        "examples": EXAMPLE_QUERIES,
        "query": query,
        "query_components": component_rows(query_vector),
        "result_count": len(results),
        "results": results[:5],
        "shown_component_count": 12,
        "vector_dimensions": vector_dimensions,
    }
    return render(request, "search/search.html", context)
