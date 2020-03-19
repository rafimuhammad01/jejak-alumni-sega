from django.db import models
from django.contrib.auth.models import User as u

class User(models.Model) :
	nama = models.CharField("Nama",max_length=50)
	nis = models.IntegerField("Nis")
	username = models.CharField("Username",max_length=50)
	status = models.CharField("Status",max_length=50, default="-")
	kontak = models.CharField("Kontak",max_length=50, default="-")
	jurusan = models.CharField("Jurusan",max_length=50, default="-")
	fakultas = models.CharField("Fakultas",max_length=50, default="-")
	univ = models.CharField("Universitas",max_length=50, default="-")
	jalur = models.CharField("Jalur",max_length=50, default="-")
	skor_1 = models.CharField("Skor 1",max_length=50, default="-")
	skor_2 = models.CharField("Skor 2",max_length=50, default="-")
	tahunlulus = models.CharField("Tahun Lulus", max_length=50, default="-")
	tahunlulus = models.CharField("Tauhun Lulus", max_length=50, default="-")
	tahunmasuk = models.CharField("Tahun Masuk",max_length=50, default="-")
	refrensi = models.TextField("Refrensi",max_length=200, default="-")
	pesan = models.TextField("Pesan",max_length=200, default="-")
	image = models.ImageField("Foto",default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return "{} ({})".format(self.nama, self.nis)

class PerguruanTinggi(models.Model) :
	nama = models.CharField('Nama',max_length=100)
	status = models.CharField('Status', max_length=50)

	def __str__(self):
		return "{}".format(self.nama)