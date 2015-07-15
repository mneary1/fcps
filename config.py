import os 

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'supersecretkey'

ALLOWED_EXTENSIONS = ['docx','doc','pdf','txt','py','jpg','png','jpeg','gif','ppt','pptx']
UPLOAD_PATH = os.path.join(basedir, 'uploads')
READINGS_PATH = os.path.join(basedir,"app","static","readings")
ASSIGNMENTS_PATH = os.path.join(basedir,"app","static","assignments")
REFERENCES_PATH = os.path.join(basedir,"app","static","references")
