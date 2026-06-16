# Vector Search Django Demo

A small Django application that demonstrates how vector search ranks text rows by
similarity score.

The app stores a handful of SQLite rows with embeddings from a real Hugging Face
model. A user enters query text, the app embeds that text with the same model,
computes cosine similarity against each stored row, and shows the top matches in
score order.

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Then open http://127.0.0.1:8000/.

## Useful commands

```bash
python manage.py seed_demo_data
python manage.py test
```

`migrate` creates the demo rows. `seed_demo_data` downloads
`BAAI/bge-small-en-v1.5` from Hugging Face into `.hf_cache/`, embeds the rows,
and stores those vectors in SQLite.

## What it demonstrates

- Documents are stored with an embedding vector in `SearchDocument.embedding`.
- Query text is converted into the same Hugging Face vector space in
  `search/embedding.py`.
- Results are ranked by cosine similarity in `search/views.py`.
- The UI shows both the score and the vector weights so the ranking is visible.
