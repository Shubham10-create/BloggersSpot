#Flask is a web framework written in python
#Its a microwebframwork which is light weight and it doed not require particular tools or libraries
from flask import Flask, render_template, request, redirect #render_template render the template from the given folder
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)  #calling the flask constructor

#setting up our databases
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db' #helps us to configure where our database is gonna get store
                                      #sqlalchemy_uri is just a pathmto where the database is stored
                                      #/// means relative path, whereas //// means absolute path
db = SQLAlchemy(app) #create a db, db has taken flask app and linked it together

#creating a real database now
class BlogPost(db.Model):   #inherits from db model
    id = db.Column(db.Integer, primary_key = True ) #its means that this id is the main distinguisher between duplicate blogpost
    title = db.Column(db.String(100), nullable = False) #nullable=False means that this field is compulsary, this cannot be empty
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(20), nullable=False, default = 'N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    #prints out whenever we create a new blogpost
    def __repr__(self):
        return 'Blog post'+ str(self.id) 



@app.route('/') #base directory
def index():
    return render_template('index.html') #here the browser can interpret raw text and also html in the browser
                                         #its template so it needs to be in the directory called as templates

@app.route('/posts', methods = ['GET','POST'])
def posts():

    if request.method == 'POST': #reads all the data from the form and sends it to the db
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post) #adds this to the database in this current session
        db.session.commit() #commit it permanent
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all() #reading all the data from db and ordering them by their date_posted and sending them back to our frontend window
        return render_template('posts.html', posts = all_posts) #well have the access of all the data in the var all_posts

@app.route('/AboutUs')
def AboutUs():
    return render_template('about_us.html')

@app.route('/home/users/<string:name>/posts/<int:id>') #flask uses this to define all of its urls
def hello(name, id):    #whenever we say route whatever function that comes linearly next will get
    return "hello, "+ name +",your id is" +str(id) #so whatever is in url now gonna be displayed in the web page

@app.route('/onlyget',methods = ['GET']) #get is like you can only get, and post is like you can only post not get
def get_req():
    return "You can only get this webpage. 4"

@app.route('/posts/delete/<int:id>') #int:id is written which means from which id to delete the blogpost
def delete(id):
    post = BlogPost.query.get_or_404(id) 
    db.session.delete(post)              
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET','POST']) #methods added because if we are editing post then we need to update the db
def edit(id):
    
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST': 
        post.title = request.form['title'] #gets the data that is in the title field and save it to post.title
        post.author = request.form['author']
        post.content = request.form['content'] 
        db.session.commit()
        return redirect('/posts') #after redirecting we simply go back to posts
    else:
        return render_template('edit.html', post=post)
       
@app.route('/posts/new', methods=['GET','POST'])
def new_post():
    if request.method == 'POST': 
        post.title = request.form['title'] #gets the data that is in the title field and save it to post.title
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts') #after redirecting we simply go back to posts
    else:
        return render_template('new_post.html')


if __name__ == "__main__":
    app.run(debug=True) #shows us the error when the error pops up,it also helps us update our server or website on the flask
