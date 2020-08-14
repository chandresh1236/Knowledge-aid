from django.contrib import admin

from . models import student,course,teachers,User,blog,data,img,news,YTLinka,FileUpload,TextBlock,Chaptera,placeOrder,addToCart,Enrollcourse
#Register your models here.


from django.contrib.auth.models import User, Group 
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _ 
# Register your models here.

class MyUserAdmin(UserAdmin): 

    list_display = ("username","first_name", "last_name", "email","is_active","is_staff")
    list_filter = ()
    # Static overriding 
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

class DemoProfileAdmin(admin.ModelAdmin):
    #actions_selection_counter = True
    #actions_on_bottom = False
    #actions_on_top = True

    fields = ('title','discription',  'course_pic')
    list_display = [
        'course_pic',
        'course_name',
        'course_discription',
    ]
    list_display_links=[
        'course_name',
    ]
    list_filter = [
        'course_name',
        'course_discription',
    ]

    fields = ( 'admin_photo', )
    readonly_fields = ('admin_photo',)
    
class DemoProfileAdminb(admin.ModelAdmin):
        #actions_selection_counter = True
    #actions_on_bottom = False
    #actions_on_top = True

    fields = ('image','link',  'discription')
    list_display = [
        'admin_photo',
        'link',
        'discription',
    ]
    list_display_links=[
        'link',
    ]
    list_filter = [
        'link',
        'discription',
    ]
    
  
    
    


class CustPost(admin.ModelAdmin):
     list_display = ('firstname','lastname')
     list_display_links=('lastname',)
     list_editable = ('firstname',)
     search_fields = ('firstname','lastname')


admin.site.site_header="Knowledge-Aid"
admin.site.site_title="Find And Compare Courses!.."
admin.site.register(student,CustPost)
admin.site.register(course,DemoProfileAdmin)
admin.site.register(teachers,CustPost)
admin.site.register(blog,DemoProfileAdminb)
admin.site.register(data)
admin.site.register(img)
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(news)
admin.site.register(User,MyUserAdmin)
admin.site.register(YTLinka)
admin.site.register(FileUpload)
admin.site.register(Chaptera)
admin.site.register(placeOrder)
admin.site.register(addToCart)
admin.site.register(Enrollcourse)



