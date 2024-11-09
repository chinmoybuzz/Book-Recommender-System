# from flask import Flask, request, render_template

# import requests
# import numpy as np

# import pandas as pd

# import pickle



# app = Flask(__name__)

# model = pickle.load(open('artifacts/model.pkl','rb'))
# book_names = pickle.load(open('artifacts/book_names.pkl','rb'))
# final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
# book_pivot = pickle.load(open('artifacts/book_pivot.pkl','rb'))



# # function to fetch book poster


# def fetch_poster(suggestion):
#     book_name = []
#     ids_index = []
#     poster_url = []

#     for book_id in suggestion:
#         book_name.append(book_pivot.index[book_id])

#     for name in book_name[0]: 
#         ids = np.where(final_rating['title'] == name)[0][0]
#         ids_index.append(ids)

#     for idx in ids_index:
#         url = final_rating.iloc[idx]['image_url']
#         poster_url.append(url)

#     return poster_url




# # function to get recommended book

# def recommend_book(book_name):
#     books_list = []
#     book_id = np.where(book_pivot.index == book_name)[0][0]
#     distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

#     poster_url = fetch_poster(suggestion)
    
#     for i in range(len(suggestion)):
#             books = book_pivot.index[suggestion[i]]
#             for j in books:
#                 books_list.append(j)
#     return books_list , poster_url       


# # home page

# @app.route('/')

# def home():
#    book_list = book_names.tolist()
#    return render_template('index.html', book_list=book_list)



# # recommendation page

# @app.route('/recommend', methods=['POST'])

# def recommend():
#    book_title = request.form['selected_book']
#    recommended_book_titles, recommended_book_posters = recommend_book(book_title)
#    selected_book = request.form['selected_book']
#    return render_template('index.html', book_list=book_names.tolist(),
#                           recommended_book_titles=recommended_book_titles,
#                           recommended_book_posters=recommended_book_posters,
#                           selected_book=selected_book) 



# if __name__ == '__main__':
#    app.run(debug=True)

from flask import Flask, request, render_template
import requests
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# Load necessary pickle files
model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_names = pickle.load(open('artifacts/book_names.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))


# Function to fetch book posters
def fetch_poster(suggestions):
    poster_url = []
    for book_id in suggestions:
        book_name = book_pivot.index[book_id]
        book_index = np.where(final_rating['title'] == book_name)[0][0]
        url = final_rating.iloc[book_index]['image_url']
        poster_url.append(url)
    return poster_url


# Function to get recommended books
def recommend_book(book_name):
    book_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

    poster_url = fetch_poster(suggestion.flatten())
    
    for book_id in suggestion.flatten():
        book_list.append(book_pivot.index[book_id])
        
    return book_list, poster_url


# Home page route
@app.route('/')
def home():
    book_list = book_names.tolist()
    return render_template('index.html', book_list=book_list)


# Recommendation page route
@app.route('/recommend', methods=['POST'])
def recommend():
    book_title = request.form['selected_book']
    recommended_book_titles, recommended_book_posters = recommend_book(book_title)
    selected_book = request.form['selected_book']
    return render_template('index.html', 
                           book_list=book_names.tolist(),
                           recommended_book_titles=recommended_book_titles,
                           recommended_book_posters=recommended_book_posters,
                           selected_book=selected_book)


if __name__ == '__main__':
    app.run(debug=True)
