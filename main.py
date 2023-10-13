from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    comment = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_movies = db.session.query(Movie).all()
    return render_template('index.html', movies=all_movies)


@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie_title = request.form['title']
        movie_comment = request.form['comment']
        movie_rating = request.form['rating']
        new_movie = Movie(title=movie_title, comment=movie_comment, rating=movie_rating)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit_rating():
    if request.method == 'POST':
        movie_id = request.form['id']
        movie_to_update = db.get_or_404(Movie, movie_id)
        movie_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    movie_id = request.args.get('id')
    movie_selected = db.get_or_404(Movie, movie_id)
    return render_template('edit.html', movie=movie_selected)


@app.route('/delete')
def delete_movie():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
