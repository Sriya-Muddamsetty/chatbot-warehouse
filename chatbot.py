from flask import Flask, render_template, request, jsonify
import sqlite3
import re
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")


# Function to fetch order status from the database
def fetch_order_status(order_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Query to fetch order status
    cursor.execute('SELECT status FROM orders WHERE order_id = ?', (order_id,))
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    if result:
        return f"The status of your order {order_id} is: {result[0]}"
    else:
        return f"Order ID {order_id} not found in our system."


# Response generator with NLP
def generate_response(message):
    doc = nlp(message.lower())
    lemmas = [token.lemma_ for token in doc]

    # Check for valid order ID format like ORD123
    match = re.search(r"\bORD\d+\b", message.upper())
    if match:
        return fetch_order_status(match.group())

    # Respond to greetings
    if any(word in lemmas for word in ["hi", "hello", "hey"]):
        return "Hello! 👋 How can I assist you with your order today?"

    # Asking how to order
    elif any(word in lemmas for word in ["order", "buy", "purchase"]) and any(
            word in lemmas for word in ["how", "want", "place"]):
        return "To place an order, browse products, add items to your cart, and click 'Checkout'."

    # Delivery time
    elif any(word in lemmas for word in ["delivery", "arrive", "receive", "ship", "reach"]):
        return "Delivery usually takes 3 to 5 business days depending on your location."

    # Cancel order
    elif "cancel" in lemmas:
        return "To cancel your order, please provide your order ID (e.g., ORD123)."

    # Check status
    elif any(word in lemmas for word in ["status", "track", "where"]):
        return "Sure! Please provide your order ID (e.g., ORD123) to check the current status."

    # Help
    elif any(word in lemmas for word in ["help", "can", "do"]):
        return "I can help you place orders, check order status, cancel orders, and answer delivery-related questions."

    # Default fallback
    else:
        return (
            "I'm not sure I understood that. Try asking things like:\n"
            "- How can I place an order?\n"
            "- What's the delivery time?\n"
            "- Cancel my order\n"
            "- Track order ORD123"
        )


# Home route
@app.route("/")
def index():
    return render_template("index.html")


# Chat endpoint
@app.route("/index", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = generate_response(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
