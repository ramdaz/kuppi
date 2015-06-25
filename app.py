from bottle import get, post, request,  jinja2_view,request, route, hook, redirect, run, url, static_file
from settings import *
import os, jinja2, random, bottle
import beaker.middleware
from functools import wraps
from hashlib import md5, sha256
from wtforms import Form, BooleanField as BField, StringField, PasswordField, IntegerField as IField, validators, TextAreaField, FileField
from utils import *
import datetime, time
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#Another check,
from local_settings import *
if DEBUG_MODE==False:
    BASE_DIR = "/var/www/kuppi/"
import bottle
from beaker.middleware import SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 144000,
    'session.data_dir': './session',
    'session.auto': True
}

app = SessionMiddleware(bottle.default_app(), session_opts)

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    autoescape=True,
)
env.globals.update({
    'url': url,
    'site_name': 'Kuppi-Blog',
})
env.filters['datetimeformat'] = datetimeformat

@route('/session_test')
def session_test():
    app = SessionMiddleware(bottle.app(), session_opts)
    varsession = bottle.request.environ.get('beaker.session')
    return str(dir(varsession))
    varsession['value1'] = 'This is the value'
    return varsession['value1']

@bottle.route('/test')
def test():
    s = bottle.request.environ.get('beaker.session')
    s['test'] = s.get('test',0) + 1
    s.save()
    return 'Test counter: %d' % s['test']

def view(template_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            response = view_func(*args, **kwargs)

            if isinstance(response, dict):
                template = env.get_or_select_template(template_name)
                return template.render(**response)
            else:
                return response

        return wrapper

    return decorator


    
    


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
	s = bottle.request.environ.get('beaker.session')

        if s !=None:
	    if not s.get('logged_in'):
		return redirect('/login')
	else:
	    return redirect('/login')
        return f(*args, **kwargs)
    return inner

def admin_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
	s = bottle.request.environ.get('beaker.session')
	if s !=None:
	    if not s.get('logged_in'):
		return redirect('/login')
	    else:
		h= s.get('username')
		try:
		    x= Admin.load(h)
		except:
		    return "You need to be an Admin to do Access this Functions"
	    return f(*args, **kwargs)
	else:
	    return redirect('/login')
    return inner
def is_admin(username):
    try:
	admin =Admin.load(username)
	return True
    except:
	return False
def location(f):
    return os.path.join(BASE_DIR, f)

def check_login(username, password):
    try:
	user=User.load(username)
	if sha256(SECRET_KEY+password).hexdigest()== user.password:
	    return True, 0
	else:
	    return False, 1
	    
    except ValueError:
	return False, 2
    except KeyError:
	return False, 3
    
def auth_user(username):
    try:
	s = bottle.request.environ.get('beaker.session')

	s ['logged_in'] = True
	s['username'] = username
	try:
	    user =User.load(username)
	    user.last_login= datetime.datetime.now()
	    user.save()
	except KeyError:
	    pass
	s.save()
    except:
	bottle.request.environ["beaker.session"]={}
	s= bottle.request.environ.get('beaker.session')
	s ['logged_in'] = True
	s['username'] = username
def get_user():
    try:
	s = bottle.request.environ.get('beaker.session')

	if s['logged_in'] == True:
	    return s['username']
    except:
	return None
    
def unique_slugify(title, all_list):
    s= ''.join([t.lower() for t in title if (t.isalnum() or t==" " or t=="-")])
    s= s.replace(" ", "-")
    if s in all_list:
	s+=str(random.random())[:4]
    return s

def slugify(title):
    s= ''.join([t.lower() for t in title if (t.isalnum() or t==" " or t=="-")])
    s= s.replace(" ", "-")
    return s
def get_available_name(name):
    if os.path.exists(name):

	dir_name, file_name = os.path.split(name)
	file_root, file_ext = os.path.splitext(file_name)
	new_file_name = file_root +"_"+get_random_string() + file_ext
	return os.path.join(dir_name, new_file_name)
    else:
	return name


###############ENV FILTERS###################


def get_author_name(username):
    
    try:
	author=Author.load(self.author)
	return author.name
    except:
	return username
    
def get_author_url(username):
    try:
	author=Author.load(author)
	return author.get_absolute_url()
    except:
	return "#"
    return "#"
    
env.filters['get_author_name'] = get_author_name
env.filters['get_author_url'] = get_author_url
def get_author_pic(username):
    
    try:
	author=Author.load(username)
	return author.get_pic_url()
    except:
	return ""

def get_author_bio(username):
    try:
	author=Author.load(username)
	return author.bio
    except:
	return ""

def get_absolute_url_post(pid):
    try:
	post=Post.load(pid)
	return post.get_absolute_url()
    except:
	return ""
def get_avatar(username):
    try:
	avatar=Avatar.load(username)
	return '<img src="/%s">' %(avatar.path)
    except:
	return '<img src="/static/user.png">'
def get_tags(pid):
    odd ="post-category post-category-design"
    even ="post-category post-category-pure"
    post = Post.load(pid)
    tags = list(post.tags)
    x=" "
    for tag in tags:
	if tags.index(tag)%2==0:
	    x+='<a class="%s" href="/tags/%s">%s</a>' %(even,tag, tag)
	elif tags.index(tag)%2==1:
	    x+='<a class="%s" href="/tags/%s">%s</a>' %(odd,tag, tag)
    return x
env.filters['get_author_pic'] =get_author_pic
env.filters['get_author_bio'] = get_author_bio
env.filters['get_tags'] =get_tags

env.filters['get_absolute_url_post'] = get_absolute_url_post
env.filters['get_avatar'] = get_avatar

#################################MODELS###################################





class Author(BaseModel):
    user = TextField(primary_key=True)
    name = TextField(index=True)
    bio = TextField()
    picture= TextField()
    def __unicode__(self):
	return self.user
    def get_absolute_url(self):
	return "/authors/%s" %(self.user)

class Post(BaseModel):
    author = TextField(index=True)
    pid = AutoIncrementField(primary_key=True)
    
    title = TextField(index=True)
    keywords = TextField()
    slug = TextField(index=True)
    intro = TextField(index=True)
    body = TextField(index=True, fts=True)
    created = DateTimeField(index=True)
    edited = DateTimeField()
    tags = SetField()
    draft = IntegerField(index=True)
    
    def __unicode__(self):
	return self.title
    def get_absolute_url(self):
	return "/posts/%s/%s" %(self.slug, self.pid)


class File(BaseModel):
    filename = TextField()
    path = TextField()
    def __unicode__(self):
	return self.filename
    def get_url(self):
	return self.path
    def is_image(self):
	if self.path !=None:
	    
	    try:
		ext=(os.path.splitext(self.path)[1]).lower()
		if ext in (".jpg", ".gif", ".png", ".jpeg"):
		    return True
	    except:
		return False
	return False

class Avatar(BaseModel):
    username = TextField(primary_key=True)
    path =TextField()
    def is_image(self):
	if self.path !=None:
	    
	    try:
		ext=(os.path.splitext(self.path)[1]).lower()
		if ext in (".jpg", ".gif", ".png", ".jpeg"):
		    return True
	    except:
		return False
	return False

################################WTF FORM CLASSES ####################################    

class LoginForm(Form):
    username     = StringField('Username', [validators.Length(min=4, max=25)])
    password     = PasswordField('Password', [validators.Length(min=8, max=35)])



class FileForm(Form):
    filename =StringField('Title', [validators.Length(min=4, max=125)])
    upload = FileField()
    
class PostForm(Form):
    title     = StringField('Title', [validators.Length(min=4, max=125)])
    intro     = TextAreaField('Introduction')
    keywords  = StringField('Key  Words', [validators.Length(min=4, max=125)])
    body      = TextAreaField()
    draft     = BField("Is it Draft")
    tags      = StringField( "Tags",[validators.Length(min=4, max=125)])
    

class AuthorForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=125)])
    bio      = TextAreaField()
    
class AvatarForm(Form):
    username = StringField('User Name', [validators.Length(min=4, max=125)])
    upload = FileField()


####################Form Methods #############################################
    
@get("/login")
@route( "/login")
@view('login.html')
def login():
    
    form = LoginForm()
    return {"form":form}

@route("/upload_file")
@view("upload.html") 
@login_required   
def file_form():
    form =FileForm()
    return {"form":form}


@route("/upload_file", method="POST")
@login_required   
def file_form():
    form = FileForm(request.forms)
    if form.validate():
	upload     = request.files.get('upload')
	name = upload.filename
	path = os.path.join(BASE_DIR, "media/uploads/")
	
	path1 =os.path.join(path, name)
	
	try:
	    name =get_available_name(path1)
	    upload.save(name)
	except IOError as e:    
	    return "I/O error({0}): {1}".format(e.errno, e.strerror)
	F= File.create(filename= form.filename.data, path=name)
	F.save()
	if F.is_image():
	    return redirect("/"+F.path)
	else:
	    return "File Uploaded Successfully"


@route("/create_avatar")
@view("avatar.html") 
@login_required   
def avtar_form():
    form =AvatarForm()
    return {"form":form}

from avatar.round_avatar import *
@route("/create_avatar", method="POST")
@login_required   
def avtar_form():
    form = AvatarForm(request.forms)
    if form.validate():
	upload     = request.files.get('upload')
	name = upload.filename
	path = os.path.join(BASE_DIR, "media/avatar/")
	
	path1 =os.path.join(path, name)
 	
	try:
	    name =get_available_name(path1)
	    upload.save(name)
	    
	except IOError:
	    return "Unable to Save the File"
	
	F= Avatar.create(username= form.username.data, path=name)
	F.save()
	if F.is_image():
	    path =masker(name,(128,128))
	    F.path =path
	    F.save()
	    return "Avtar Created"
	else:
	    return "File Uploaded Successfully"


@route("/create_author")    
@view("create_author.html") 
@login_required   
def author_form():
    try:
	s = bottle.request.environ.get('beaker.session')
	username =s['username']
	
	author= Author.load(username)
	
	form =AuthorForm(data={"name": author.name, "bio":author.bio})
	
	return {"form": form }
    except:
	form =AuthorForm()
	return {"form": form }

@route('/create_author', method= 'POST')
@login_required
def create_author():
    form = AuthorForm(request.forms)
    if form.validate():
	s = bottle.request.environ.get('beaker.session')
	username =s['username']
	try:
	    author = Author.load(username)
	    author.name = form.name.data
	    bio = form.name.bio
	    author.save()
	    return "Author Edited Successfully"

	except:
	    author =Author.create(name=form.name.data,  bio=  form.bio.data, user=username)
	
	    author.save()
	    return "Author Created Successfully"

@route("/post")
@view("post.html")   
@login_required 
def post():
    form =PostForm()
    return {"form": form }


@route("/post", method="POST")
@login_required
def do_post():
    form = PostForm(request.forms)
    if form.validate():
	s = bottle.request.environ.get('beaker.session')
	username =s['username']
	
	slugs = [p.slug for p in Post.all()]
	
	    
	    
	slug = unique_slugify(form.title.data, slugs)
	if form.draft.data==True:
	    draft=1
	else:
	    draft=0
	post =Post.create(title=form.title.data, intro= form.intro.data, body =form.body.data, created=datetime.datetime.now(),\
	edited=datetime.datetime.now(),  slug=slug, draft=draft, author=username)

	post.save()
	if len(form.tags.data)>4:
	    tags = form.tags.data.split(",")
	    for tag in tags:
		post.tags.add(tag.strip(' '))


	post.save()
	return redirect(post.get_absolute_url())
	#return redirect("/posts/%s/%s" %(post.slug,post.pid))

@route("/posts/<slug>/<pid:int>")
@view("post_detail.html")
def post_detail(slug,pid):
    user=get_user()
    post =Post.load(int(pid))
    body = post.body
    title = post.title
    intro = post.intro
    author = post.author
    edited = post.edited
    created = post.created
    if abs((edited -created).seconds) <4:
	really_edited=None
    else:
	really_edited=True
   
    return {"body":post.body,"title":post.title,"author":post.author,"edited":post.edited,"created":post.created,"intro":post.intro,
     "slug":post.slug, "user": user,"pid":pid, "really_edited":really_edited}
		


@route("/post_edit/<pid:int>")
@view("post_edit.html")   
@login_required 
def post_edit(pid):
    post =Post.load(int(pid))
    data = {"title":post.title, "keywords": post.keywords, "intro": post.intro, "body":post.body, "draft":post.draft}
    form =PostForm(data=data)
    return {"form": form,     "user":get_user(),  "pid": pid}


@route("/post_edit/<pid:int>", method="POST")
@login_required 
def post_edit(pid):
    form = PostForm(request.forms)
    if form.validate():
	
	s = bottle.request.environ.get('beaker.session')
	username =s['username']
	post =Post.load(int(pid))
	if post.author == username or  is_admin(username):
	    pass
	else:
	    return "You do not have Permissions"
	post.title =form.title.data
	post.intro= form.intro.data
	post.body =form.body.data
	post.keywords = form.keywords.data
	post.edited=datetime.datetime.now()
	if form.draft.data==True:
	    post.draft=1
	else:
	    post.draft=0
	
	post.save()
	if len(form.tags.data)>4:
	    tags = form.tags.data.split(",")
	    for tag in tags:
		post.tags.add(tag.strip(' '))

	post.save()
	return redirect("/posts/%s/%s" %(post.slug,post.pid))
    else:
	return "SNAFU"

class Post_View(BaseModel):
    pid = IntegerField(primary_key=True)
    views =IntegerField(index=True)
    ipaddress = TextField(index=True)


    
    def increment(self):
	self.views+=1
	self.save()
    
@route("/login", method="POST")
def do_login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    tup =check_login(username, password)
    if tup[0]==True:
	auth_user(username)
	redirect("/")
    elif tup[1]==1 :
	return "<p>Login failed.</p>"
    elif tup[1]==3:
	return "<p>Username does not Exist.</p>"
    else:
	return "<p>Chooth does not Exist.</p>"
	



class RegistrationForm(Form):
    username     = StringField('Username', [validators.Length(min=4, max=25)])
    email        = StringField('Email Address', [validators.Length(min=6, max=35)])
    password     = PasswordField('Password', [validators.Length(min=4, max=35)])
    #accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])
    #class Meta:
        #csrf = True
        #csrf_class = IPAddressCSRF

@route('/register')
@view('register.html')
@admin_required
def register_view():
    form = RegistrationForm()
    return {"form": form}

    
@route('/register', method= 'POST')
def register():
    
    form = RegistrationForm(request.forms )
    if form.validate():
	#return str((form.username.data))
	user =create_user(username=form.username.data, password= form.password.data, email =form.email.data)
	if user !=None:
	    return "User is Registered"
	else:
	    return "User Exists or Some Error"
    else:
	return "SNAFU"
    return {"form": form}
  
@route("/static/<filename>")
def server_static(filename):
    return static_file(filename, location("static"))
@route("/static/<filepath:path>")
def server_static_path(filepath):
    
    return static_file(filepath, location("static"))

@route("/media/<filepath:path>")
def server_media_path(filepath):
    
    return static_file(filepath, location("media"))



@route("/app_dir", name="app_dir")
def dir_app():
    return str(dir(app))

@route('/log', name='log')
@login_required
def log():
    return redirect("/app_dir")
@route('/authors/<username>')
@view('/author_stories.html')
def author_details(username):
    posts= Post.query(Post.author==username)
    return {"user": get_user(), "posts":posts}
    
@route('/tags/<tag>')
@view('/tag_stories.html')
def tag_details(tag):
    posts= list(p for p in Post.all() if tag in list(p.tags))
    return {"user": get_user(), "posts":posts}
@route('/logout')
@route('/logout')
def logout():
    s = bottle.request.environ.get('beaker.session')
    s['logged_in'] = None
    s.save()
    return redirect("/")
@route('/', name='home')
@view('index.html')
def home():
    posts =list(Post.query(Post.draft!=1, order_by=Post.created.desc()))[:HOME_PAGE_LIMIT]

    return {'posts': posts, "user":get_user()}


###Dashboard###

@route('/dashboard', name='dashboard')
@view("dashboard.html")
@login_required
def dashboard():
    s = bottle.request.environ.get('beaker.session')
    username =s['username']
    if is_admin(username):
	posts=Post.query(order_by=Post.created.desc())
    else:
	posts= Post.query(Post.author==username, order_by=Post.created.desc())
    return {"posts":posts}

from local_settings import *

if DEBUG_MODE==True:
    run(app=app, host="127.0.0.1", port=8008, debug=True, autoload=True)
else:
    pass
