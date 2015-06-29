from app import models

users = models.User.query.all()
f = open("passwords.txt", "w")
for user in users:
    f.write(user.username + ": " + user.password + "\n")

