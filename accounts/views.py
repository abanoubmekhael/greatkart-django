from django.shortcuts import render , redirect
from . forms import RegistrationForm
from .models import Account
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils. encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage , send_mail
 

# Create your views here.
def register (request):  #cleand_data['all fields']
    if request.method =='POST':                 # إلطريقة إلتإنية
        form = RegistrationForm(request.POST)   # Contain all fields values - Fetch data   contain all values
        if form.is_valid():
            first_name     = form.cleaned_data['first_name']  # طإبق/زاوج/سكّن البيانات في قاعدة البيانات مش الفورم
            last_name      = form.cleaned_data['last_name']    # هنجيب كل الفيلدس 
            phone_number   = form.cleaned_data['phone_number'] 
            email          = form.cleaned_data['email'] 
            password       = form.cleaned_data ['password']
            username       = email.split('@')[0] #split  => بيقسم - يفرط
            user           = Account.objects.create_user(first_name = first_name, last_name = last_name, email = email, password = password , username = username)
            user.phone_number = phone_number
            user.save() #after user.save() [Not Complicatecd]
            # user activate (decode)
            current_site = get_current_site(request) 
            # local host , in future use a different domain
            mail_subject = 'Please Activate Your Account'
            to_email   = email
            message = render_to_string ('accounts/account_verification_email.html' , {
                'user'   : user,
                'domain' : current_site ,
                'uid'    : urlsafe_base64_encode(force_bytes(user.pk)), #user_id
                'token'  : default_token_generator.make_token(user), # رمز مميز
            })# pass (template file , {user - domain - uid}) 
            send_email = EmailMessage (mail_subject , message , to = [to_email]) 
            # 3 حإجإت نجمع إلـ
            send_email.send()
            # messages.success(request , 'Thank You For regisration with us , We have Sent You an email verification to Your email. Please verify it')  #messages.success
            return redirect ('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {'form':form}
    return render(request , 'accounts/register.html' , context)

def login (request):   
    #for only admin , other users requires activation
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email , password=password)
        if user is not None:
            auth.login(request , user)
            messages.success(request , 'You are Logged in.')
            return redirect ('dashboard') #not home
        else:
            messages.error(request , 'invalid login Credential')
            return redirect ('login')
    return render(request , 'accounts/login.html')

#This Function require: 
# reqire Login_required (login_url = 'login')
@login_required (login_url = 'login')   #  لازم يكون مسجل عشان يعمل تسجيل خروج
def logout (request):  
    auth.logout(request)
    messages.success(request ,  "You are Loggedout")
    return redirect ('login')

    # form.is_valid(): => وراها => ex.username =form.cleaned_data['username']

#                  cleaned_data['username']
#  cleaned_data = مطابقة الداتا في الفورم وحفظ مثيلتها في قاعدة البيانات
# إذا كنت تستخدم ModelForm،
#  فلن تكون هناك حاجة إلى اللعب بقاموس البيانات النظيفة لأنه عندما تستخدم form.save()
#  ، تكون مطابقته بالفعل ويتم حفظ البيانات النظيفة. 
#     لكنك تستخدم الفورم الأساسي،
#   فيجب عليك مطابقة كل داتا تم تنظيفها يدويًا بمكان قاعدة البيانات الخاصة بها
#    ثم حفظ المثيل في قاعدة البيانات وليس الفورم 

# يعد التابع clean()‎ في الفئة الفرعية Field مسؤولاً عن تشغيل to_python() وvalidate() وrun_validators()
#  بالترتيب الصحيح ونشر أخطائهم. إذا ظهرت أي من الطرق، في أي وقت، خطأ في التحقق من الصحة، 
# فستتوقف عملية التحقق وسيظهر هذا الخطأ. 
# تقوم هذه الطريقة بإرجاع البيانات النظيفة، والتي يتم بعد ذلك إدراجها في قاموس البيانات النظيفة الخاص بالنموذج.


def activate (request , uidb64 , token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError , ValueError , OverflowError , Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user , token):
        user.is_active = True
        user.save()
        messages.success(request , 'Congratulations! Your Account is activated')
        return redirect ('login')
    else:
        messages.error(request , "Invalid activation link")
        return redirect ('register')

@login_required (login_url = 'login')
def dashboard (request):
    return render (request , 'accounts/dashboard.html')


def forgetPassword (request):
    # الفكرة الرئيسة  
#   [لو الايميل موجود في [كلاس اكونت دوت اوبجيكتس
#   اليوزر هيساوي نفس الايميل بالحروف الحساسة 
# عشان نرسل له الاكتيفيشن
    if request.method == 'POST':
        email = request.POST.get('email') # POST ['email']
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__exact = email)
            # __exact => filter & Case Sensetive البحث الدقيق الحساس للحروف
            # iexact For a case insensitive search, use the iexact lookup  حروف غيرحساسة
            # Q __icontains => Search vs __exact
                         # Copy & Paste Activation
            current_site = get_current_site(request) 
            mail_subject = 'Reset Your Password'
            to_email   = email
            message = render_to_string ('accounts/reset_password_email.html' , {
                'user': user,
                'domain': current_site ,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)), 
                'token' : default_token_generator.make_token(user), 
            })
            send_email = EmailMessage (mail_subject , message , to = [to_email]) 
            send_email.send()
            messages.success(request , 'password reset email has been sent to your email')
            return redirect ('login')

        else:
            messages.error(request , "email Not Exist")
            return redirect ('forgetPassword')

    return render (request , 'accounts/forgetPassword.html')

def resetpassword_validate (request, uidb64 , token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError , ValueError , OverflowError , Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user , token):
        request.session['uid'] = uid
        messages.success(request , 'Please reset your password')
        return redirect ('resetPassword')
    else:
        messages.error(request , 'This Link has been expired')
        return redirect ('login')

def resetPassword (request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user= Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request ,'Password reset Successful')
            return redirect ('login')
        else: 
            messages.error(request , 'Password not matching')
            return redirect ('resetPassword')
    else:        
        return render (request , 'accounts/resetPassword.html')

  



                              # Base64URL Encode 
# Base64URL Encode هي أداة مجانية عبر الإنترنت لتحويل البيانات
#  إلى قيمة Base64 والتي يمكن استخدامها بأمان لعناوين URL وأسماء الملفات. 

# يمكنك إرسال البيانات التي تريد تشفيرها إلى Base64URL عن طريق
#  كتابة نص أو لصقه، أو تحميل ملف، أو تحديد عنوان URL.


# Base64URL Decode هي أداة مجانية عبر الإنترنت لفك تشفير قيم Base64URL إلى 
# البيانات الأصلية. 
# افتراضيًا، يقوم بفك تشفير Base64URL كنص عادي، ومع ذلك، فهو يدعم أيضًا البيانات الثنائية، مثل الصور أو الملفات الأخرى.



# push code to GitHub: (terminal of project) 4- Steps
# git status
# git add -A
# git commit -m "django authentication"
# git push origin main