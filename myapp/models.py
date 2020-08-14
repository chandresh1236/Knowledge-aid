from django.db import models
# Create your models here.
from django.template.defaultfilters import truncatechars 
from django.utils.safestring import mark_safe

class User(models.Model):
    email = models.EmailField(unique= True)
    password = models.CharField(max_length = 20)
    otp = models.IntegerField(default = 459)
    is_active = models.BooleanField(default=True)
    is_verfied = models.BooleanField(default=False)
    role = models.CharField(max_length = 10)
    created_at= models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True, blank=False)
    pic = models.FileField(upload_to='myapp/img/', default='myapp/img/avatar2.png', blank=True)

class student(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    student_pic = models.FileField( upload_to='myapp/img/', default='course_6.png', blank=True)
    
class teachers(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    qualification = models.CharField(max_length=100, blank= True)
    teacher_pic = models.FileField( upload_to='myapp/img/', default='img/avatar.png', blank=True)
    
class course(models.Model):
    course_name = models.CharField(max_length=50, blank=True)
    course_discription = models.CharField(max_length=200, blank=True)
    course_price = models.IntegerField(blank=True)
    course_duration = models.CharField(max_length=50, blank=True)
    course_specification = models.CharField(max_length=200, blank=True)
    course_rating = models.IntegerField(blank=True)
    website = models.CharField(max_length=60, blank=True)
    course_pic = models.FileField(upload_to='myapp/img/', default='course_6.png', blank=True)
    course_video = models.FileField(upload_to='myapp/media/videos', default='course_6.png', blank=True)
    t_id = models.ForeignKey(teachers, on_delete = models.CASCADE)
    @property
    def short_description(self):
        return truncatechars(self.description, 20)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))
    admin_photo.short_description = 'Image'
    admin_photo.allow_tags = True
class ratings(models.Model):
    course = models.ForeignKey(course, on_delete = models.CASCADE)
    rate=models.IntegerField(blank=True)


class Enrollcourse(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    student_id = models.ForeignKey(student, on_delete = models.CASCADE)
    teachers_id = models.ForeignKey(teachers, on_delete = models.CASCADE)
    course_id=models.ForeignKey(course, on_delete = models.CASCADE)
    status=models.CharField(max_length=60, blank=True)
    price=models.IntegerField(default=0)
    totalprice=models.IntegerField(default=0)
    tid=models.CharField(max_length=50)

class addToCart(models.Model):
    uid= models.ForeignKey(User, on_delete = models.CASCADE)
    pid= models.ForeignKey(course, on_delete = models.CASCADE)
    price= models.IntegerField(default=0)
    
class placeOrder(models.Model):
    uid= models.ForeignKey(User, on_delete = models.CASCADE)
    pid= models.ForeignKey(course, on_delete = models.CASCADE)
    price= models.IntegerField(default=0)
    created_at= models.DateTimeField(auto_now_add=True,blank=False)
    #placed_date=models.DateField(blank=False)
    status=models.CharField(max_length=50,default="In Process")
   

class admin(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique= True,blank=False)
    password = models.CharField(max_length = 20)

class news(models.Model):
    newstitle=models.CharField(max_length=1000)
    location=models.URLField(max_length=2000)
    description=models.TextField(max_length=1000)
    date=models.CharField(max_length=50)
    picnews = models.FileField(upload_to='myapp/img/', default='course_6.png', blank=True)

class viewsa(models.Model):
    sid = models.ForeignKey(student, on_delete = models.CASCADE)
    tid = models.ForeignKey(teachers, on_delete = models.CASCADE)
    uid = models.ForeignKey(User,on_delete=models.CASCADE)

class data(models.Model):
    name=models.CharField(max_length=1000)
    price=models.CharField(max_length=1000)
    ratings=models.CharField(max_length=100)

class img(models.Model):
    image=models.ImageField()
    link=models.ImageField()
    
class blog(models.Model):
    image=models.ImageField()
    link=models.ImageField()
    title=models.CharField(max_length=1000)
    discription=models.CharField(max_length=1000)

    @property
    def short_description(self):
        return truncatechars(self.description, 20)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))
    admin_photo.short_description = 'Image'
    admin_photo.allow_tags = True


class Chapter(models.Model):
    chapter_name = models.CharField(max_length=20)
    chapter_created_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(course, on_delete=models.CASCADE, default=1)


    def __unicode__(self):
        return self.chapter_name

class YTLink(models.Model):
    link = models.URLField(max_length=200)
    yt_link_fk = models.ForeignKey(Chapter, on_delete=models.CASCADE, default=1)
    date_created = models.DateTimeField(auto_now_add=True)


class FileUpload(models.Model):
    file = models.FileField(null=False, blank=False, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    file_fk = models.ForeignKey(Chapter, on_delete=models.CASCADE, default=1)

class TextBlock(models.Model):
    lesson = models.TextField()
    text_block_fk = models.ForeignKey(Chapter, on_delete=models.CASCADE, default=1)
    date_created = models.DateTimeField(auto_now_add=True)

class Chaptera(models.Model):
    chapter_name = models.CharField(max_length=20)
    chapter_created_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(course, on_delete=models.CASCADE, default=1)


    def __unicode__(self):
        return self.chapter_name

class YTLinka(models.Model):
    link = models.URLField(max_length=200)
    yt_link_fk = models.ForeignKey(Chaptera, on_delete=models.CASCADE, default=1)
    date_created = models.DateTimeField(auto_now_add=True)