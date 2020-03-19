from django.shortcuts import render,redirect
from .forms import editProfile as eP
from .forms import editProfileSiswa as ePS
from .models import User, PerguruanTinggi

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, sortBy
from django.db.models.functions import Lower
from django.contrib import messages

from django.views.generic import TemplateView
import random


def aboutUs(response):
	if response.user.is_authenticated :
		user = User.objects.get(username=response.user.get_username())
		allUser = User.objects.all()
		return render(response, 'web/aboutUs.html',{'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : allUser})
	else :
		return redirect('login')

def beranda(response):
	if response.user.is_authenticated :
		user = User.objects.get(username=response.user.get_username())
		allUser = User.objects.all().order_by('nama')
		if user.kontak != "-" and user.jurusan != "-" and user.fakultas != "-" and user.univ != "-" and user.jalur != "-"  and user.tahunlulus != "-" and user.tahunmasuk != "-" and user.refrensi != "-" and user.pesan != "-" :
			if response.method == 'POST' :
				dataFix = []
				filtering = User.objects.all().order_by('nama')
				if response.POST.get('Fakultas') != '*':
					filtering = User.objects.filter(fakultas__contains=response.POST.get('Nama_F'))

				if response.POST.get("Jurusan") != "*" :
					filtering = filtering.filter(jurusan__contains=response.POST.get('Nama_J'))

				if response.POST.get("Tahun_M") != "*" :
					filtering = filtering.filter(tahunmasuk__contains=response.POST.get('Tahun_M'))

				if response.POST.get("Jalur_M") != "*" :
					filtering = filtering.filter(jalur__contains=response.POST.get('Jalur_M'))

				if response.POST.get("Univ") != "*" :
					if response.POST.get("Univ") != "PT" :
						for i in filtering :
							if i.univ in PerguruanTinggi.objects.filter(status=response.POST.get('Univ')) :
								dataFix.append(i)
						return render(response, 'web/beranda.html',{'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : dataFix})
					
					elif response.POST.get('Univ') == 'PT' :
						filtering = filtering.filter(univ__contains=response.POST.get('Nama_P'))

				return render(response, 'web/beranda.html',{'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : filtering})
			
			else :
				return render(response, 'web/beranda.html',{'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : allUser})
		else :
			messages.info(response, 'Silahkan Lengkapi Profile Anda')
			return redirect('web-EditProfile', username=user.username)
	else :
		return redirect('login')

def profile(response, username) :
	if response.user.is_authenticated :
		usernameindatabase = User.objects.filter(username=username).first()
		userlogin = User.objects.get(username=response.user.get_username())
		if usernameindatabase != None and usernameindatabase.status == 'alumni':
			if username == userlogin.username :
				return render(response, 'web/Myprofile.html', {'user' : usernameindatabase})
			elif usernameindatabase.jurusan == "-" :
				 return render(response, 'web/profileNotFound.html')
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
					univ = PerguruanTinggi.objects.get(nama=user.univ)
					form = eP(instance=user, initial = {'univ' : univ.pk})
			else :
				if request.method == "POST": 
					form = ePS(request.POST, instance=user)
					if form.is_valid() :
						form.save()
						return redirect('web-Profile',username=user.username)
				else :
					user = User.objects.get(username=request.user.get_username())
					form = ePS(instance=user)

			return render(request, 'web/editprofile.html', {"form" : form,'user' : usernameindatabase})
		else :
			return redirect('web-EditProfile',username=user.username)

	else :
		return redirect('login')

def statistikUniv(response) : 
	if response.user.is_authenticated:
		user = User.objects.get(username=response.user.get_username())
		allUser = User.objects.all()		 
		Univ = {} #dict buat nyimpen univ dan jumlah
		listUniv = [] #list buat simpen Univ maksimal 10
		jumlahUniv = [] #list buat jumlah Univ maksimal 10
		#Note : univ di listUniv index 0, jumlahnya ada di jumlahUniv index 0 juga, jadi indexnya sama

		sisa = 0
		total = 0 #Variabel ini berguna kalo jumlah univnya lebih dari 9, jadi nanti sisa univ akan masuk ke "Lainnya"
		#For loop buat ngisi dict Univ
		for item in allUser :
			if item.univ in Univ and item.univ != "-":
				Univ[item.univ] += 1
			elif item.univ != "-":
				Univ[item.univ] = 1
		Univ = sorted(Univ.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
		
		for val in Univ :
			sisa += val[1]
		total = sisa
		if len(Univ) > 10 :
			for item in Univ :
				if len(listUniv) == 9 : #berhubung cu
					break
				listUniv.append(item[0])
				jumlahUniv.append(item[1])
				sisa -= item[1]
			listUniv.append('Lainnya')
			jumlahUniv.append(sisa)
		else :
			for item in Univ :
				listUniv.append(item[0])
				jumlahUniv.append(item[1])
		persenUniv = []
		persenAtas = [] #buat gambar diagram batang
		for jumlah in jumlahUniv :
			persenUniv.append(round(jumlah/total*100))
			persenAtas.append(round(100-(jumlah/total*100)))

		listColor = ["#0f1c26;","#D9F1F1;","#008EA0;","#7FACD6;","#B6E3E9;","#6593F5;","#eee;","#ddd;","#00dae6;","#4F97A3;"]
		hasilBar = zip(persenUniv,persenAtas,listColor)
		hasilKeterangan = zip(listUniv,persenUniv,listColor)
		hasilTable = zip(listUniv,jumlahUniv)

		return render(response, 'web/statistikUniv.html', {"hasilBar" : hasilBar,"hasilKeterangan" : hasilKeterangan, "hasilTable" : hasilTable,'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : allUser})
	else :
		return redirect('login')

def statistikJalur(response) : 
	if response.user.is_authenticated:
		user = User.objects.get(username=response.user.get_username())
		allUser = User.objects.all()
		Jalur = {} #dict buat nyimpen jalur dan jumlah
		listJalur = [] #list buat simpen Univ maksimal 10
		jumlahJalur = [] #list buat jumlah Univ maksimal 10
		#Note : univ di listUniv index 0, jumlahnya ada di jumlahUniv index 0 juga, jadi indexnya sama

		sisa = 0
		total = 0 #Variabel ini berguna kalo jumlah univnya lebih dari 9, jadi nanti sisa univ akan masuk ke "Lainnya"
		#For loop buat ngisi dict Univ
		for item in allUser :
			if item.jalur in Jalur and item.jalur != "-":
				Jalur[item.jalur] += 1
			elif item.jalur != "-":
				Jalur[item.jalur] = 1
		Jalur = sorted(Jalur.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
		
		for val in Jalur :
			sisa += val[1]
		total = sisa
		if len(Jalur) > 3 :
			for item in Jalur :
				if len(listJalur) == 3 : #berhubung cu
					break
				listJalur.append(item[0])
				jumlahJalur.append(item[1])
				sisa -= item[1]
			listJalur.append('Lainnya')
			jumlahJalur.append(sisa)
		else :
			for item in Jalur :
				listJalur.append(item[0])
				jumlahJalur.append(item[1])
		persenJalur = []
		persenAtas = [] #buat gambar diagram batang
		for jumlah in jumlahJalur :
			persenJalur.append(round(jumlah/total*100))
			persenAtas.append(round(100-(jumlah/total*100)))

		listColor = ["#0f1c26;","#D9F1F1;","#008EA0;","#7FACD6;","#B6E3E9;","#6593F5;","#eee;","#ddd;","#00dae6;","#4F97A3;"]

		hasilBar = zip(persenJalur,persenAtas,listColor)
		hasilKeterangan = zip(listJalur,persenJalur,listColor)
		hasilTable = zip(listJalur,jumlahJalur)

		return render(response, 'web/statistikJalur.html', {"hasilBar" : hasilBar,"hasilKeterangan" : hasilKeterangan, "hasilTable" : hasilTable,'nama' : user.nama, 'username' : user.username, 'nis' : user.nis, 'data' : allUser})
	else :
		return redirect('login')


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
				messages.success(response, 'Register Berhasil')
				return render(response, "registration/register.html", {'form':form, 'res' : 1})
			else :
				messages.warning(response, 'Register Gagal')
				return render(response, "registration/register.html", {'form':form, 'res' : -1})
		else :
			form = UserRegistrationForm()
	
	return render(response, "registration/register.html", {'form':form})


class StatistikUnivChartView (TemplateView) :
	template_name = 'web/statistikUniv.html'

	def get_context_data(self, **kwargs) :
		context = super().get_context_data(**kwargs)
		total = {}

		subject = []
		user = User.objects.exclude(univ='-')
		for item in user :
			if item.univ not in total :
				total[item.univ] = 1
			else :
				total[item.univ] += 1

		warnaBackground = []
		warnaBorder = []
		for item in range(len(total)) :
			r = random.randint(0,255)
			g = random.randint(0,255)
			b = random.randint(0,255)
			a1 = 0.5
			a2 = 1
			
			warnaBackground.append('rgba('+ str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a1) + ')')
			warnaBorder.append('rgba('+ str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a2) + ')')

		context['label'] = total
		context['total'] = total.values()
		context['warnaBackground'] = warnaBackground
		context['warnaBorder'] = warnaBorder
		return context

class StatistikJalurChartView (TemplateView) :
	template_name = 'web/statistikJalur.html'

	def get_context_data(self, **kwargs) :
		context = super().get_context_data(**kwargs)
		total = {}

		subject = []
		user = User.objects.exclude(jalur='-')
		for item in user :
			if item.jalur not in total :
				total[item.jalur] = 1
			else :
				total[item.jalur] += 1

		warnaBackground = []
		warnaBorder = []
		for item in range(len(total)) :
			r = random.randint(0,255)
			g = random.randint(0,255)
			b = random.randint(0,255)
			a1 = 0.5
			a2 = 1
			
			warnaBackground.append('rgba('+ str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a1) + ')')
			warnaBorder.append('rgba('+ str(r) + ", " + str(g) + ", " + str(b) + ", " + str(a2) + ')')

		context['label'] = total
		context['total'] = total.values()
		context['warnaBackground'] = warnaBackground
		context['warnaBorder'] = warnaBorder
		return context




