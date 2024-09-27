# QA Bot: FAQ

This repository demonstrates how to use Pinecone and OpenAI to create a question-answering bot (FAQ bot) using a RAG (Retrieval-Augmented Generation) model. It leverages Pinecone for vector similarity search and OpenAI's GPT for generating responses based on retrieved contexts. Sentence embeddings are generated using the `SentenceTransformer` model.

## Prerequisites

Before running the notebook, you need to install the required libraries:

```bash
!pip install sentence-transformers
!pip install pinecone-client
!pip install openai
```

## Environment Setup

- Pinecone API Key: Create a Pinecone account and get your API key from the dashboard.
- OpenAI API Key: Create an OpenAI account and get your API key.

## Pinecone Setup

- Create a Pinecone Index: We create an index named qabots with 768 dimensions to store the vector embeddings of documents. The metric used for similarity search is Euclidean distance.

    ```python
    from pinecone import Pinecone, ServerlessSpec

    pc = Pinecone(api_key="YOUR_PINECONE_API_KEY")
    pc.create_index(
        name="qabots",
        dimension=768,
        metric="euclidean",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    ```
- Sentence Embedding Generation: The bert-base-nli-mean-tokens model from sentence-transformers is used to generate vector embeddings for predefined documents.

    ```python
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer('bert-base-nli-mean-tokens')
    documents = [
        "Welcome to Our Business! Here you will find information about our products and services.",
        "FAQs:\nQ: What are your business hours?\nA: We are open from 9 AM to 5 PM, Monday to Friday.",
        "Product A:\nProduct A is our flagship product designed to help businesses streamline their operations.",
        "Product B:\nProduct B is a software solution aimed at enhancing customer engagement.",
        "Contact Us:\nFor any inquiries, please contact our customer service team at contact@business.com."
    ]

    index = pc.Index("qabots")
    res = []
    for i, doc in enumerate(documents):
        embedding = model.encode(doc)
        res.append({"id": str(i), "values": embedding.tolist()})

    index.upsert(vectors=res)
    ```

# OpenAI GPT Integration (RAG Model)

To answer questions, we retrieve relevant documents using Pinecone, pass them as context to OpenAI's GPT model, and generate answers.

- OpenAI Setup: Initialize OpenAI with your API key.

- Querying Pinecone and Generating Answers: The bot first retrieves top-k documents from Pinecone based on the similarity of the query embedding, then passes the retrieved context to OpenAI to generate an answer.

# Project Workflow

* Set up the Pinecone index to store document embeddings.
* Use Sentence-Transformers to generate vector embeddings for your dataset.
* Store these embeddings in Pinecone.
* Query Pinecone with a user question to retrieve the top-k most relevant documents.
* Use OpenAI GPT to generate a response based on the context of the retrieved documents.

# Dependencies

```
Python 3.10
sentence-transformers
pinecone-client
openai
```


