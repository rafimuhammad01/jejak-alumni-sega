from django.shortcuts import render,redirect
from .forms import editProfile as eP
from .forms import editProfileSiswa as ePS
from .models import User

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, sortBy
from django.db.models.functions import Lower



def beranda(response):
	if response.user.is_authenticated :
		user = User.objects.get(username=response.user.get_username())
		allUser = User.objects.all()
		if response.method == 'POST' :
			form = sortBy(response.POST)
			if form.is_valid(): 
				if form.cleaned_data['sort_By'] == 'Universitas' :
					allUser = User.objects.all().order_by(Lower('univ'))
					if form.cleaned_data['search'] != "" :
						allUser = User.objects.filter(univ__contains=form.cleaned_data['search'])
					return render(response, 'web/beranda.html',{'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : allUser, 'form' : form})
				elif form.cleaned_data['sort_By'] == 'Jurusan' :
					allUser = User.objects.all().order_by(Lower('jurusan'))
					if form.cleaned_data['search'] != "" :
						allUser = User.objects.filter(jurusan__contains=form.cleaned_data['search'])
					return render(response, 'web/beranda.html',{'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : allUser, 'form' : form})
				elif form.cleaned_data['sort_By'] == 'Nama' :
					allUser = User.objects.all().order_by(Lower('nama'))
					if form.cleaned_data['search'] != "" :
						allUser = User.objects.filter(nama__contains=form.cleaned_data['search'])
					return render(response, 'web/beranda.html',{'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : allUser, 'form' : form})
		else :
			form = sortBy()
			return render(response, 'web/beranda.html',{'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : allUser, 'form' : form})

	else :
		return redirect('login')

def profile(response, username) :
	if response.user.is_authenticated :
		usernameindatabase = User.objects.filter(username=username).first()
		userlogin = User.objects.get(username=response.user.get_username())
		if usernameindatabase != None and usernameindatabase.jurusan != "-" and usernameindatabase.status == 'alumni':
			if username == userlogin.username :
				return render(response, 'web/Myprofile.html', {'user' : usernameindatabase})
			else :
				return render(response, 'web/profile.html', {'user' : usernameindatabase})
		elif usernameindatabase != None and usernameindatabase.status == 'siswa':
			if  username == userlogin.username :
				return render(response, 'web/MyprofileSiswa.html', {'user' : usernameindatabase})
			else :
				return render(response, 'web/profileSiswa.html', {'user' : usernameindatabase})
		else  :
			return render(response, 'web/profileNotFound.html')
	else :
		return redirect('login')

def editProfile(request,username):
	if request.user.is_authenticated:
		user = User.objects.get(username=request.user.get_username())
		usernameindatabase = User.objects.filter(username=username).first()
		if usernameindatabase != None and user.username == usernameindatabase.username :
			if usernameindatabase.status == 'alumni':
				if request.method == "POST": 
					form = eP(request.POST, instance=user)
					if form.is_valid() :
						form.save()
						return redirect('web-Profile',username=user.username)
				else :
					user = User.objects.get(username=request.user.get_username())
					form = eP(instance=user)
			else :
				if request.method == "POST": 
					form = ePS(request.POST, instance=user)
					if form.is_valid() :
						form.save()
						return redirect('web-Profile',username=user.username)
				else :
					user = User.objects.get(username=request.user.get_username())
					form = ePS(instance=user)

			return render(request, 'web/editprofile.html', {"form" : form})
		else :
			return redirect('web-EditProfile',username=user.username)

	else :
		return redirect('login')

def statistik(request) :
	return render(request, 'web/statistik.html')


def register (response):
	if response.user.is_authenticated:
		return redirect('web-Beranda')

	else :
		if response.method == "POST" :
			form = UserRegistrationForm(response.POST)
			if form.is_valid() and User.objects.filter(username=form.cleaned_data["username"]).first() != None:
				form.save()
				usernameindatabase = User.objects.get(username=form.cleaned_data['username'])
				usernameindatabase.status = form.cleaned_data['status']
				usernameindatabase.save()
				return render(response, "registration/register.html", {'form':form, 'res' : 1})
			else :
				return render(response, "registration/register.html", {'form':form, 'res' : -1})
		else :
			form = UserRegistrationForm()
	
	return render(response, "registration/register.html", {'form':form})
