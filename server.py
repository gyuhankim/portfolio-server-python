from flask import Flask, jsonify, request #import objects from the Flask model
from flask_pymongo import PyMongo

# look into postgreSQL
# SQLalchemy -> ORM

app = Flask(__name__) #define app using Flask
# app.config['JSON_SORT_KEYS'] = False #prevents Flask from sorting data (not recommended)
app.config['MONGO_DBNAME'] = 'portfolio_blog'
app.config['MONGO_URI'] = ''

mongo = PyMongo(app)

@app.route('/api/posts', methods=['GET'])
def getPosts():
  blog = mongo.db.blog

  output = []

  for q in blog.find():
    output.append(
      {
        '_id' : str(q['_id']),
        'title' : q['title'], 
        'date' : q['date'], 
        'body' : q['body']
      }
    )
  
  return jsonify(output)

@app.route('/api/posts', methods=['POST'])
def newPost():
  blog = mongo.db.blog
  post = request.json
  postID = blog.insert(post) # PyMongo returns the _id of the new document
  
  return jsonify('Posted successfully with ID of {}'.format(postID))

@app.route('/api/posts/<string:id>', methods=['DELETE'])
def deletePost(id):
  blog = mongo.db.blog
  blog.delete_one({'_id' : id})

  return jsonify('Successfully deleted post with ID of {}'.format(id))

if __name__ == '__main__':
  app.run(debug=True, port=8080)