from walrus import *

SECRET_KEY="secrets"
db =0 # change the db number
database = Database(host='127.0.0.1', port=6379, db=db) #change port number if it's not correcy
namespace ="blog"
HOME_PAGE_LIMIT=10
class BaseModel(Model):
    database = database
    namespace = namespace

class Admin(BaseModel):
    username =TextField(primary_key=True)

class User(BaseModel):
    username = TextField(primary_key=True)
    password = TextField(index=True)
    email = TextField()
    created = DateTimeField(default=datetime.datetime.now)
    last_login = DateTimeField()
    
    def __unicode__(self):
	return self.username
    
    
    
    

