from django.shortcuts import render
from petadoptapp.models import pet,cart,adopt,Contact
from django.contrib.auth.models import  User  
from django.contrib.auth import authenticate , login , logout
from django.shortcuts import redirect
from django.contrib import messages
import uuid
import razorpay


# Create your views here.
def index(request):
    user=request.user 
    print("user logged in",user.is_authenticated) 
    context ={}
    allpet = pet.objects.all()
    context['pets'] = allpet
    return render(request,'index.html',context) 



def userlogin(request):
        if request.method=="GET": 
            return render(request, 'login.html')    
        else:
            '''1.fetch data '''
            u=request.POST['username'] 
            p=request.POST['password'] #capture form data  
             
            user= authenticate(username=u ,password= p) #inbuilt authethticate tunnction  . it verify only if password and username same or not 
            # when user login it will create session . and authnthicate only verify username and pasword if coorect will get user object.
            # print("login user after authenticate",user) 
            if user is not None: #succesfully login 
                login(request,user)
                return redirect("/") 
            else:
                context={}
                context["error"]='plz enter valid credential'
                return render(request,'login.html',context) 
 
 
 
def register(request):
    if request.method=="GET":   #render register page its load templates fom teplates django handle template rendering 
        return render(request,'register.html')     
    else:
        u=request.POST['username']   #form input  
        e=request.POST['email']
        p=request.POST['password'] 
        cp=request.POST['Confirmpassword']     
        
        context={}
        
        if u=="" or e=="" and e=="@gmail.com" or p=="" or cp=="" :  
            context['error']='all the field are compulsory' 
            return render(request,'register.html',context)     
        elif p != cp:
            context['error']='password and confirm password must be same.'    
            return render(request,'register.html',context)    
        else:
            # user= User.objects.create(username=u,email=e,password=p)   #model class name  (db column name)  
            user = User.objects.create(username=u,email=e)  #auth_user    
            user.set_password(p) #encrypted password      . protect user account 
            user.save()  
            
            return redirect('/login') 
    
def aboutus(request):
    return render(request,'about.html')

def contactus(request):
    return render(request,'contact.html')
        
def userlogout(request):
    logout(request) 
    return redirect("/") 

from django.db.models import Q

def search(request):
    query = request.GET.get('query')
    if query:
        results = pet.objects.filter(Q(name__icontains=query) | Q(type__icontains=query))
    else:
        results = []

    return render(request, 'search_results.html', {'query': query, 'results': results})




def addtocart(request,petid):
    selectedpetobject = pet.objects.get(id=petid)
    userid = request.user.id
    if userid is not None:
        loggedInUserObject = User.objects.get(id = userid)  #if user is login 
        Cart = cart.objects.create(uid=loggedInUserObject,petid=selectedpetobject) 
        Cart.save()
        # messages.success(request,'pet added to cart successfully') 
        return redirect('/') 
    else: 
        return redirect('/login') 
    

def removecart(request,cartid):
    c= cart.objects.filter(id=cartid)  
    c.delete()  
    return redirect('/confirmadopt')     
    
def confirmadopt(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    user_cart_items = cart.objects.filter(uid=request.user).select_related('petid')

    totalbill = sum(item.petid.price for item in user_cart_items)

    context = {
        'mycart': user_cart_items,
        'count': user_cart_items.count(),
        'totalbill': totalbill,
    }

    return render(request, 'confirmadopt.html', context)

def placeadopt(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    user = request.user
    cartlist = cart.objects.filter(uid=user)

    if not cartlist:
        return redirect('/confirmadopt') 

    total = sum(item.petid.price for item in cartlist)

    # Store pet ids temporarily in session
    request.session['cart_ids'] = [item.petid.id for item in cartlist]
    request.session['order_id'] = str(uuid.uuid4())

    client = razorpay.Client(auth=("rzp_test_5tcqyKP7gK3N5l", "7p6xDqY81DWrnHdYUntGeOmw"))
    payment = client.order.create(data={
        "amount": total * 100,
        "currency": "INR",
        "receipt": request.session['order_id']
    })

    return render(request, 'pay.html', {
        'total': total,
        'data': payment
    })

from django.contrib.auth.decorators import login_required

@login_required
def myadoptions(request):
    user = request.user
    adoptions = adopt.objects.filter(userid=user).select_related('petid').order_by('-adopt_date')
    return render(request, 'myadoptions.html', {'adoptions': adoptions})


def adopt_success(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    user = request.user
    pet_ids = request.session.get('cart_ids', [])
    ordid = request.session.get('order_id', str(uuid.uuid4()))

    for pid in pet_ids:
        pet_obj = pet.objects.get(id=pid)
        adopt.objects.create(
            adoptid=ordid,
            userid=user,
            petid=pet_obj
        )

    # Clear cart and session
    cart.objects.filter(uid=user).delete() 
    request.session.pop('cart_ids', None)
    request.session.pop('order_id', None)

    return render(request, 'adopt_success.html')  



def contactus(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save message to the model (if applicable)
        Contact.objects.create(name=name, email=email, message=message)

        messages.success(request, "Thank you for reaching out. We’ll get back to you shortly.")
        return redirect('/contact')  # or re-render same page
    
    return render(request, 'contact.html')






           