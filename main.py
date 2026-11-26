# --------------- Portfolio Website --------------- #
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Float, Date, ForeignKey, func
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, ProjectTypeForm, ExecutableForm, GameForm, GeneralForm, ContactForm, EditForm
from email.message import EmailMessage
from ssl import create_default_context
from datetime import date
import sqlalchemy
import smtplib
import os

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'super_secret_change_later'

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager(app)

db.init_app(app)


# --------------- Variables --------------- #
category_desc = {"software": "Clean, Scalable, Code.", "game dev": ""}

MY_INBOX = "caydenmfritz@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = MY_INBOX #os.environ.get("SENDER_EMAIL")
SENDER_PASSWORD = "kslmstvbdecdrjsf" #os.environ.get("SENDER_PASSWORD")

admin_account = 'caydenmfritz@gmail.com'
project_types = ['executable', 'game', 'general']
project_categories = ['software', 'game dev', 'engineering']

owner = 'Cayden Fritz'
start_date = "2026"
current_date = date.today().year


# --------------- User Database --------------- #
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    password_hashed: Mapped[str] = mapped_column(String(256), nullable=False)
    profile_img: Mapped[str] = mapped_column(String, nullable=False, default='imgs/default_avater.png')


# --------------- Projects Database --------------- #
class Project(db.Model):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    tag: Mapped[str] = mapped_column(String(12), nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    tools: Mapped[str | None] = mapped_column(String, nullable=True)
    cover_image: Mapped[str] = mapped_column(String, nullable=True)

    images: Mapped[list['ProjectMedia']] = relationship('ProjectMedia', back_populates='project', cascade='all, delete-orphan')
    html: Mapped[list['ProjectHTML']] = relationship('ProjectHTML', back_populates='project', cascade='all, delete-orphan')


# --------------- Project Images --------------- #
class ProjectMedia(db.Model):
    __tablename__ = 'project_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), nullable=False)
    image_url: Mapped[list[String]] = mapped_column(String, nullable=True)
    video_url: Mapped[list[String]] = mapped_column(String, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    project: Mapped['Project'] = relationship("Project", back_populates="images")


# --------------- Project HTML --------------- #
class ProjectHTML(db.Model):
    __tablename__ = 'project_html'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), nullable=False)
    html_url: Mapped[list[String]] = mapped_column(String)

    project: Mapped["Project"] = relationship("Project", back_populates="html")


# --------------- Project List Database --------------- #
class ProjectList(db.Model):
    __tablename__ = 'project_list'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# --------------- Functions --------------- #
def send_contact_email(user_name, user_email, user_message, user_subject='New Contact'):
    msg = EmailMessage()
    msg['Subject'] = user_subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = MY_INBOX
    msg['Reply-To'] = user_email

    body_content = f"Message from: {user_name} | {user_email}\n\nMessage:\n{user_message}"
    msg.set_content(body_content)

    context = create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)


# --------------- Web Routes --------------- #
@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            send_contact_email(
                user_name=form.name.data,
                user_email=form.email.data,
                user_message=form.message.data
            )

            flash('Form sent successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            app.logger.error(f"Mail delivery failed: {e}")
            flash('There was an issue sending you message. Please try again later.', 'danger')

    random_software = db.session.execute(db.select(Project).where(Project.category == 'Software').order_by(func.random()).limit(1)).scalar_one_or_none()
    random_game = db.session.execute(db.select(Project).where(Project.category == 'Game').order_by(func.random()).limit(1)).scalar_one_or_none()
    random_hardware = db.session.execute(db.select(Project).where(Project.category == 'Hardware').order_by(func.random()).limit(1)).scalar_one_or_none()
    random_3d_design = db.session.execute(db.select(Project).where(Project.category == '3D Design').order_by(func.random()).limit(1)).scalar_one_or_none()

    if random_software or random_game or random_3d_design:
        return render_template('index.html', owner=owner, date=current_date, start_date=start_date, form=form, software_block=random_software, game_block=random_game, design_3d_block=random_3d_design, hardware_block=random_hardware, current_user=current_user, admin_account=admin_account)
    return render_template('index.html', owner=owner, date=current_date, start_date=start_date, form=form, current_user=current_user, admin_account=admin_account)


@app.route('/project/<int:project_id>', methods=['GET', 'POST'])
def project(project_id):
    current_project = db.session.execute(db.select(Project).filter_by(id=project_id)).scalar_one_or_none()
    if current_project:
        return render_template('project.html', project=current_project, current_user=current_user, admin_account=admin_account)
    return redirect(url_for('home'))


@app.route('/projects/<category>')
def all_projects(category):
    results = db.session.scalars(db.select(Project).filter_by(category=category))

    projects = ({c.name: getattr(project, c.name) for c in project.__table__.columns} for project in results)
    projects_list = list(projects)

    if category == 'Game':
        category = 'Game Development'
    elif category == 'Software':
        category = 'Software Development'

    return render_template('all_projects.html', projects=projects_list, owner=owner, date=current_date, start_date=start_date, category=category)


#@login_required
@app.route('/select_project_type', methods=['GET', 'POST'])
def select_project_type():
    form = ProjectTypeForm()

    if form.validate_on_submit():
        project_type = str(form.type.data).lower()
        if project_type in project_types:
            return redirect(url_for('add_project', project_type=project_type))

    return render_template('project_type.html', form=form)


@login_required
@app.route('/add_project/<project_type>', methods=['GET', 'POST'])
def add_project(project_type):
    if project_type not in project_types:
        flash('Project type not found in selection', 'danger')
        return redirect(url_for('select_project_type'))

    form_map = {
        'general': (GeneralForm, 'add_project_general.html'),
        'game': (GameForm, 'add_project_game.html'),
        'executable': (ExecutableForm, 'add_project_executable.html')
    }

    form_class, template = form_map[project_type]
    form = form_class()

    if form.validate_on_submit():
        new_project = Project(
            name=form.name.data,
            description=form.description.data,
            tag=form.tag.data,
            tools=form.tools.data,
            category=form.category.data,
            cover_image=form.cover_image.data
        )
        db.session.add(new_project)
        db.session.flush()

        # Handle general project's extra fields (images and videos)
        if project_type == 'general':
            if form.image_urls.data:
                for url in form.image_urls.data.splitlines():
                    clean_url = url.strip()
                    if clean_url:
                        media = ProjectMedia(project_id=new_project.id, image_url=clean_url)
                        db.session.add(media)

            if form.video_urls.data:
                for url in form.video_urls.data.splitlines():
                    clean_url = url.strip()
                    if clean_url:
                        media = ProjectMedia(project_id=new_project.id, video_url=clean_url)
                        db.session.add(media)

        # Handle game project's extra fields (HTML, URL)
        elif project_type == 'game':
            if form.html_url.data:
                html_entry = ProjectHTML(project_id=new_project.id, html_url=form.html_url.data)
                db.session.add(html_entry)

        db.session.commit()
        return redirect(url_for('project', project_id=new_project.id))
    return render_template(template, form=form, project_type=project_type)


@login_required
@app.route('/remove_project/<int:project_id>', methods=['GET', 'POST'])
def remove_project(project_id):
    current_project = db.session.execute(db.select(Project).filter_by(id=project_id)).scalar_one_or_none()

    if current_project:
        db.session.delete(current_project)
        db.session.commit()

        flash('Project deleted successfully', 'success')

        return redirect(url_for('home'))
    else:
        flash("Couldn't delete project", 'danger')
    return redirect(url_for('home'))


@app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    current_project = db.session.execute(db.select(Project).filter_by(id=project_id)).scalar_one_or_none()

    form = EditForm()

    if form.validate_on_submit():
        if form.name.data != "":
            current_project.name = form.name.data
        if form.description.data != "":
            current_project.description = form.description.data
        if form.tools.data != "":
            current_project.tools = form.tools.data

        db.session.commit()

        return redirect(url_for('project', project_id=project_id))
    return render_template('edit.html', form=form, project=current_project)


@app.route('/about')
def about():
    return render_template('about.html', owner=owner, date=current_date, start_date=start_date, current_user=current_user)


@app.route('/contact')
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            send_contact_email(
                user_name=form.name.data,
                user_email=form.email.data,
                user_message=form.message.data
            )

            flash('Form sent successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            app.logger.error(f"Mail delivery failed: {e}")
            flash('There was an issue sending you message. Please try again later.', 'danger')

    return render_template('contact.html', form=form, owner=owner, date=current_date, start_date=start_date, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data

        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

        if user and check_password_hash(user.password_hashed, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password, please try again.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data.lower()
        password = form.password.data

        user_exists = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
        if user_exists:
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(str(password))
        new_user = User(username=username, email=email, password_hashed=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
