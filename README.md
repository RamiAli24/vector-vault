# Vectors Vault

Semantic search API powered by vector embeddings. Query "stone" and find "rock" - understands meaning, not just keywords.

## Features

-   **Semantic Search**: Natural language queries with contextual understanding
-   **Vector Embeddings**: distiluse-base-multilingual-cased-v1 multilingual model for accurate results
-   **PostgreSQL + pgvector**: Efficient vector storage and retrieval

## Quick Start

First install [Poetry](https://python-poetry.org)

```bash
# Install dependencies
make install

# Run migrations and start server
make migrate
make run-server
```

## API Usage

**Search Books:**

```http
GET /api/names/?title=adventure novel
```

**Add Book:**

```http
POST /api/names/
Content-Type: application/json

{"title": "The Great Gatsby"}
```
