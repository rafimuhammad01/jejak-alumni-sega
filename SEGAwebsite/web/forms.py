from django import forms
from .models import User as myUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import Textarea, CharField

from .models import PerguruanTinggi

from .models import PerguruanTinggi

class UserRegistrationForm(UserCreationForm):
	status = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'Radio'}), choices=(('alumni','Alumni'),('siswa','Siswa'),('gapyear/kerja', 'Gap Year/Kerja')))

class editProfile(forms.ModelForm):
	status = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'Radio'}), choices=(('alumni','Alumni'),('siswa','Siswa'),('gapyear/kerja', 'Gap Year/Kerja')))
	jalur = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'Radio'}), choices=(('SNMPTN','SNMPTN'),('SBMPTN','SBMPTN'),('Mandiri', 'Mandiri'),('Lainnya', 'Lainnya')))
	univ = forms.ModelChoiceField(queryset=PerguruanTinggi.objects.all().order_by("nama"))
	class Meta :
		model = myUser
		fields = [
			'kontak',
			'jurusan',
			'fakultas',
			'univ',
			'jalur',
			'skor_1',
			'skor_2',
			'tahunlulus',
			'tahunmasuk',
			'refrensi',
			'pesan',
			'status'
			]
		widgets = {
			'pesan': Textarea(attrs={'cols':35}),'refrensi': Textarea(attrs={'cols':35}), 'univ' : forms.Select(attrs={'size' : '10px'})
		}

	def clean_jurusan(self):
		return self.cleaned_data["jurusan"].title()

	def clean_kontak(self):
		return self.cleaned_data['kontak'].lower()

	def clean_fakultas(self) :
		return self.cleaned_data['fakultas'].title()

class editProfileSiswa(forms.ModelForm):
	status = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'Radio'}), choices=(('alumni','Alumni'),('siswa','Siswa'),('gapyear/kerja', 'Gap Year/Kerja')))
	class Meta :
		model = myUser
		fields = [
			'kontak',
			'status'
			]


class sortBy(forms.Form):
	CHOICES = (('Universitas', 'Universitas'),('Jurusan','Jurusan'),('Nama','Nama'))
	sort_By = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
	search = forms.CharField(max_length=50, required=False)

#	kontak = forms.CharField(max_length=50,  label="Kontak", widget=forms.TextInput(attrs={'placeholder':'none'}))
#	jurusan = forms.CharField(max_length=50, label="Jurusan")
#	fakultas = forms.CharField(max_length=50, label="Fakultas")
#	univ = forms.CharField(max_length=50, label="Universitas")
#	jalur = forms.CharField(max_length=50, label="Jalur Masuk")
#	skor_1 = forms.CharField(max_length=50, label="Skor Utbk 1")
#	skor_2 = forms.CharField(max_length=50, label="Skor Utbk 2")
#	tahunlulus = forms.CharField(max_length=50, label="Tahun Lulus")
#	tahunmasuk = forms.CharField(max_length=50, label="Tahun masuk")
#	refrensi = forms.CharField(max_length=50, label="Refrensi")
#	pesan = forms.CharField(max_length=200, label="Pesan")
