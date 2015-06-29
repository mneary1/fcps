from app import db, models

users = models.User.query.all()

for user in users:
    db.session.delete(user)

db.session.commit()
