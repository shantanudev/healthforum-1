#!/usr/bin/python
import json
from healthcode import app
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, abort, fields, marshal_with, marshal
from flask.ext.restful.utils import cors
from database import db, Users
from flask.ext.sqlalchemy import SQLAlchemy

"""
More information about Flask RESTful:
http://flask-restful.readthedocs.org/en/latest/installation.html

More documentation on cors (cross origin resource sharing):
https://github.com/twilio/flask-restful/pull/131

More information on argument passing:
http://flask-restful.readthedocs.org/en/latest/reqparse.html

For the brave souls: To push this server onto heroku,
https://devcenter.heroku.com/articles/getting-started-with-python

"""

herokuURI = 'mysql://bbe6adb0b555dc:488c7e4d@us-cdbr-east-05.cleardb.net/heroku_5f9923672d3888a'
henryURI = 'mysql://halin2_guest:helloworld@engr-cpanel-mysql.engr.illinois.edu/halin2_sample'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = henryURI
db = SQLAlchemy(app)

api = restful.Api(app)
api.decorators=[cors.crossdomain(origin='*')]

# Generic function that aborts the call if the
# queried index is not in the input list
def assertInList(inputList, index):
	if not(len(inputList) > index >= 0) or inputList[index] is None:
		abort(404, message = "ERROR! Item doesn't exist in table.")
#
## Drug
## show a single drug item and lets you delete them
#class Drug(restful.Resource):
#
#	# $ curl localhost:5000/drugs/2
#	def get(self, drugNum):
#		assertInList(drugsTable, drugNum)	
#		return drugsTable[drugNum]
#
#	# $ curl localhost:5000/drugs/1 -X DELETE
#	def delete(self, drugNum):
#		assertInList(drugsTable, drugNum)	
#		drugsTable[drugNum] = None
#		return "Successfully killed.", 204
#
#api.add_resource(Drug, '/drugs/<int:drugNum>')
#
#
## Allows the input URI to be parsed
## We can theoretically use this for the above class, but we didn't
#parser = reqparse.RequestParser()
#parser.add_argument('name', type = str)
#parser.add_argument('side_effects', type = str, action = "append")	# Creates array
#
## DrugList
## shows a list of all drugs, and lets you POST to add new drugs
#class DrugList(restful.Resource):
#
#	# Gets the current list
#	# $ curl localhost:5000/drugs
#	def get(self):
#		return drugsTable
#
#	# Adding a new drug and side effects list
#	# $ curl http://localhost:5000/drugs -d "name=advil" -d "side_effect=nausea" -d "side_effect=dying" -X POST -v
#	# Interesting note: When formulating your post request, don't have a space before
#	def post(self):
#
#		# Parse the arguments from the post request
#		args = parser.parse_args()
#		name = args["name"]				# name = "advil"
#		effects = args["side_effect"] 	# effects = ["nausea", "dying"] 
#	
#		# Create the dictionary that we're going to put into the table
#		drugDict = dict()
#		drugDict["name"] = name
#		drugDict["side effects"] = effects
#
#		# Add this to the table and send its index to the client
#		drugsTable.append(drugDict)
#		drugNum = len(drugsTable) - 1
#		return drugNum, 201
#
#api.add_resource(DrugList, '/drugs')
#
#class DrugNames(restful.Resource):
#
#	def get(self):
#		names = [drugObj["name"] for drugObj in drugsTable]
#		return names, 201
#
#api.add_resource(DrugNames, '/names')
#

# Marshalling documentation:
# http://flask-restful.readthedocs.org/en/latest/api.html
# http://flask-restful.readthedocs.org/en/latest/fields.html
users_fields = {
	'first_name': fields.String,
	'last_name': fields.String,
	'dob': fields.DateTime,
	'weight_lbs': fields.Integer,
	'height_inches': fields.Integer,
	'gender': fields.Raw
}


# Added April 8th to test out querying database
class Users_resource(restful.Resource):

	def get(self):
		users = Users.query.all()
		return [marshal(user, users_fields) for user in users], 200

api.add_resource(Users_resource, '/users')

################################################
################################################

user_parser = reqparse.RequestParser()
user_parser.add_argument('first', type = str)
user_parser.add_argument('last', type = str)
user_parser.add_argument('dob', type = str)

users_fields = {
	'first_name': fields.String,
	'last_name': fields.String,
	'dob': fields.DateTime,
	'weight_lbs': fields.Integer,
	'height_inches': fields.Integer,
	'gender': fields.Raw
}
class User_resource(restful.Resource):

	# $ curl http://localhost:5000/user -d "first=john" -d "last=smith" -X POST -v
	def post(self):
		args = user_parser.parse_args()
		first = args['first']
		last = args['last']
		dob = restful.types.date(args['dob'])
		user = Users(first, last, dob)

		db.session.add(user)
		db.session.commit()

api.add_resource(User_resource, '/user')


if __name__ == '__main__':
	app.run(debug=True)
