from django.shortcuts import render, redirect
from flask import Flask
from flask import request
from pymongo import MongoClient
import requests

client = MongoClient('mongodb+srv://godusov:ZSuD1SP4RBHNlZa3@maincluster.zurxi.mongodb.net/maindb?retryWrites=true&w=majority')
db = client['maindb']
cll = db['userdata']
dcll = db['userdonatedata']
gcll = db['guilddata']
discordauthurl = "https://discord.com/api/oauth2/authorize?client_id=863028787708559400&redirect_uri=https%3A%2F%2Fovbotdiscord.herokuapp.com%2Fconfirm-user&response_type=code&scope=identify"
global loggedid

# Create your views here.
def homepage(request):
	totalusers = cll.count()
	totalservers = gcll.count()
	return render(request, "index.html", {'totalusers': totalusers, 'totalservers': totalservers})

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
		gift = request.POST.get('gift')

		if not success == "COMPLETED" or totalprice == 0 or quantity == 0:
			return render(request, "Purchase-fail.html", {})

		if success == "COMPLETED":
			if gift == "False":
				if dcll.find_one({"id": userid}) ==  None:
					dcll.insert_one({"id": userid, "name": username, "totaldonated": 0.0, "totalitembought": 0, "Donator Case": 0, "Donator Pack": 0, "Pro Pack": 0, "Hacker Pack": 0, "gifted": 0, 'giftreceived': 0, 'gifts': {}})
				user = dcll.find_one({"id": userid})
				if not user['name'] == username:
					dcll.update_one({"id": userid}, {"$set": {"name": username}})
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
			elif gift == "True":
				gifterid = int(request.POST.get('gifterid'))
				giftername = request.POST.get('giftername')
				if dcll.find_one({"id": gifterid}) ==  None:
					dcll.insert_one({"id": gifterid, "name": giftername, "totaldonated": 0.0, "totalitembought": 0, "Donator Case": 0, "Donator Pack": 0, "Pro Pack": 0, "Hacker Pack": 0, "gifted": 0, 'giftreceived': 0, 'gifts': {}})
				if dcll.find_one({"id": userid}) ==  None:
					dcll.insert_one({"id": userid, "name": username, "totaldonated": 0.0, "totalitembought": 0, "Donator Case": 0, "Donator Pack": 0, "Pro Pack": 0, "Hacker Pack": 0, "gifted": 0, 'giftreceived': 0, 'gifts': {}})
				user = dcll.find_one({"id": userid})
				gifter = dcll.find_one({"id": gifterid})
				if not user['name'] == username:
					dcll.update_one({"id": userid}, {"$set": {"name": username}})
				if not gifter['name'] == giftername:
					dcll.update_one({"id": gifterid}, {"$set": {"name": giftername}})
				dcll.update_one({"id": gifterid}, {"$inc": {"totaldonated": totalprice}})
				dcll.update_one({"id": gifterid}, {"$inc": {"totalitembought": quantity}})
				dcll.update_one({"id": gifterid}, {"$inc": {"gifted": quantity}})
				dcll.update_one({"id": userid}, {"$inc": {"giftreceived": quantity}})
				dcll.update_one({"id": userid}, {"$set": {"gifts": {"gifterid": gifterid, "itemname": itemname, "quantity": quantity}}})
				if itemname == "Donator Case":
					dcll.update_one({"id": userid}, {"$inc": {"Donator Case": quantity}})
				if itemname == "Donator Pack":
					dcll.update_one({"id": userid}, {"$inc": {"Donator Pack": quantity}})
				if itemname == "Pro Pack":
					dcll.update_one({"id": userid}, {"$inc": {"Pro Pack": quantity}})
				if itemname == "Hacker Pack":
					dcll.update_one({"id": userid}, {"$inc": {"Hacker Pack": quantity}})
				return render(request, "Purchase-success.html", {})
	return render(request, "Purchase-success.html", {})

def pfail(request):
	return render(request, "Purchase-fail.html", {})

def verify(request):
	return render(request, "A6085E730C40707DBAFA47AB2118475E.txt", {})

def login(request):
	return redirect(discordauthurl)

def confirm(request):
	print("A")
	if request.method == 'GET':
		code = request.GET.get('code')
		user = exchangecode(code)
		userid = int(user['id'])
		loggedid = userid
		if cll.find_one({"id": userid}) == None:
			return render(request, "Cannot-find-user.html", {'userid': userid})
		else:
			user = cll.find_one({"id": userid})
			username = user['name']
			return render(request, "Confirm-user.html", {'username': username, 'userid': userid})
	elif request.method == 'POST':
		print("B")
		userid = int(request.POST.get('userid'))
		if cll.find_one({"id": userid}) == None:
			return render(request, "Cannot-find-user.html", {'userid': userid})
		else:
			print(loggedid)
			gifter = cll.find_one({"id": loggedid})
			user = cll.find_one({"id": userid})
			username = user['name']
			giftername = gifter['name']
			return render(request, "Gifting-user.html", {'username': username, 'userid': userid, 'giftername': giftername, 'gifterid': loggedid})


def exchangecode(code: str):
	data = {
		'client_id': '863028787708559400',
		'client_secret': '2nE2Ck8aupqxQ2Wi7LVS2GF4ff-nq3jA',
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': 'https://ovbotdiscord.herokuapp.com/confirm-user',
		'scope': 'identify'
	}
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
	credentials = response.json()
	access_token = credentials['access_token']
	response = requests.get("https://discord.com/api/v6/users/@me", headers = {"Authorization": "Bearer %s" % access_token})
	user = response.json()
	return user
