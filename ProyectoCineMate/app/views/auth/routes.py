from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app import get_sirope
from app.core.auth import auth_service

auth_routes = Blueprint("auth", __name__, url_prefix="/auth")


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    srp = get_sirope()

    if form.validate_on_submit():
        if auth_service.login_with_credentials(srp, form.username.data, form.password.data):
            return redirect(url_for("main_routes.index"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template("auth/login.html", form=form)


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    srp = get_sirope()

    if form.validate_on_submit():
        if auth_service.register_user(srp, form.username.data, form.password.data, form.email.data):
            flash("Usuario registrado correctamente. Inicia sesión.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("El nombre de usuario ya está en uso", "warning")

    return render_template("auth/register.html", form=form)


@auth_routes.route("/logout")
@login_required
def logout():
    auth_service.logout_current_user()
    return redirect(url_for("main_routes.index"))


@auth_routes.route("/editar_nombre", methods=["GET", "POST"])
@login_required
def edit_username():
    srp = get_sirope()

    if request.method == "POST":
        new_username = request.form.get("new_username", "").strip()
        user, error = auth_service.update_username(srp, current_user.get_id(), new_username)

        if error:
            flash(error, "danger" if "uso" in error else "warning")
        else:
            flash("Nombre de usuario actualizado correctamente. Vuelva a Iniciar Sesión.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/edit_username.html", user=current_user)
