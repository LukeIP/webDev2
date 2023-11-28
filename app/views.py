from flask import redirect, render_template
from app import app, models

@app.route('/users/<id>.html')
def show_wall(id):
    user = models.User.one_or_404(id=id)
    return render_template('user_wall.html', user=user)