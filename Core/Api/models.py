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
    userdetails_bd = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True ,on_delete= models.CASCADE)
    position = models.ForeignKey(Position, blank=True, null=True,on_delete= models.CASCADE)
    userdetails_avatar = models.CharField(max_length=104, blank=True, null=True)
    class Meta:
        db_table = "userdetails"
    def __str__(self):
        return str(self.userdetails_id)
    
class Company_has_users(models.Model):
    company_has_users_id = models.AutoField(primary_key=True)
    users = models.ForeignKey(Users, models.CASCADE)
    company = models.ForeignKey(Company, models.CASCADE)
    created = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "company_has_users"
    def __str__(self):  
        return str(self.company_has_users_id)

class Company_has_usersdetails(models.Model):
    company_has_users_details_id = models.AutoField(primary_key=True)
    company_has_users = models.ForeignKey(Company_has_users, models.CASCADE , default=None)
    userdetails = models.ForeignKey(Userdetails, models.CASCADE )
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = "company_has_usersdetails"
    def __str__(self):  
        return str(self.company_has_users_details_id)

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
 

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_public_id =  models.UUIDField(
         default=uuid.uuid4, editable=False
    )
    company = models.ForeignKey(Company, models.CASCADE)
    admin_username = models.CharField(max_length=100, unique=True , blank=False, null=False )
    admin_password = models.CharField(max_length=80, blank=True, null=True)
    admin_is_active = models.BooleanField(default=False)
    class Meta:
        db_table = "admin"
    def __str__(self):
        return str(self.admin_public_id)
class News_category (models.Model):
    news_category_id = models.AutoField(primary_key=True)
    news_category_name = models.CharField(max_length=80, blank=True, null=True)
    class Meta:
        db_table = "news_category"
    def __str__(self):
        return str(self.news_category_name)
class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=180, blank=True, null=True)    
    news_excerpt = models.CharField(max_length=180, blank=True, null=True)    
    news_body = models.TextField(blank = True)
    news_image = models.CharField(max_length=180, blank=True, null=True)    
    news_category = models.ForeignKey(News_category, models.CASCADE)
    company = models.ForeignKey(Company, models.CASCADE)
    admin = models.ForeignKey(Admin, models.CASCADE)
    created = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    delete_at = models.DateTimeField(blank=True, null=True )
    class Meta:
        db_table = "news"
    def __str__(self):
        return str(self.news_title)

class Announcement(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    announcement_title  = models.CharField(max_length=180, blank=True, null=True)  
    announcement_body = models.TextField(blank = True)
    company = models.ForeignKey(Company, models.CASCADE)
    admin = models.ForeignKey(Admin, models.CASCADE)
    created = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    delete_at = models.DateTimeField(blank=True, null=True )
    class Meta:
        db_table = "announcement"
    def __str__(self):
        return str(self.announcement_title)

class Beacon(models.Model):
    beacon_id = models.AutoField(primary_key=True)
    beacon_name =  models.CharField(max_length=180, blank=True, null=True)  
    beacon_unique_uuid = models.CharField(max_length=250, blank=True, null=True)  
    beacon_service_uuid = models.CharField(max_length=250, blank=True, null=True) 
    beacon_characteristic_uuid = models.CharField(max_length=250, blank=True, null=True) 
    beacon_model =models.CharField(max_length=100, blank=True, null=True)  
    is_active = models.BooleanField(default=False)
    delete_at = models.DateTimeField(blank=True, null=True )
    class Meta:
        db_table = "beacon"
    def __str__(self):
        return str(self.beacon_name)
class Company_has_beacon(models.Model):
    company_has_beacon_id =  models.AutoField(primary_key=True)
    beacon = models.ForeignKey(Beacon, models.CASCADE)
    company = models.ForeignKey(Company, models.CASCADE)
    is_active = models.BooleanField(default=False)
    delete_at = models.DateTimeField(blank=True, null=True )
    class Meta:
        db_table = "company_has_beacon"
    def __str__(self):
        return str(self.company_has_beacon_id)

class Attendance_method(models.Model):
    attendance_method_id = models.AutoField(primary_key=True)
    attendance_method_name = models.CharField(max_length=80, blank=True, null=True)  
    class Meta:
        db_table = "attendance_method"
    def __str__(self):
        return str(self.attendance_method_name)
class Attendance_type(models.Model):
    attendance_type_id = models.AutoField(primary_key=True)
    attendance_type_name  =  models.CharField(max_length=80, blank=True, null=True)  
    class Meta:
        db_table = "attendance_type"
    def __str__(self):
        return str(self.attendance_type_name)

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    attendance_public_id =  models.UUIDField(
         default=uuid.uuid4, editable=False
    )
    users_uuid = models.ForeignKey(
        Users,
        to_field="users_uuid",
        on_delete=models.CASCADE,
        related_name="users_uuid_attendance",
        blank=True,
        null=True,
    )
    attendance_type = models.ForeignKey(Attendance_type, models.CASCADE)
    attendance_method = models.ForeignKey(Attendance_method, models.CASCADE)
    attendance_date =  models.DateField(blank=True, null=True )
    attendance_time = models.TimeField(blank=True, null=True )
    attendace_remark = models.CharField(max_length=150, blank=True, null=True) 
    attendance_location = models.CharField(max_length=150, blank=True, null=True) 
    attendance_lat = models.CharField(max_length=50, blank=True, null=True) 
    attendance_long =models.CharField(max_length=50, blank=True, null=True) 
    created = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    delete_at = models.DateTimeField(blank=True, null=True )
    class Meta:
        db_table = "attendance"
    def __str__(self):
        return str(self.attendance_public_id)

class Leave_type(models.Model):
    leave_type_id = models.AutoField(primary_key=True)
    leave_type_name = models.CharField(max_length=50, blank=True, null=True) 
class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    users_uuid = models.ForeignKey(
        Users,
        to_field="users_uuid",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    
    