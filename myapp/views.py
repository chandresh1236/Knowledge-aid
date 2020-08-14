from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import NoReverseMatch, reverse
from random import *
from .models import *
from .models import blog
from .models import  addToCart
from django.core.mail import send_mail
from math import ceil
from .form import *
import json
import random
from django.views.decorators.csrf import csrf_exempt

from . import Checksum
MERCHANT_KEY = 'KW2JLss6FDcAYPmj'

# Create your views here.
from django.http import HttpResponse

# Create your views here.


def home(request):
    if "email" in request.session:
        data = course.objects.all()
        news_data = news.objects.all()
        bloga = blog.objects.all()
        context={
            'bloga':bloga
            }
        uid = User.objects.get(email=request.session['email'])
        if uid:
                if uid.role == 'student':
                   request.session['email'] = uid.email
                   sid = student.objects.get(user_id=uid.id)
                   if sid:
                        request.session['firstname'] = sid.firstname
                        context = {
                            'uid': uid,
                            'sid': sid,
                            'bloga':bloga,
                             }
                        return render(request, "myapp/index.html", {'context': context,'news_data':news_data,'data':data})

                if uid.role == 'teacher':
                   request.session['email'] = uid.email
                   tid = teachers.objects.get(user_id=uid)
                   if tid:
                        request.session['firstname'] = tid.firstname

                        context = {
                            "uid": uid,
                            "tid": tid,
                            "bloga":bloga
                        }

                        return render(request, "myapp/index.html", {'context': context,'news_data':news_data,'data':data})
        else:
            e_msg = "Invalid input"
            return render(request, "myapp/login.html", {'e_msg': e_msg})

    else:    
        data = course.objects.all()
        news_data = news.objects.all()
        bloga = blog.objects.all()
        context={
               'bloga':bloga
            }
            
        return render(request, 'myapp/index.html',{'data':data,'news_data':news_data,'context':context})


def cartItems(cart):
    items = []
    for item in cart:
        items.append(course.objects.get(id=item))
        print(items)
    return items
def priceCart(cart):
    cart_items = cartItems(cart)
    price = 0
    for item in cart_items:
        price += item.course_price
    return price


def homea(request):
    return render(request,'myapp/index.html')
def register_page(request):
    return render(request, 'myapp/register.html')

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.course_discription.lower() or query in item.course_name.lower() or query in item.course_specification.lower():
        return True
    else:
        return False


def search(request):
    data = course.objects.all()
    news_data = news.objects.all()
    bloga = blog.objects.all()
    context={
        'bloga':bloga
        }
    
    if request.method=='GET':
        query = request.GET["search"]
        print(query)
        if query:
            match = course.objects.filter(course_name__icontains=query) | course.objects.filter(course_discription__icontains=query) | course.objects.filter(course_specification__icontains=query)
            print(match)
            return render(request,"myapp/search.html",{'query':match,'bloga':bloga,'news_data':news_data,'context':context,'data':data})
        else:
            return HttpResponseRedirect('/search/')
    '''allProds = []
    catprods = course.objects.values('course_name', 'id')
    cats = {item['course_name'] for item in catprods}
    for cat in cats: 
        prodtemp = course.objects.filter(course_name=cat)
        prod = [item for item in prodtemp if searchMatch(query,
         item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
             allProds.append([prod])
    params = {'allProds': allProds, "msg": ""}

    if len(allProds) == 0 or len(query)<4:
       params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'myapp/search.html', params)'''


def about(request):
    return render(request, 'myapp/about.html')

def cart1(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart, 'cart_size':len(cart), 'cartItems':cartItems(cart), 'cart_price': priceCart(cart)}
    return render(request, "myapp/cart-1.html", ctx)

    
def carting(request,pk=None):
    print("khihih")
    '''
    totalprice=0
    taid=""
    cart = request.session['cart']
    request.session.set_expiry(0)
    cid=course.objects.get(id=pk)
    print(cid,"-->course there")
    if "email" in request.session:
            uid = User.objects.get(email=request.session['email'])
            if(uid.role=="student"):
                sid=student.objects.get(user_id=uid)
                print(sid,"students")

            else:
                taid=teachers.objects.get(user_id=uid)
    else:
        print("-->please login")
    #print("tid is",cid.t_id)    
    #tida=int(cid.t_id)
    tida=cid.t_id_id
    tvid=teachers.objects.get(id=tida)
    price=cid.course_price
    totalprice=totalprice+price
    status="pending"
    if taid is not None:
        taid=taid
    else:
        taid="null"
    ctx=Enrollcourse.objects.create( user_id=uid,student_id=sid,teachers_id=tvid,price=price,totalprice=totalprice,tid=taid,course_id=cid)
    print("add sucessfully")

   # return render(request,"myapp/cart-1.html",{'ctx': ctx})
    

    #print(cid)
    #print("---->cid",type(cid.id))
    #print("111")
    if cid.id not in cart:
        cart.append(cid.id)
        
    else:
        pass
   
    cart_items=cartItems(cart)
    cart_price=priceCart(cart)
    cart = request.session['cart']
    request.session.set_expiry(0)
    cart_size=len(cart)
    print("---->cart_size",cart_size)
    ctx=Enrollcourse.objects.create( user_id=uid,student_id=sid,teachers_id=tvid,price=price,totalprice=totalprice,tid=taid,course_id=cid)    
    #ctx={'cid':cid,'cart':cart,'cart_size':cart_size,'cart_price':cart_price,'cartItems':cartItems(cart)}
    #return render(request, 'myapp/cart-1.html',ctx)'''
    #store_items = Enrollcourse.objects.all()
   # print("---->store",store_items)
    #cart = request.session['cart']
    '''
    taid=""
    totalprice=0
    cid=course.objects.get(id=pk)
    if "email" in request.session:
            uid = User.objects.get(email=request.session['email'])
            if(uid.role=="student"):
                sid=student.objects.get(user_id=uid)
                print(sid,"students")

            else:
                taid=teachers.objects.get(user_id=uid)
    else:
        print("-->please login")
    #print("tid is",cid.t_id)    
    #tida=int(cid.t_id)
    tida=cid.t_id_id
    tvid=teachers.objects.get(id=tida)
    price=cid.course_price
    totalprice=totalprice+price
    status="pending"
    if taid is not None:
        taid=taid
    else:
        taid="null"
    ctx=Enrollcourse.objects.create( user_id=uid,status=False,student_id=sid,teachers_id=tvid,price=price,totalprice=totalprice,tid=taid,course_id=cid)
    print("add sucessfully")
    '''
    if "email" in request.session:
        uida = User.objects.get(email=request.session['email'])
        if "email" in request.session:
            uida = User.objects.get(email=request.session['email'])
            if(uida.role=="student"):
                 cid=student.objects.get(user_id=uida)

            else:
                 cid=student.objects.get(user_id=uida)
                 print(cid)

        else:
            print("please login")

        cart = request.session['cart']
        request.session.set_expiry(0)
        #ctx = {'store_items':store_items, 'cart':cart, 'cart_size':len(cart)}
        #main_page = render(request, 'myapp\cart-1.html', ctx)
        civ=course.objects.get(id=pk)
        print(civ.course_price)
        v=addToCart.objects.create(uid=uida,pid=civ,price=civ.course_price)
        print(v)
        if pk not in cart:
            cart.append(int(pk))
            c=cartItems(cart)
            for i in c:
                print(i.course_name)
                print(i.id)

        ctx = {'cart':cart, 'cart_size':len(cart), 'cart_items':cartItems(cart), 'total_price': priceCart(cart),'civ':civ}
        return render(request,"myapp/cart-1.html", ctx)
    else:
        return render(request,"myapp/asha.html")


def carting1(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if(uid.role=="student"):
            cid=student.objects.get(user_id=uid)

        else:
             cid=student.objects.get(user_id=uid)

        return render(request, 'myapp/cart-2.html',{'cid': cid})
    else:
        print("please login")

def carting2(request):
    return render(request, 'myapp/cart-2.html')

def checkouta(request,p=None):
 try:
    v=p
    if "email" in request.session:
        email=request.session['email']
        print(email)
        u=User.objects.get(email=email)
        m=addToCart.objects.get(id=u.id)
        c=m.pid
        print(c.id)
        va=placeOrder.objects.filter(pid=c.id)
        print(va)
        if va:
            print("already there")
        else:
            s=placeOrder.objects.create(uid=u,pid=c,price=v)
            if s:
               print("sucess order")
               
    if request.method=="POST":
        #items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        #order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                      # state=state, zip_code=zip_code, phone=phone, amount=amount)
        #order.save()
        #update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        #update.save()
        thank = True
        id = random.random() + 1.00
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'HaQprA83605960459616',
                'ORDER_ID': str(id),
                'TXN_AMOUNT': str(p),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)

        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
 except:
    print(Exception)

 return render(request, 'myapp/check.html',{'v':v})


    

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')

        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})



def removecart(request,pk=None):
    print("khipk",pk)
    '''
    cid=Enrollcourse.objects.get(course_id=pk)
    Enrollcourse.delete(cid)
    ctx=Enrollcourse.objects.all()
    return render(request,"myapp\cart-1.html",{'ctx':ctx})'''
    request.session.set_expiry(0)
    obj_to_remove = pk
    obj_indx = request.session['cart'].index(int(obj_to_remove))
    request.session['cart'].pop(obj_indx)
    return redirect("cart3")


def cart3(request):
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx = {'cart':cart, 'cart_size':len(cart), 'cart_items':cartItems(cart), 'total_price': priceCart(cart)}
    return render(request, "myapp\cart-1.html", ctx)

def bloga(request):
    return render(request, 'myapp/blog.html')


def err(request):
    return render(request, 'myapp/404.html')


def agendacalender(request):
    return render(request, 'myapp/agenda-calendar.html')


def faq(request):
    return render(request, 'myapp/faq.html')


def help(request):
    return render(request, 'myapp/help.html')


def coursedetail(request):
    return render(request, 'myapp/course-detail.html')


def coursedetaila(request):
    return render(request, 'myapp/course-detail-2.html')

def course_preview6(request,p=None):
    
    if 'cart' not in request.session:
        cart = []
        request.session['cart'] = []
    cid=course.objects.get(id=p)
    
    print("hfjgikg")
    try:
       link=YTLinka.objects.get(id=p).link
    except YTLinka.DoesNotExist:
       link = None 
    if link is not None:
        print(link)
    if link is None:
        link="weljk"
        print(link)
    return render(request,"myapp/course-detail-23.html",{'cid':cid,'link':link})
    

def course_preview1(request,pk=None):
    
    if 'cart' not in request.session:
        cart = []
        request.session['cart'] = []
    cid=course.objects.get(id=pk)
    
    
    try:
       link=YTLinka.objects.get(id=pk).link
    except YTLinka.DoesNotExist:
       link = None
    if link is not None:
        print(link)
    if link is None:
        link="weljk"
        print(link)
    return render(request,"myapp/course-detail22.html",{'cid':cid,'link':link})


    
    

def purchase(request,pk=None):
    pass

def edit(request,pk=None):
    uid=User.objects.get(id=pk)
    if uid.role=='student':
            tid=student.objects.get(user_id=pk)
            context = {
                         'tid': tid,
                         'uid':uid
                }
            return render(request, "myapp/admin_section/user-profile.html", {'context': context})
    else:
         
            tid = teachers.objects.get(user_id=pk)
            context = {
                        "uid": uid,
                        "tid": tid
               }
            return render(request, "myapp/admin_section/teacher-profile.html", {'context': context})

def editcourse(request,pk=None):
    uid=course.objects.get(id=pk)
    return render(request, "myapp/admin_section/coursesedit.html", {'uid': uid})
def deletecourse(request,pk=None):
    cid=course.objects.get(id=pk)
    print(cid)
    cid.delete()
    print('--->data deleted sucessfully')
    sid=course.objects.all()
    return render(request,"myapp/admin_section/allcourses.html",{'sid':sid})

def delete(request,pk=None):
    print("-----> id is" + pk)
    uid=User.objects.get(id=pk)
    uid.delete()
    print("---->data deleted sucessfully")


def pricingtables(request):
    return render(request, 'myapp/pricing-tables.html')


def mediagallery(request):
    return render(request, 'myapp/media-gallery.html')


def coursegrid(request):
    data=course.objects.all()
    print(data)
    '''rat=data.objects.get(course_rating=data.course_rating)'''
    return render(request, 'myapp/courses-grid.html',{'data':data})


def courselist(request):
    data=course.objects.all()
    return render(request,"myapp/courses-list.html",{'data':data})

def course_preview(request,pk=None):

    if 'cart' not in request.session:
        cart = []
        request.session['cart'] = []
    
    cid=course.objects.get(id=pk)
    link=YTLink.objects.get(id=pk)
    file=FileUpload.objects.get(id=pk)
    text=TextBlock.objects.get(id=pk)

    print(link)
    return render(request,"myapp/course-detail.html",{'cid':cid,'link':link,'file':file,'text':text})


def courses(request):
    data=course.objects.all() 
    return render(request, 'myapp/courses.html',{'data':data})


def contacts(request):
    return render(request, 'myapp/contacts.html')


def teachersdetail(request):
    return render(request, 'myapp/teachers-detail.html')


def iconpack1(request):
    return render(request, 'myapp/icon-pack-1.html')


def iconpack1(request):
    return render(request, 'myapp/icon-pack-1.html')


def admin_login(request):
    return render(request, 'myapp/admin_login.html')


def admission(request): 
    return render(request, 'myapp/admission.html')


def adminsection(request):
    c=course.objects.all().count()
    t=teachers.objects.all().count()
    u=User.objects.all().count()
    print("dgg",c)
    print(u)
    context={
        "c": c,
        "t": t,
        "u": u,

    }
    return render(request, 'myapp/admin_section/index.html',{'context':context})
def adminprofile(request):
    return render(request,'myapp/admin_section/adminprofile.html')


def admin_login_evalute(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
        uid = admin.objects.get(email=email)
        print("ugug",uid)
        if uid:
            print("-------->admin exist")
            return render(request, "myapp/admin_section/adminprofile.html")
        else:
            e_msg = "Invalid input"                                                                                                                                                                                                                                                                                                                                              
            return render(request, "myapp/admin_login.html", {'e_msg': e_msg})
    except:
        e_msg = "User does not exist"
        print(e_msg)
        return render(request, "myapp/admin_section/adminprofile.html")


def login(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        data = course.objects.all()
        news_data = news.objects.all()
        bloga = blog.objects.all()
    
        print(news_data,"news-->")

        if uid:
            if uid.role == 'student':
                request.session['email'] = uid.email
                sid = student.objects.get(user_id=uid.id)
                if sid:
                    request.session['firstname'] = sid.firstname
                    context = {
                        'uid': uid,
                        'sid': sid,
                        'bloga': bloga
                         }
                   
                    return render(request, 'myapp/index.html',{'data':data,'news_data':news_data,'context': context})

            if uid.role == 'teacher':
                request.session['email'] = uid.email
                tid = teachers.objects.get(user_id=uid)
                if tid:
                    request.session['firstname'] = tid.firstname

                    context = {
                        "uid": uid,
                        "tid": tid,
                        "bloga":bloga
                    }

                    return render(request, 'myapp/index.html',{'data':data,'news_data':news_data,'context': context})
        else:
            e_msg = "Invalid input"
            return render(request, "myapp/login.html", {'e_msg': e_msg})
    else:
        return render(request, 'myapp/login.html')


def login_evaluate(request):
    '''   
     if request.method=="POST":
           role=request.POST.get('role')
           if role == 'students':
               email = request.POST['email']
               password = request.POST['password']
               user = User.objects.filter(email = email)
               print(user)
               if user[0]:
                   if user[0].password == password and user[0].role == 'student':
                       students = student.objects.filter(user_id = user[0])
                       request.session['email'] = user[0].email
                       request.session['firstname'] = students[0].firstname
                       request.session['role'] = user[0].role
                       request.session['id'] = user[0].id
                       print('login sucessfully')
                       return render(request,"myapp/index.html")
               else:
                       message = "Your password is incorrect or user doesn't exist"
                       return render(request,"myapp/login.html",{'message':message})
           else:
                message = "user doesn't exist"
                return render(request,"myapp/login.html",{'message':message})

           if role == 'teachers':

               email = request.POST['email']
               password = request.POST['password']
               user = User.objects.filter(email = email)
               print(user)
               if user[0]:
                   if user[0].password == password and user[0].role == 'teachers':
                       teacher = teachers.objects.filter(user_id = user[0])
                       request.session['email'] = user[0].email
                       request.session['firstname'] = patient[0].firstname
                       request.session['role'] = user[0].role
                       return HttpResponseRedirect(reverse('login'))
               else:
                       message = "Your password is incorrect or user doesn't exist"
                       return render(request,"myapp/login.html",{'message':message})
           else:
                message = "user doesn't exist"
                return render(request,"myapp/login.html",{'message':message})
       '''


def login_evaluate(request):
    news_data=news.objects.all()
    data = course.objects.all()
    bloga=blog.objects.all()
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if uid:
            if uid.role == 'student':
                request.session['email'] = uid.email
                sid = student.objects.get(user_id=uid.id)
                if sid:
                    request.session['firstname'] = sid.firstname
                    context = {
                        'uid': uid,
                        'sid': sid,
                        'bloga':bloga,
                    }
                    return render(request, "myapp/index.html", {'context': context,'news_data':news_data,'data':data})

            if uid.role == 'teacher':
                request.session['email'] = uid.email
                tid = teachers.objects.get(user_id=uid)
                if tid:
                    request.session['firstname'] = tid.firstname

                    context = {
                        "uid": uid,
                        "tid": tid,
                        "bloga":bloga

                    }

                    return render(request, "myapp/index.html", {'context': context,'news_data':news_data,'data':data})
        else:
            e_msg = "Invalid input"
            return render(request, "myapp/login.html", {'e_msg': e_msg})

    try:
        email = request.POST['email']
        password = request.POST['password']
        uid = User.objects.get(email=email)
        print("uid .............", uid)
        if uid.email==email:
            if uid.role == 'student':
                print("------------>role", uid.role)
                request.session['email'] = uid.email
                sid = student.objects.get(user_id=uid.id)
                print("sid.......", sid)
                if sid:
                    request.session['firstname'] = sid.firstname
                    context = {
                        'uid': uid,
                        'sid': sid,
                    }
                    print("-------------->student", sid.firstname)
                    return render(request, "myapp/index.html", {'context': context})

            if uid.role == 'teacher':
                request.session['email'] = uid.email
                tid = teachers.objects.get(user_id=uid)
                print("sid.......", tid)
                if tid:
                    request.session['firstname'] = tid.firstname

                    context = {
                        "uid": uid,
                        "tid": tid
                    }

                    return render(request, "myapp/index.html", {'context': context})
        else:
            print("fufuf")
            e_msg = "Invalid input email or password"
            return render(request, "myapp/login.html", {'e_msg': e_msg})

    except:
        e_msg = "User does not exist"
        return render(request, "myapp/login.html", {'e_msg': e_msg})


def userLogout(request):
    flag=0
    if "email" in request.session:
        logout(request)
        print("------------------->logout")
        return redirect('/login/')
    else:
        flag=1
        data = course.objects.all()
        news_data = news.objects.all()
        bloga = blog.objects.all()
        context={
            'bloga':bloga
         }
    
        return render(request,"myapp/index.html",{'flag':flag,'data':data,'news_data':news_data,'bloga':bloga})


def register(request):
    if request.method == "POST":
        role = request.POST['role']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cnfpassword = request.POST['cnfpassword']

        if password != cnfpassword:
            e_msg = "password does not match !"
            return render(request, 'myapp/register.html', {'e_msg': e_msg})

        else:
            if role == "student":
                uid = User.objects.create(
                    email=email, password=password, role=role)
                sid = student.objects.create(user_id=uid, firstname=firstname, lastname=lastname)
                emaila="chandresh6531@gmail.com"
                s_msg = "Registeration successfully done"
                send_mail("Conformation mail:-", "welcome to knowledge-aid","knowledgeaid2@gmail.com", [emaila])
                return render(request, 'myapp/register.html', {'s_msg': s_msg})
            else:
                uid = User.objects.create(
                    email=email, password=password, role=role)
                sid = teachers.objects.create(
                    user_id=uid, firstname=firstname, lastname=lastname)
                s_msg = "Registeration successfully done"

                send_mail("Conformation mail:-", "welcome to knowledge-aid", "knowledgeaid2@gmail.com", [email])

                return render(request, 'myapp/register.html', {'s_msg': s_msg})
    else:
        return render(request, "myapp/register.html")


def forgot_password(request):
    return render(request, "myapp/forgot-password.html")


def send_otp(request):
    try:
        uemaila = request.POST['email']
        uemail="chandresh6531@gmail.com"
        uid = User.objects.get(email=uemail)
        print("---->",uid)
        if uid:
            n_otp = randint(1111, 9999)
            print('--otp',n_otp)
            uid.otp = n_otp
            uid.save()
            send_mail("Forget_password", "otp is:" + str(uid.otp),
                      "knowledgeaid2@gmail.com", [uemail])
            return render(request, "myapp/reset-password.html", {'email': uemail})
        else:
            e_msg = "user doesn't exist"
            return render(request, "myapp/forgot-password.html", {'e_msg': e_msg})
    except:
        return render(request, "myapp/forgot-password.html")


def reset_password(request):
    try:
        email = request.POST['email']
        otp = request.POST['otp']
        newpassword = request.POST['newpassword']
        retypepassword = request.POST['retypepassword']
        uid = User.objects.get(email=email)
        if uid:
            if str(uid.otp) == str(otp) and newpassword == retypepassword:
                uid.password = newpassword
                uid.save()
                s_msg = "Password sucessfully changed"
                return render(request, "myapp/login.html", {'s_msg': s_msg})
            else:
                e_msg = "password otp doesnot match!"
                render(request, "myapp/forgot-password.html", {'e_msg': e_msg})

        else:
            render(request, "myapp/forgot-password.html")

    except:
        e_msg = "user does not exist!"
        render(request, "myapp/forgot-password.html", {'e_msg': e_msg})


def addcourse(request):
    data=teachers.objects.all()
    s=AddChapterForm()
    l=AddLinkForm()
    d=AddTxtForm()

    return render(request, "myapp/admin_section/add-listing.html",{'data':data,'s':s,'l':l,'d':d})

def upcourse(request):
    uid=course.objects.all()
    return render(request,"myapp/admin_section/coursesedit.html",{'uid':uid})
def updcourse(request):
    id=request.POST['course_id']
    uid=course.objects.get(id=id)
    uid.course_name=request.POST['course_name']
    uid.course_discription=request.POST['course_discription']
    uid.course_price=request.POST['course_price']
    uid.course_duration=request.POST['course_duration']
    uid.course_specification=request.POST['course_specification']
    uid.course_rating=request.POST['course_rating']
    if "course_pic" in request.FILES:
          uid.course_pic = request.FILES['course_pic']
    if "course_video" in request.FILES:
            uid.course_video = request.FILES['course_video']
    uid.save()
    
    print("---> adddd suc",uid.course_name)
    return render(request, "myapp/admin_section/index.html")


def userprofile(request):
   uid = User.objects.get(email=request.session['email'])
   if uid:

            if uid.role == "student":
                tid = student.objects.get(user_id=uid)
                context = {
                         "uid": uid,
                         "tid": tid
                          }
                return render(request, "myapp/admin_section/user-profile.html", {'context': context})
            else:
                msg="login required"
                return render(request, "myapp/login.html",{'msg': msg})
               
   else:
           print("----> please login user")
           msg="login required"
           
           return render(request, "myapp/login.html",{'msg': msg})

def teacherprofile(request):

    uid = User.objects.get(email=request.session['email'])
 
    if uid.role == "teacher":
        tid = teachers.objects.get(user_id=uid)
        context = {
            "uid": uid,
            "tid": tid
        }
        return render(request, "myapp/admin_section/teacher-profile.html", {'context': context})
    else:
        return render(request, "myapp/login.html")


def updateteacher(request):
    firstname = request.POST['firstname']
    email = request.POST['email']
    lastname = request.POST['lastname']
    qualification = request.POST['qualification']
    uid = User.objects.get(email=email)
    tid = teachers.objects.get(user_id=uid)

    if uid:
        uid.password = forgot_password
        uid.save()
    if tid:
        tid.firstname = firstname
        tid.lastname = lastname
        tid.qualification = qualification
        if "mypic" in request.FILES:
            mypic = request.FILES['mypic']
            tid.teacher_pic = mypic
            uid.pic=mypic
        tid.save()
        uid.save()

    context = {
        "uid": uid,
        "tid": tid
    }

    return render(request, "myapp/admin_section/index.html", {'context': context})
def updatestudent(request):
    firstname = request.POST['firstname']
    email = request.POST['email']
    lastname = request.POST['lastname']
    uid = User.objects.get(email=email)
    tid = student.objects.get(user_id=uid)

    #if uid:
        #uid.password = forgot_password
        #uid.save()
    if tid:
        tid.firstname = firstname
        tid.lastname = lastname
        if "mypic" in request.FILES:
            mypic = request.FILES['mypic']
            tid.student_pic = mypic
            uid.pic=mypic
        tid.save()
        uid.save()

    context = {
        "uid": uid,
        "tid": tid
    }

    return render(request, "myapp/admin_section/index.html", {'context': context})
def updatecourse(request):
    course_name=request.POST['course_name']
    course_discription=request.POST['course_discription']
    course_price=request.POST['course_price']
    course_duration=request.POST['course_duration']
    course_specification=request.POST['course_specification']
    course_rating=request.POST['course_rating']
    teacher_id=request.POST['tid']
    tid=teachers.objects.get(id=teacher_id)

    if "course_pic" in request.FILES:
          course_pic = request.FILES['course_pic']
    if "course_video" in request.FILES:
            course_video = request.FILES['course_video']
    cid=course.objects.create(course_name=course_name,course_discription=course_discription,course_price=course_price,course_duration=course_duration,course_specification=course_specification,course_rating=course_rating,course_pic=course_pic,course_video=course_video,t_id=tid)
    print("---> adddd suc",cid)
    form = AddChapterForm(request.POST or None) 
    if form.is_valid(): 
        form.save() 
    forma = AddLinkForm(request.POST or None) 
    if forma.is_valid(): 
        forma.save() 
    formb = AddTxtForm()(request.POST or None) 
    if formb.is_valid(): 
        formb.save() 
        print("->---form added")
    
    uid.save()
    return render(request, "myapp/admin_section/index.html")
    
    
def display_course(request):
    data=course.objects.all()
    return render(request,"myapp/index.html",{'data':data})
def newsa(request):
    return render(request,"myapp/admin_section/news.html")

def viewsall(request):
    sid=student.objects.all()
    return render(request,"myapp/admin_section/viewsall.html",{'sid':sid})
def viewsstu(request):
    sid=[]
    if "email" in request.session:
        email=request.session['email']
        id=User.objects.get(email=email)
        ida=placeOrder.objects.filter(uid=id)
        
        for i in ida:pass
        user1=ida[0:ida.count()+1]
        print(type(user1))
        print(user1)
        for i in user1:
            sid.append(i.pid)
      
       
       
    
        print(sid)
    
        
        
    
        return render(request,"myapp/admin_section/stucourses.html",{'sid':sid})
def allteachers(request):
    uid=User.objects.all()
    sid=teachers.objects.all()
    return render(request,"myapp/admin_section/allteachers.html",{'sid':sid,'uid':uid})
def allcourse(request):
    sid=course.objects.all()
    return render(request,"myapp/admin_section/allcourses.html",{'sid':sid})


def viewsb(request):
    sid=student.objects.all()
    uid=User.objects.all()
    tid=teachers.objects.all()
    vid=viewsa.objects.create(sid=sid,tid=tid,uid=uid)
    data=viewsa.objects.all()
    return render(request,"myapp/admin_section/viewsall.html",{'data':data})


    
def addnews(request):
    news_title=request.POST['newstitle']
    news_location=request.POST['location']
    news_description=request.POST['description']
    news_date=request.POST['datenews']
    if "picnews" in request.FILES:
        news_pic=request.FILES['picnews']
    msg="data added Sucessfully!..."
    ob=news.objects.create(newstitle=news_title,location=news_location,description=news_description,date=news_date,picnews=news_pic)
    return render(request,"myapp/admin_section/news.html",{'msg':msg})
def comparision(request):
    dataa=data.objects.all()
    imga=img.objects.all()
    d=list(dataa)
    i=list(imga)
    zipa=zip(d,i)
    

    return render(request,"myapp/datatable.html",{'context':zipa})


