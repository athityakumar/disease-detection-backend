from __future__ import absolute_import, division, print_function


from flask import Flask, request, jsonify
import MySQLdb
import traceback
import json
import label_image
import uuid
import tagCheck
import os
from werkzeug.datastructures import ImmutableMultiDict
import sys
import json
import pickle
import random, string
app = Flask(__name__)
cursor = None
db = None
def connect_database():
	global cursor,db
	# Open database connection
	db = MySQLdb.connect("127.0.0.1", "root", os.environ["MYSQL_PASS"], "krishi")
	# prepare a cursor object using cursor() method
	cursor = db.cursor()


@app.route('/')
def hello_world():
	return 'Hello, World!'
@app.route('/hi')
def asd():
	return "HIIII"
@app.route('/login', methods=['GET', 'POST'])
def login():
	if cursor == None :
		connect_database()
	credentials_json = request.form.to_dict()
	print(credentials_json)
	query = "SELECT * FROM users WHERE Email= '%s' " % (credentials_json['email'])
	try :
		cursor.execute(query)
		dbdata = cursor.fetchone()
		print(dbdata)
		password = dbdata[0]
		print(password)
		print(credentials_json['pass'])
		db.commit()
		if password == credentials_json['pass'] :	
			print("Pass cor")
			return jsonify({"status":"1","user_type":dbdata[4]})
		else :
			print("pass wrong")
			return '{"status":"0"}'
	except TypeError as e :
		print(e)
		return '{"status":"noemail"}'
	except Exception as e:
		print(e)
		return "z"
		db.rollback()
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	details_json = request.form.to_dict()
	if cursor == None :
		connect_database()
	query = "INSERT INTO users(Email,FirstName,LastName,contact_no,password,user_type) values ('%s','%s','%s','%s','%s','%s') " % (details_json['email'] ,details_json['first_name'] , details_json['last_name'] , details_json['contact_no'],details_json['password'],details_json['user_type'])
	try :
		cursor.execute(query)
		db.commit()
		return jsonify({"status":"ok"})
	except Exception as e:
		print("In the exception ")
		if e[0] == 1062 :
			print("Duplicate entry")
			print(jsonify({"status":"dup_user"}))
			return jsonify({"status":"dup_user"})
		# print traceback.format_exc()
		return '{"a":"a"}'
		db.rollback()


@app.route('/prices',methods=['GET', 'POST'])
def price():
	user_request=request.form.to_dict()
	price_data = json.load(open('pricedata.txt' , 'r'))
	if user_request['request'] == 'pesticide' :
		print("User reqested pesticide")
		return_list = list()
		for data in price_data :
			if data['producttype'] == 'pesticide' :
				return_list.append(data)
		return jsonify({"data" : return_list})
	elif user_request['request'] == 'fertilizer' :
		return_list = list()
		print("User requested fertilizer")
		for data in price_data :
			if data['producttype'] == 'fertilizer' :
				return_list.append(data)
		return jsonify({"data" : return_list})
	elif user_request['request'] == 'seed' :
		return_list = list()
		print("User requested seed")
		for data in price_data :
			if data['producttype'] == 'seeds' :
				return_list.append(data)
		return jsonify({"data" : return_list})


@app.route('/check/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
#    print request.status_code
	print(request.method)
	print(request.form.to_dict())
   # imd = request.form

	return jsonify({"uuid":uuid})


@app.route('/news', methods=['GET', 'POST'])
def news() :
	news_data = json.load(open('newsdata.txt' , 'r'))
	return jsonify({"data":news_data})

@app.route('/crop_check', methods = ['GET', 'POST'])
def get_crop(image_id, flag=0):
	model_name = "First-Layer"
	print("Got a file")
	image_name = image_id + ".jpg"
	if flag :
		# tag_flag = tagCheck.main("{}/{}.jpg".format(label_image.IMAGES_PATH, image_id))
		tag_flag = 1
		if tag_flag:
			result = label_image.main(model_name, image_name)
			print("Crop name is:", result)
			return result[0]["disease"]
	if request.method == 'POST':
		try :
			f = request.files['file']
		except :
			return jsonify({"status":0})
		try:
			return_dict = dict()
			f.save("/home/snorloks/uploadedImages/crop_img.jpg")
			tag_flag = tagCheck.main("crop_img.jpg")
			# flag=1
			if tag_flag :
				return_dict["data"] = label_image.main(model_name,"crop_img.jpg")[0]
				return_dict["status"] = 5
				return jsonify(return_dict)
			else :
				return jsonify({"status" :2})
		except:
			print(traceback.format_exc())
		return jsonify({"status":0})


@app.route('/disease_check', methods = ['GET', 'POST'])
def get_disease(image_id=None):
	def randomword(length=10):
		letters = string.ascii_lowercase
		return ''.join(random.choice(letters) for i in range(length))

	# print "Finding disease for {}".format(crop_name)
	if request.method == 'POST':
		if not image_id:
			try :
				f = request.files['file']
			except :
				return jsonify({"status":0})
			image_id = randomword()
		try :
			return_dict = dict()
			image_name = image_id + ".jpg"
			f.save("{}/{}".format(label_image.IMAGES_PATH, image_name))
			# flag = tagCheck.main(image_name)
			flag=1
			if flag :
				# crop_name = get_crop(image_id, flag)
				crop_name = "apple"
				print("The crop is {}".format(crop_name))
				# label_image.main("banana","disease_img.jpg")
				# label_image.main("first_layer","disease_img.jpg")
				result = label_image.main(crop_name, image_name)
				# result = pickle.load(open("/home/snorloks/result.pickle","r"))
				print("THe result is {}".format(result))
				# print ("The crop is {}".format(crop_name))
				return_dict["data"] = result
				# return_dict["data"] = label_image.main(crop_name,"disease_img.jpg")
				return_dict["status"] = 1
				return jsonify(return_dict)
			else :
				return jsonify({"status" :2})
		except :
			print(traceback.format_exc())
		return jsonify({"status":0})	

@app.route('/buynsell', methods = ['GET', 'POST'])
def buynsell():
	buysell_json = request.form.to_dict()
	print(buysell_json)
	if cursor == None :
		connect_database()
	query = "INSERT INTO cropsale (crop_name,price,qty,farmer_id,description) values ('%s',%d, %d,'%s','%s') " % (buysell_json['crop'] ,int(buysell_json['price']), int(buysell_json['quantity']), buysell_json['email'],buysell_json['description'])
	try :
		cursor.execute(query)
		db.commit()
		return jsonify({"status":"ok"})
	except Exception as e:
		print(traceback.format_exc())
		print("In the exception ")
		if e[0] == 1062 :
			print("Duplicate entry")
			print(jsonify({"status":"dup_user"}))
			return jsonify({"status":"dup_user"})
	# print traceback.format_exc()
	return '{"a":"a"}'
	db.rollback()

if __name__ == '__main__':
	try :
		app.run(port=8000,debug=True,threaded=True)
		# get_disease("puxhixiqqs")
	except Exception as e:
		if e[0] == 48 :
			print("Address already in use")
		else :
			app.run(port=8000,debug=True,threaded=True)
			print("Got the following error:\n{} ".format(traceback.format_exc()))
