from django.shortcuts import render
from flask import Flask
from flask import request
from pymongo import MongoClient

client = MongoClient('mongodb+srv://godusov:ZSuD1SP4RBHNlZa3@maincluster.zurxi.mongodb.net/maindb?retryWrites=true&w=majority')
db = client['maindb']
cll = db['userdata']
dcll = db['userdonatedata']
gcll = db['guilddata']

# Create your views here.
def homepage(request):
	totalusers = cll.count()
	totalservers = gcll.count()
	return render(request, "index.html", {'totalusers': totalusers, 'totalservers': totalservers})

def dcase(request):
	return render(request, "Donator-Case.html", {})

def dpack(request):
	return render(request, "Donator-Pack.html", {})

def propack(request):
	return render(request, "Pro-Pack.html", {})

def hpack(request):
	return render(request, "Hacker-Pack.html", {})

def confirm(request):
	if request.method == 'POST':
		userid = int(request.POST.get('userid'))
		if cll.find_one({"id": userid}) == None:
			return render(request, "Cannot-find-user.html", {'userid': userid})
		else:
			user = cll.find_one({"id": userid})
			username = user['name']
			return render(request, "Confirm-user.html", {'username': username, 'userid': userid})

def cfuser(request):
	return render(request, "Cannot-find-user.html", {})

def psuccess(request):
	if request.method == 'POST':
		totalprice = float(request.POST.get('price'))
		success = request.POST.get('success')
		userid = int(request.POST.get('userid'))
		username = request.POST.get('username')
		itemname = request.POST.get('itemname')
		quantity = int(request.POST.get('quantity'))

		if not success == "COMPLETED" or totalprice == 0 or quantity == 0:
			return render(request, "Purchase-fail.html", {})

		if success == "COMPLETED":
			if dcll.find_one({"id": userid}) ==  None:
				dcll.insert_one({"id": userid, "name": username, "totaldonated": 0.0, "totalitembought": 0, "Donator Case": 0, "Donator Pack": 0, "Pro Pack": 0, "Hacker Pack": 0})

			dcll.update_one({"id": userid}, {"$inc": {"totaldonated": totalprice}})
			dcll.update_one({"id": userid}, {"$inc": {"totalitembought": quantity}})
			if itemname == "Donator Case":
				dcll.update_one({"id": userid}, {"$inc": {"Donator Case": quantity}})
			if itemname == "Donator Pack":
				dcll.update_one({"id": userid}, {"$inc": {"Donator Pack": quantity}})
			if itemname == "Pro Pack":
				dcll.update_one({"id": userid}, {"$inc": {"Pro Pack": quantity}})
			if itemname == "Hacker Pack":
				dcll.update_one({"id": userid}, {"$inc": {"Hacker Pack": quantity}})

	return render(request, "Purchase-success.html", {})

def pfail(request):
	return render(request, "Purchase-fail.html", {})