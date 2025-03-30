from app import db, create_app,login_manager
from flask import render_template
from app.models import User
from config.commands import register_commands
from app.controllers.auth_controller import auth_bp
from app.controllers.user_controller import users_bp
from app.controllers.admin_controller import admin_bp

app = create_app()

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(admin_bp)
 
with app.app_context():
    register_commands(app)

@app.route("/")
def home():
    return render_template("home.html")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)