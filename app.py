from flask import Flask, render_template, request
import os
from main import retrieve_documents

app = Flask(__name__)

folder_path = 'C:/Users/Envy/OneDrive/Desktop/Article'  

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']  # Get query from the form input
        ranked_results = retrieve_documents(folder_path, query)  # Retrieve documents based on the query
        return render_template('index.html', results=ranked_results, query=query)  # Pass the results to the template

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
