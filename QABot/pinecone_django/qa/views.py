from django.shortcuts import render
from django.http import JsonResponse
import os
import pinecone
from sentence_transformers import SentenceTransformer
import openai

# Initialize Pinecone
pinecone.init(api_key=os.getenv('PINECONE_API_KEY'))
index = pinecone.Index("qabots")

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize Sentence Transformer model
model = SentenceTransformer('bert-base-nli-mean-tokens')

# Predefined documents
documents = [
    "Welcome to Our Business! Here you will find information about our products and services.",
    "FAQs:\nQ: What are your business hours?\nA: We are open from 9 AM to 5 PM, Monday to Friday.",
    "Product A:\nProduct A is our flagship product designed to help businesses streamline their operations.",
    "Product B:\nProduct B is a software solution aimed at enhancing customer engagement.",
    "Contact Us:\nFor any inquiries, please contact our customer service team at contact@business.com."
]

# View for the homepage
def home(request):
    return render(request, 'qa/index.html')

# View to handle question queries
def ask_question(request):
    if request.method == 'POST':
        question = request.POST.get('question')

        # Encode the question using Sentence Transformer
        query_embedding = model.encode(question).tolist()

        # Retrieve relevant documents from Pinecone
        results = index.query(vector=query_embedding, top_k=3, include_values=True)
        if not results or not results.items:
            return JsonResponse({"answer": "Sorry, I couldn't find any relevant information to answer your question."})

        doc_ids = [result['id'] for result in results['matches']]
        retrieved_documents = [documents[int(doc_id)] for doc_id in doc_ids]

        # Generate context for OpenAI
        context = "\n\n".join(retrieved_documents)
        input_text = f"Question: {question}\nContext: {context}\nAnswer:"

        # Call OpenAI to generate an answer
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=input_text,
            max_tokens=50
        )

        answer = response['choices'][0]['text'].strip()

        return JsonResponse({"answer": answer})

    return JsonResponse({"error": "Invalid request method."})

