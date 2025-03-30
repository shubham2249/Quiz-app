from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.forms import RegisterForm, LoginForm
from app.models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form =RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():

        new_user = User(
                username=form.username.data,
                fullname=form.fullname.data,
                qualification=form.qualification.data,
                dob=form.dob.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form = form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash("Your account is deactivated. Contact the admin.", "danger")
                return redirect(url_for("auth.login"))
            login_user(user) 
            flash("Login successful!", "success")
            if user.is_admin:
                return redirect(url_for("admin.admin_dashboard"))
            else:
                return redirect(url_for("users.user_dashboard"))

        flash("Invalid credentials", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html", form = form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login"))


