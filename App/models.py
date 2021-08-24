from App import db

class ListVaccine(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(length=20), nullable=False)

