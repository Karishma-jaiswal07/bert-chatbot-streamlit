# bert-chatbot-streamlit
# BERT Chatbot with Streamlit

A BERT-powered chatbot built using Streamlit, Hugging Face Transformers, and PyTorch. This application leverages pre-trained BERT embeddings to understand user queries and generate responses based on a set of predefined Q&A pairs. It also features a custom background image for an enhanced user experience.

## Features

- **BERT-Based NLP:** Uses the `bert-base-uncased` model for text tokenization and embedding generation.
- **Cosine Similarity:** Compares user input with predefined questions to determine the most relevant response.
- **Customizable Interface:** Built with Streamlit and enhanced with custom CSS for a visually appealing background.
- **Precomputed Embeddings:** Improves performance by calculating embeddings for fixed Q&A pairs once during startup.
- **Interactive Chat:** Users can type queries and receive context-aware responses instantly.

## Technologies Used

- **Python**
- **Streamlit:** For creating the interactive web application.
- **PyTorch:** To run the BERT model.
- **Hugging Face Transformers:** Provides the pre-trained BERT model and tokenizer.
- **Scikit-Learn:** For computing cosine similarity between embeddings.
- **Base64:** Used for embedding the background image in CSS.


