from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	firstname = db.Column(db.String(64), unique=False)
        lastname = db.Column(db.String(64), unique=False)
        password = db.Column(db.String(64), index=True, unique=False)
        session = db.Column(db.Integer)
        year = db.Column(db.String(4), unique=False)

	def __repr__(self):
		return "User<%r> Name<%r, %r> Year<%r> Session<%r>" % (self.username, self.lastname, self.firstname, self.year, self.session)

        def __str__(self):
                return "%s, %s %s session %d" % (self.lastname, self.firstname, self.year, self.session)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	
