from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from dbsirm.utils import get_current_user

# Create your models here.
from decimal import Decimal
#almacenes
import os

def generate_pathfoto(instance, filename):
    folder = "fotografias/" + str(instance.created_by) 
    return os.path.join("imagenes", folder, filename)

def generate_pathimg(instance, filename):
    folder = "images/obj/"
    return os.path.join("imagenes", folder, filename)

def generate_pathdoc(instance, filename):
    folder = "comprobantes/" + str(instance.created_by) 
    return os.path.join("documentos", folder, filename)
#Almacena los diferentes del sistema activo, inactivo, oculto o eliminado
class EstadoSistemas(models.Model):
	codigo =  models.CharField(max_length=30)
	nombre =  models.CharField(max_length=30)
	created_by = models.ForeignKey('auth.User',related_name='EstadoSistemas_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='EstadoSistemas_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(EstadoSistemas, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.nombre

#Almacena todos los objetos necesitados para el funcionamiento escalable del sistema
class ObjetosSistemas(models.Model):
	codigo =  models.CharField(max_length=30)
	nombre =  models.CharField(max_length=50)
	created_by = models.ForeignKey('auth.User',related_name='ObjetosSistemas_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='ObjetosSistemas_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(ObjetosSistemas, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.nombre

#Almacena todos los valores de los objectos del sistema
class ValoresObjetosSistemas(models.Model):
	idobjetossistemas = models.ForeignKey('dbsirm.ObjetosSistemas',related_name='ValoresObjetosSistemas_idobjetossistemas', on_delete=models.PROTECT, null=False,blank=False) 
	codigo =  models.CharField(max_length=50,unique=False)
	valor =  models.CharField(max_length=100)
	img = models.ImageField(upload_to=generate_pathimg, blank=True, null=True)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='ValoresObjetosSistemas_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='ValoresObjetosSistemas_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='ValoresObjetosSistemas_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(ValoresObjetosSistemas, self).save(*args, **kwargs)
	class Meta:
		ordering = ['valor']
	def __str__(self):
		return self.valor

#Almacena todos los datos de las usuarias
class PerfilUsuarias(models.Model):
	idtipoidentidad = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_idtipoidentidad', blank=True, null=True,on_delete=models.CASCADE)
	idaldeanacimiento =  models.ForeignKey('dbsirm.Aldeas', blank=True, null=True,on_delete=models.CASCADE)
	idmunicipio =  models.ForeignKey('dbsirm.Municipio', blank=True, null=True,on_delete=models.CASCADE)
	ndocumento =  models.CharField(max_length=30)
	nombres =  models.CharField(max_length=60)
	primerapellido =  models.CharField(max_length=30)
	segundoapellido =  models.CharField(max_length=30,blank=True, null=True)
	fechanacimiento = models.DateField(verbose_name="Fecha de nacimiento")
	idestadocivil = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_idestadocivil', blank=True, null=True,on_delete=models.CASCADE)
	iddiscapacidad = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_iddiscapacidad', blank=True, null=True,on_delete=models.CASCADE)
	idgenero = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_idgenero', blank=True, null=True,on_delete=models.CASCADE)	
	fotografia = models.ImageField(upload_to=generate_pathfoto,default='media/imagenes/img.jpg', blank=True, null=True)
	alias =  models.CharField(max_length=30,blank=True, null=True)
	especificaciondiscapacidad =  models.CharField(max_length=30,blank=True, null=True)
	tieneempleo =  models.BooleanField(default=False)
	esmigrante =  models.BooleanField(default=False)
	tienehijos =  models.BooleanField(default=False)
	migrante =  models.BooleanField(default=False)
	desplazada =  models.BooleanField(default=False)
	nhijos =  models.IntegerField(default=0)
	npersonas =  models.IntegerField(default=0)
	idprofesionoficio = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_idprofesionoficio', blank=True, null=True,on_delete=models.CASCADE)
	tienediscapacidad =  models.BooleanField(default=False)
	disponibilidadcurso =  models.BooleanField(default=False)
	huella =  models.CharField(max_length=200,blank=True, null=True)
	correo = models.EmailField(max_length=75,blank=True, null=True)
	telefono =  models.CharField(max_length=20,blank=True, null=True)
	celular =  models.CharField(max_length=20,blank=True, null=True)
	idescolaridad =  models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_idescolaridad', blank=True, null=True,on_delete=models.CASCADE) 
	idetnico =  models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_idetnico', blank=True, null=True,on_delete=models.CASCADE) 
	imgcodigoqr =  models.CharField(max_length=200,blank=True, null=True)
	idhorarioatencion =  models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_idhorarioatencion', blank=True, null=True,on_delete=models.CASCADE) 
	idtipoformacion =  models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_idtipoformacion', blank=True, null=True,on_delete=models.CASCADE) 
	idcomoseentero =  models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='PerfilUsuarias_idcomoseentero', blank=True, null=True,on_delete=models.CASCADE) 
	estaencentro =  models.BooleanField(default=False)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='PerfilUsuarias_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='PerfilUsuarias_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='PerfilUsuarias_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(PerfilUsuarias, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.nombres


#relacion 1 a muchos de los empleos de las usuarias
class EmpleosUsuarias(models.Model):
	idusuaria =  models.ForeignKey('dbsirm.PerfilUsuarias', blank=True, null=True,on_delete=models.CASCADE)
	lugarempleo =  models.CharField(max_length=200)
	idrangosalarial = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='EmpleosUsuarias_idrangosalarial', blank=True, null=True,on_delete=models.CASCADE)
	idtipoempresa = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='EmpleosUsuarias_idtipoempresa', blank=True, null=True,on_delete=models.CASCADE)
	cargo =  models.CharField(max_length=200)
	direccion =  models.TextField()
	telefonoempleo =  models.CharField(max_length=100,blank=True, null=True)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='EmpleosUsuarias_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='EmpleosUsuarias_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='EmpleosUsuarias_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(EmpleosUsuarias, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.lugarempleo

#relacion 1 a muchos de las direcciones de las usuarias
class DireccionesUsuarias(models.Model):
	idusuaria =  models.ForeignKey('dbsirm.PerfilUsuarias', blank=True, null=True,on_delete=models.CASCADE)
	idaldea =  models.ForeignKey('dbsirm.Aldeas', blank=True, null=True,on_delete=models.CASCADE)
	idmunicipio =  models.ForeignKey('dbsirm.Municipio', blank=True, null=True,on_delete=models.CASCADE)
	nombrecolonia =  models.CharField(max_length=50,blank=True, null=True)
	bloquesector =  models.CharField(max_length=50,blank=True, null=True)
	ncasa =  models.CharField(max_length=10,blank=True, null=True)
	direccionexacta =  models.TextField(blank=True, null=True)
	latitud =  models.CharField(max_length=30,blank=True, null=True)
	longitud =  models.CharField(max_length=30,blank=True, null=True)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='DireccionesUsuarias_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='DireccionesUsuarias_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='DireccionesUsuarias_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(DireccionesUsuarias, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.idusuaria.nombres

#Almacena las Persona con la relacion de las usuarias acompañantes/hijos/pareja/otros familiares 
class Personas(models.Model):
	idusuaria =  models.ForeignKey('dbsirm.PerfilUsuarias',related_name='Personas_idusuaria', blank=True, null=True,on_delete=models.CASCADE) 
	ndocumento =  models.CharField(max_length=30,unique=True,blank=True,null=True)
	nombre =  models.CharField(max_length=100)
	sexo =  models.CharField(max_length=15)
	idetnico =  models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='Personas_idetnico', blank=True, null=True,on_delete=models.CASCADE) 
	nacimiento = models.DateField(blank=True, null=True)
	vivejuntousuaria =  models.BooleanField(default=False)
	estaencentro =  models.BooleanField(default=False)
	idparentesco =  models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='Personas_idparentesco', blank=True, null=True,on_delete=models.CASCADE) 
	fotografia = models.ImageField(upload_to=generate_pathfoto,default='img.jpg', blank=True, null=True)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='Personas_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='Personas_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='Personas_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(Personas, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.nombre

#Almacena el Historial de servicios brindados a las Personas
class PersonasServiciosHistorial(models.Model):
	idcomponente = models.ForeignKey('dbsirm.ComponentesServiciosIndicados',related_name='PersonasServiciosHistorial_idcomponente', blank=True, null=True,on_delete=models.CASCADE) 
	idpersonas =  models.ForeignKey('dbsirm.Personas',related_name='PersonasServiciosHistorial_idpersonas', blank=True, null=True,on_delete=models.CASCADE) 
	descripcion = models.TextField(blank=False)
	created_by = models.ForeignKey('auth.User',related_name='PersonasServiciosHistorial_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='PersonasServiciosHistorial_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(PersonasServiciosHistorial, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.descripcion


#Almacena las Aldeas del país
class Aldeas(models.Model):
	codigo =  models.CharField(max_length=200)
	nombre =  models.CharField(max_length=200)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='Aldeas_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	idmunicipio =  models.ForeignKey('dbsirm.Municipio', blank=True, null=True,on_delete=models.CASCADE)
	created_by = models.ForeignKey('auth.User',related_name='Aldeas_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='Aldeas_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(Aldeas, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.nombre

#Almacena los municipios de país
class Municipio(models.Model):
	codigo =  models.CharField(max_length=200)
	nombre =  models.CharField(max_length=200)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='Municipio_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	iddepartamento =  models.ForeignKey('dbsirm.Departamento', blank=True, null=True,on_delete=models.CASCADE)
	created_by = models.ForeignKey('auth.User',related_name='Municipio_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='Municipio_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(Municipio, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.nombre

#Almcena los departamentos del País
class Departamento(models.Model):
	codigo =  models.CharField(max_length=200)
	nombre =  models.CharField(max_length=200)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='Departamento_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='Departamento_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='Departamento_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(Departamento, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.nombre

#Almacena el tiempo que las personas la acompañado
class RegistroAcompanante(models.Model):
	idccm =  models.ForeignKey('funcionarias.CentroCiudadMujer',related_name='RegistroAcompanante_idccm', blank=True, null=True,on_delete=models.PROTECT) 
	idpersonas =  models.ForeignKey('dbsirm.Personas',related_name='RegistroAcompanante_idpersonas', blank=True, null=True,on_delete=models.CASCADE) 
	idservicios =  models.ForeignKey('dbsirm.ServiciosIndicados',related_name='RegistroAcompanante_idserviciosindicados', blank=True, null=True,on_delete=models.CASCADE) 
	idestadoderivacion = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='RegistroAcompanante_idtiporegistro', blank=True, null=True,on_delete=models.CASCADE)
	idtipoderivacion = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='RegistroAcompanante_idtipoderivacion', blank=True, null=True,on_delete=models.CASCADE)
	idtipoacompante = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='RegistroAcompanante_idtipoacompante', blank=True, null=True,on_delete=models.CASCADE)
	nota =  models.CharField(max_length=200)
	horadeinicio = models.TimeField(blank=True, null=True)
	horafinalizado = models.TimeField(blank=True, null=True) 
	antendidapor = models.ForeignKey('funcionarias.PerfilFuncionarias',related_name='RegistroAcompanante_idfuncionarias', blank=True, null=True,on_delete=models.PROTECT) 
	created_by = models.ForeignKey('auth.User',related_name='RegistroAcompanante_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='RegistroAcompanante_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(RegistroAcompanante, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.idpersonas.nombre

#Almacena los modulos de Ciudad mujer
class Modulos(models.Model):
	codigo =  models.CharField(max_length=20)
	titulo =  models.CharField(max_length=200)
	sigla =  models.CharField(max_length=30)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='Modulos_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='Modulos_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='Modulos_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(Modulos, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.titulo


#Almacena todos los servicios por modulo
class ComponentesServiciosIndicados(models.Model):
	titulo =  models.CharField(max_length=200)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='Componentes_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	idservicioindicado =  models.ForeignKey('dbsirm.ServiciosIndicados',related_name='Componentes_idservicioindicado', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='Componentes_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='Componentes_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(ComponentesServiciosIndicados, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.titulo

#Almacena todos los servicios por modulo
class ServiciosIndicados(models.Model):
	codigo =  models.CharField(max_length=20,unique=True)
	titulo =  models.CharField(max_length=200)
	descripcion =  models.CharField(max_length=200,blank=True, null=True)
	emergencia = models.BooleanField(default=False)
	idtiposervicio = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='ServiciosIndicados_idtiposervicio', on_delete=models.PROTECT, null=False,blank=False) 
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='ServiciosIndicados_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	idmodulos =  models.ForeignKey('dbsirm.Modulos',related_name='ServiciosIndicados_idmodulos', blank=True, null=True,on_delete=models.CASCADE) 
	idinstitucion =  models.ForeignKey('dbsirm.Instituciones',related_name='Instituciones_idmodulos', blank=True, null=True,on_delete=models.CASCADE) 
	idestrategia = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='ServiciosIndicados_idestrategia', blank=True, null=True,on_delete=models.CASCADE)	
	created_by = models.ForeignKey('auth.User',related_name='ServiciosIndicados_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='ServiciosIndicados_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(ServiciosIndicados, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.titulo

#Estrategias_MEC
class InscripcionesMEC(models.Model):
	year =  models.CharField(max_length=20)
	idhojaruta =  models.ForeignKey('dbsirm.HojaDeRuta',related_name='InscripcionesMEC_idhojaruta', blank=True, null=True,on_delete=models.CASCADE) 
	idestrategia = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='InscripcionesMEC_idestrategia', blank=True, null=True,on_delete=models.CASCADE)	
	idccm =  models.ForeignKey('funcionarias.CentroCiudadMujer',related_name='InscripcionesMEC_idccm', blank=True, null=True,on_delete=models.PROTECT) 
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='InscripcionesMEC_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='InscripcionesMECcreated_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='InscripcionesMEC_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(InscripcionesMEC, self).save(*args, **kwargs)
	class Meta:
		ordering = ['year']
	def __str__(self):
		return self.year

#Estrategias_MEC
class AgendaMEC(models.Model):
	titulo =  models.CharField(max_length=200)
	hora = models.TimeField(blank=True, null=True)
	fecha = models.DateField()
	descripcion = models.TextField(blank=True)
	idestrategia = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='AgendaMEC_idestrategia', blank=True, null=True,on_delete=models.CASCADE)	
	idccm =  models.ForeignKey('funcionarias.CentroCiudadMujer',related_name='AgendaMEC_idccm', blank=True, null=True,on_delete=models.PROTECT) 
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='AgendaMEC_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='AgendaMEC_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='AgendaMEC_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(AgendaMEC, self).save(*args, **kwargs)
	class Meta:
		ordering = ['fecha']
	def __str__(self):
		return self.idestrategia.valor

#Instituciones
class Instituciones(models.Model):
	codigo =  models.CharField(max_length=20)
	titulo =  models.CharField(max_length=200)
	sigla =  models.CharField(max_length=20)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='Instituciones_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='Instituciones_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='Instituciones_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(Instituciones, self).save(*args, **kwargs)
	class Meta:
		ordering = ['codigo']
	def __str__(self):
		return self.titulo

#Almacena todos las opciones  problemas identificados en la orientacion 
class ProblemasIdenticados(models.Model):
	codigo =  models.CharField(max_length=20)
	titulo =  models.CharField(max_length=200)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='ProblemasIdenticados_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	idmodulos =  models.ForeignKey('dbsirm.Modulos',related_name='ProblemasIdenticados_idmodulos', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='ProblemasIdenticados_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='ProblemasIdenticados_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(ProblemasIdenticados, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.titulo

#Almacena todas las opciones razones de visista relacionadas con los problemas identificados 
class RazonesVisita(models.Model):
	codigo =  models.CharField(max_length=20)
	titulo =  models.CharField(max_length=200)
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='RazonesVisita_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	idproblemasidenticados =  models.ForeignKey('dbsirm.ProblemasIdenticados',related_name='RazonesVisita_idproblemasidenticados', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='RazonesVisita_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='RazonesVisita_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(RazonesVisita, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.titulo

#Almacena la unica hoja ruta por usuarias
class HojaDeRuta(models.Model):
	idusuaria =  models.ForeignKey('dbsirm.PerfilUsuarias',related_name='HojaDeRuta_idusuaria', blank=True, null=True,on_delete=models.CASCADE) 
	porcentaje =  models.CharField(max_length=200)
	created_by = models.ForeignKey('auth.User',related_name='HojaDeRuta_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='HojaDeRuta_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(HojaDeRuta, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.idusuaria.nombres

#Almacena las razones de visita en las hojas de ruta de las usuarias
class HojaDeRutaRazonesVista(models.Model):
	idhojaruta =  models.ForeignKey('dbsirm.HojaDeRuta',related_name='HojaDeRutaRazonesVista_idhojaruta', blank=True, null=True,on_delete=models.CASCADE) 
	idrazonesvisita =  models.ForeignKey('dbsirm.RazonesVisita',related_name='HojaDeRutaRazonesVista_idrazonesvisita', blank=True, null=True,on_delete=models.CASCADE) 
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='HojaDeRutaRazonesVista_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='HojaDeRutaRazonesVista_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='HojaDeRutaRazonesVista_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(HojaDeRutaRazonesVista, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.idhojaruta.idusuaria.nombres

#Almacena los servicios asignados a las Hoja de ruta 
class HojaDeRutaServicios(models.Model):
	idhojaruta =  models.ForeignKey('dbsirm.HojaDeRuta',related_name='HojaDeRutaServicios_idhojaruta', blank=True, null=True,on_delete=models.CASCADE) 
	idserviciosindicados =  models.ForeignKey('dbsirm.ServiciosIndicados',related_name='HojaDeRutaRazonesVista_idserviciosindicados', blank=True, null=True,on_delete=models.CASCADE) 
	estadoavance = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='HojaDeRutaServicios_idobjetossistemas', on_delete=models.PROTECT, null=False,blank=False) 
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='HojaDeRutaServicios_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	resultadoesperado =  models.CharField(max_length=200)
	created_by = models.ForeignKey('auth.User',related_name='HojaDeRutaServicios_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='HojaDeRutaServicios_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(HojaDeRutaServicios, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.idserviciosindicados.titulo

#Almacena el Historial de servicios brindados por cada servicio
class HojaDeRutaServiciosHistorial(models.Model):
	idhojaderutaservicioshistorial = models.ForeignKey('dbsirm.HojaDeRutaServicios',related_name='HojaDeRutaServiciosHistorial_idserviciosindicados', blank=True, null=True,on_delete=models.CASCADE) 
	idcomponente = models.ForeignKey('dbsirm.ComponentesServiciosIndicados',related_name='HojaDeRutaServiciosHistorial_idcomponente', blank=True, null=True,on_delete=models.CASCADE) 
	idregistrodeatencion =  models.ForeignKey('dbsirm.RegistroDeAtencion',related_name='HojaDeRutaServiciosHistorial_idregistrodeatencion', blank=True, null=True,on_delete=models.CASCADE) 
	descripcion = models.TextField(blank=False)
	idmedioatencionvirtual = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='HojaDeRutaServiciosHistorial_idmedioatencionvirtual', on_delete=models.PROTECT, null=True,blank=True) 
	documento =  models.FileField(upload_to=generate_pathdoc, null=True,blank=True)
	idtipohistorial = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='HojaDeRutaServiciosHistorial_idtipohistorial', on_delete=models.PROTECT, null=True,blank=True) 
	created_by = models.ForeignKey('auth.User',related_name='HojaDeRutaServiciosHistorial_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='HojaDeRutaServiciosHistorial_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(HojaDeRutaServiciosHistorial, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.descripcion

#Almacena las derivaciones y Registro De Atencion de usuarias
class RegistroDeAtencion(models.Model):	
	idccm =  models.ForeignKey('funcionarias.CentroCiudadMujer',related_name='RegistroDeAtencion_idccm', blank=True, null=True,on_delete=models.PROTECT) 
	idserviciosindicados =  models.ForeignKey('dbsirm.HojaDeRutaServicios',related_name='RegistroDeAtencion_idserviciosindicados', blank=True, null=True,on_delete=models.CASCADE) 
	idestadoderivacion = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='RegistroDeAtencion_idtiporegistro', blank=True, null=True,on_delete=models.CASCADE)
	idtipoderivacion = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='RegistroDeAtencion_idtiporeferencia', blank=True, null=True,on_delete=models.CASCADE)
	idtipousuaria = models.ForeignKey('dbsirm.ValoresObjetosSistemas',related_name='RegistroDeAtencion_idtipousuaria', blank=True, null=True,on_delete=models.CASCADE)
	nota =  models.CharField(max_length=200)
	idfuncionariareferida = models.ForeignKey('funcionarias.PerfilFuncionarias',related_name='PerfilFuncionarias_idfuncionarias', blank=True, null=True,on_delete=models.PROTECT) 
	creadapor = models.ForeignKey('funcionarias.PerfilFuncionarias',related_name='creadapor_idfuncionarias', blank=True, null=True,on_delete=models.PROTECT) 
	antendidapor = models.ForeignKey('funcionarias.PerfilFuncionarias',related_name='antendidapor_idfuncionarias', blank=True, null=True,on_delete=models.PROTECT) 
	horadeinicio = models.TimeField(blank=True, null=True)
	horadeatencion = models.TimeField(blank=True, null=True)
	horafinalizado = models.TimeField(blank=True, null=True) 
	programada =  models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	created_by = models.ForeignKey('auth.User',related_name='RegistroDeAtencion_created_by', on_delete=models.PROTECT, null=True,blank=True) 
	modified_by = models.ForeignKey('auth.User',related_name='RegistroDeAtencion_modified_by', on_delete=models.PROTECT, null=True,blank=True) 
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.created_by = user
			if not self.id:
				self.modified_by = user
			super(RegistroDeAtencion, self).save(*args, **kwargs)
	class Meta:
		ordering = ['created']
	def __str__(self):
		return self.idccm.nombre


class CitasHistorial(models.Model):
	idhojaderutaservicios = models.ForeignKey('dbsirm.HojaDeRutaServicios',related_name='CitasHistorial_idhojaderutaservicioshistorial', blank=True, null=True,on_delete=models.CASCADE) 
	idregistrodeatencioncreado =  models.ForeignKey('dbsirm.RegistroDeAtencion',related_name='CitasHistorial_idregistrodeatencioncreado', blank=True, null=True,on_delete=models.CASCADE) 
	idregistrodeatencionafinalizado =  models.ForeignKey('dbsirm.RegistroDeAtencion',related_name='CitasHistorial_idregistrodeatencionafinalizado', blank=True, null=True,on_delete=models.CASCADE) 
	citaatendida =  models.BooleanField(default=False)
	descripcion = models.TextField(blank=False)
	idfuncionaria = models.ForeignKey('funcionarias.PerfilFuncionarias',related_name='CitasHistorial_idfuncionaria', blank=True, null=True,on_delete=models.PROTECT) 
	hora = models.TimeField(blank=True, null=True)
	fecha = models.DateField()
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='CitasHistorial_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='CitasHistorial_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='CitasHistorial_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(CitasHistorial, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.descripcion

class CitasHistorialAcompanante(models.Model):
	idservicios =  models.ForeignKey('dbsirm.ServiciosIndicados',related_name='CitasHistorialAcompanante_idserviciosindicados', blank=True, null=True,on_delete=models.CASCADE) 
	idpersonas =  models.ForeignKey('dbsirm.Personas',related_name='CitasHistorialAcompanante_idpersonas', blank=True, null=True,on_delete=models.CASCADE) 
	citaatendida =  models.BooleanField(default=False)
	descripcion = models.TextField(blank=False)
	idfuncionaria = models.ForeignKey('funcionarias.PerfilFuncionarias',related_name='CitasHistorialAcompanante_idfuncionaria', blank=True, null=True,on_delete=models.PROTECT) 
	hora = models.TimeField(blank=True, null=True)
	fecha = models.DateField()
	estadosistema =  models.ForeignKey('dbsirm.EstadoSistemas',related_name='CitasHistorialAcompanante_estadosistema', blank=True, null=True,on_delete=models.CASCADE) 
	created_by = models.ForeignKey('auth.User',related_name='CitasHistorialAcompanante_created_by', on_delete=models.PROTECT, null=False,blank=False) 
	modified_by = models.ForeignKey('auth.User',related_name='CitasHistorialAcompanante_modified_by', on_delete=models.PROTECT, null=False,blank=False) 
	created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
	updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actulización")
	def save(self, *args, **kwargs):
		user = get_current_user()
		if user and user.is_authenticated:
			self.modified_by = user
			if not self.id:
				self.created_by = user
			super(CitasHistorialAcompanante, self).save(*args, **kwargs)
	class Meta:
		ordering = ['-created']
	def __str__(self):
		return self.descripcion