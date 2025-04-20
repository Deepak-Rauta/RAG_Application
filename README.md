# RAG_Application

This app is a Q&A chatbot that can read data from websites and answer questions about it using Google's Gemini Pro model.

Let’s break it down:

🔎 1. Reads Content from URLs

You give it a list of URLs (like website pages), and it:

Fetches the full text content from each URL

Removes HTML and keeps the useful text

For example, it reads text from:

https://www.victoriaonmove.com.au

✂️ 2. Splits the Content into Chunks

Long text is hard for AI models to understand at once.

So the app splits the text into smaller parts (chunks), like paragraphs or 1000-character blocks.

🧠 3. Converts Each Chunk into Vectors (Embeddings)

Each chunk is converted into a vector (a set of numbers) using the Google Generative AI Embedding Model.

This allows the app to:

Remember the meaning of each chunk

Find similar chunks later when a user asks a question

🗃️ 4. Stores Embeddings in a Vector Database (ChromaDB)

These vectors are stored in ChromaDB, a vector store.

This makes it easy to search and retrieve the most relevant chunks later.

❓ 5. User Asks a Question

On the Streamlit page, you can type something like:

"What is Victoria on Move?"

🔍 6. Finds the Most Relevant Chunks

It uses your question to search the ChromaDB for the most relevant chunks (like paragraphs) related to your question.

🤖 7. Uses Gemini Pro to Answer the Question

Now, it sends the relevant chunks + your question to Gemini Pro, which:

Reads the context

Understands your question

Gives a smart, short, and accurate answer

💬 8. Displays the Answer

Finally, the app shows the answer in the Streamlit web app!

Example output:

“Victoria on Move is an Australian brand focused on urban fashion and practical design.”

✅ Why is this Useful?

You can use this to build:

Chatbots that answer FAQs based on websites or documents

Internal document Q&A tools

Custom AI assistants trained on your own data
