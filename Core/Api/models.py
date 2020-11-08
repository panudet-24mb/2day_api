from django.db import models
import uuid
import datetime
# Create your models here.
class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=80, blank=True, null=True)
    class Meta:
        db_table = "status"
    def __str__(self):
        return str(self.status_name)

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=80, blank=True, null=True)
    class Meta:
        db_table = "department"
    def __str__(self):
        return str(self.department_name)
    
class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=80, blank=True, null=True)
    class Meta:
        db_table = "position"
    def __str__(self):
        return str(self.position_name)
    
    
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_public_id = models.UUIDField(
         default=uuid.uuid4, editable=False ,unique = True
    )
    company_name = models.CharField(max_length=180, blank=True, null=True , unique =True)
    company_is_active = models.BooleanField(default=False)
    created_on = models.DateField( default=datetime.datetime.now)
    class Meta:
        db_table = "company"
    def __str__(self):
        return self.company_name
    
class Users(models.Model):
    users_id = models.AutoField(primary_key=True)
    users_uuid = models.UUIDField(
         default=uuid.uuid4, editable=False ,unique = True
    )
    users_citizen_id = models.CharField(max_length=14, unique=True , blank=False, null=False )
    class Meta:
        db_table = "users"
    def __str__(self):
        return str(self.users_citizen_id)

class Userdetails(models.Model):
    userdetails_id = models.AutoField(primary_key=True)
    users = models.OneToOneField(Users, models.CASCADE)
    userdetails_firstname = models.CharField(max_length=80, blank=True, null=True)
    userdetails_lastname = models.CharField(max_length=80, blank=True, null=True)
    userdetails_phone = models.CharField(max_length=80, blank=True, null=True)
    userdetails_email = models.CharField(max_length=80, blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True ,on_delete= models.CASCADE)
    position = models.ForeignKey(Position, blank=True, null=True,on_delete= models.CASCADE)
    userdetails_avatar = models.CharField(max_length=104, blank=True, null=True)
    class Meta:
        db_table = "userdetails"
    def __str__(self):
        return str(self.userdetails_id)
    
class Company_has_users(models.Model):
    comapny_has_users_id = models.AutoField(primary_key=True)
    users = models.ForeignKey(Users, models.CASCADE)
    company = models.ForeignKey(Company, models.CASCADE)
    created = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "company_has_users"
    def __str__(self):  
        return str(self.comapny_has_users_id)
    
class Token(models.Model):
    token_id = models.AutoField(primary_key=True)
    users = models.ForeignKey(Users, models.CASCADE)
    token =  models.CharField(max_length=255, unique=True , blank=False, null=False )
    token_created = models.DateTimeField()
    token_active = models.BooleanField(default=False)
    class Meta:
        db_table = "token"
    def __str__(self):
        return str(self.token)