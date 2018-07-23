from app import models, db, app
user_file = "./users.txt"
base = "ctys"
num = 1
with open(user_file) as f:
	for user in f:
		lname, fname = user.strip().split(",")
		pw = base + str(num) + lname[:3]
		user = models.User(firstname=fname, 
							lastname=lname,
							username=fname.lower(),
							password=pw,
							session=2,
							year="2018")
		db.session.add(user)
		num += 1

db.session.commit()
