import streamlit as st #For creating the frontend
from transformers import BertTokenizer, BertModel # Both are the classes from the hugging face transformer library.These are used to tokenize text and generate embeddings using the BERT model.
import torch #deep learning framework underlying the BERT model.
from sklearn.metrics.pairwise import cosine_similarity #Imports the cosine_similarity function from scikit-learn to calculate similarity between two vectors (used to compare text embeddings).
import base64 #is used to encode binary data (like images) into text format for embedding in HTML/CSS.


#adding img
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Call the function to set the background
set_background(r"C:\Users\dell\OneDrive\Pictures\istockphoto-1488335095-612x612.jpg")

# Load BERT tokenizer and model
@st.cache_resource #Uses the decorator @st.cache_resource to cache the result so the model loads only once.
def load_bert_model():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased') #Loads the tokenizer for the 'bert-base-uncased' model.
    model = BertModel.from_pretrained('bert-base-uncased') #Loads the corresponding BERT model.
    return tokenizer, model

tokenizer, model = load_bert_model() # Calls load_bert_model and assigns the returned tokenizer and model to variables for later use.

# Predefined questions and responses
qa_pairs = {
    "What is your name?": "I am a chatbot powered by BERT!",
    "How are you?": "I'm just a bunch of code, but I'm doing great!",
    "What is BERT?": "BERT stands for Bidirectional Encoder Representations from Transformers. It’s a powerful NLP model.",
    "Tell me a joke.": "Why don't programmers like nature? It has too many bugs.",
    "what is data science": "Data Science is the study of analyzing data to find useful information. It uses tools like math, statistics, and programming to understand patterns and make predictions. Data scientists work with large amounts of data to solve real-world problems. It's about turning data into smart decisions.",
    "what is your use":"A BERT-based chatbot uses the BERT model to understand and respond to user queries by analyzing the context of the conversation. It can handle tasks like answering questions, providing information, or engaging in dialogue by comparing user inputs with predefined responses or generating replies. BERT's deep understanding of language helps the chatbot give more accurate and context-aware answers.",
    "What is ai":"Artificial Intelligence (AI) is the ability of machines to simulate human intelligence. It enables systems to learn from data, make decisions, and perform tasks like understanding language, recognizing images, or solving problems. AI aims to make machines think and act intelligently.",
    "what is microsoft azure":"Microsoft Azure is a cloud computing platform and service provided by Microsoft. It offers tools and resources for building, deploying, and managing applications and services through Microsoft's global data centers. Azure supports a wide range of services like virtual machines, databases, AI, analytics, and storage, making it a flexible solution for businesses and developers.",
}

# Function to get BERT embeddings
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128) #Tokenizes the input text with appropriate options (returns PyTorch tensors, truncates or pads the sequence to a maximum length of 128).
    with torch.no_grad(): #Uses torch.no_grad() to disable gradient calculations (since we're only doing inference).
        outputs = model(**inputs)  #Passes the tokenized inputs to the BERT model.
    return outputs.last_hidden_state.mean(dim=1).numpy() #Averages the token embeddings from the model’s last hidden layer to create a single vector representation and converts it to a NumPy array.Returns the resulting embedding.

# Precompute embeddings for predefined questions
predefined_embeddings = {question: get_bert_embedding(question) for question in qa_pairs} #Uses a dictionary comprehension to precompute and store embeddings for each predefined question. This improves efficiency by avoiding repeated computation during user interactions.

# Function to get the chatbot's response
def chatbot_response(user_input):
    user_embedding = get_bert_embedding(user_input) #Computes the BERT embedding for the user’s input.
    
    # Compute cosine similarities
    similarities = {
        question: cosine_similarity(user_embedding, predefined_embeddings[question])[0][0]
        for question in qa_pairs
    }
    
    # Find the most similar question
    best_match = max(similarities, key=similarities.get) #Identifies the question with the highest similarity
    
    # Return the response if similarity is high enough
    if similarities[best_match] > 0.5:  # Threshold can be adjusted
        return qa_pairs[best_match]
    else:
        return "I'm not sure how to respond to that."

# Streamlit Frontend
st.title("BERT Chatbot")
st.write("This is a BERT-powered chatbot application with a simple user interface built using Streamlit. It allows users to type queries and receive responses based on a predefined set of questions and answers.")
st.subheader("Ask me anything!")

# User input
user_input = st.text_input("You:", placeholder="Type your message here...")

# Display the response
if user_input:
    response = chatbot_response(user_input)
    st.write(f"**Chatbot:** {response}")

# Footer
st.markdown("---")

