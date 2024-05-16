from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output
from content_filtering import get_recommendations

articles_data = pd.read_csv('articles.csv')
all_articles = articles_data[['url' , 'title' , 'text' , 'lang' , 'total_events']]
liked_articles = []
not_liked_articles = []

app = Flask(__name__)

def assign_val():
    m_data = {
        "url": all_articles.iloc[0,0],
        "title": all_articles.iloc[0,1],
        "text": all_articles.iloc[0,2] or "N/A",
        "lang": all_articles.iloc[0,3],
        "total_events": all_articles.iloc[0,4]/2
    }
    return m_data

@app.route("/get-article")
def get_article():

    article_info = assign_val()
    return jsonify({
        "data": article_info,
        "status": "success"
    })

@app.route("/liked-article")
def liked_article():
    global all_articles
    article_info = assign_val()
    liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/unliked-article")
def unliked_article():
    global all_articles
    article_info = assign_val()
    not_liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# API to return most popular articles.
@app.route("/popular-articles")
def popular_articles():
    popular_article_data = []
    for index,row in output.iterrows():
        p = {
            'url' : row["url"],
            'title' : row["title"],
            'text' : row["text"],
            'lang' : row["lang"],
            'total_events' : row["total_events"]
        } 

        popular_article_data.append(p)

    return jsonify({
        "data" : popular_article_data.head(20),
        "success": "success"
    })
    
    # return "Top 20 articles using demographic filtering method" 

# API to return top 10 similar articles using content based filtering method.
@app.route("/recommended-articles")
def recommended_articles():
    global all_articles
    colmn_names = ["url", "title", "text", "lang", "total_events"]
    all_recommended = pd.DataFrame(columns = colmn_names)
    for i in all_articles:
        output = get_recommendations(i["original_title"])
        all_recommended = all_recommended.append(output)

    all_recommended.drop_duplicates(subset = ["url"], inplace = True)
    recommended_article_data = []
    for index,row in all_recommended.iterrows():
        p = {
             'url' : row["url"],
            'title' : row["title"],
            'text' : row["text"],
            'lang' : row["lang"],
            'total_events' : row["total_events"]
        } 

        recommended_article_data.append(p)

    return jsonify({
        "data" : recommended_article_data,
        "state" :"success"
    })
    
    return "Top 10 articles using content based filtering method"

if __name__ == "__main__":
    app.run()