#  تمبلت موديل فيو)الطريقة الاولى ودي بتاع التسجيل وخطواتها) 
#                     بدي نيم في فورم التمبلت
# 1- تمبلت    name='' , form= action
# 2- موديل
# 3- فيو
# 4- Note=>  x = request.method.get(name) || x = request.method['name']
#         بعديهإ
# 4- user = auth.authnticate(email=email , password=password)
# 4- auth.login(request , user)

# =============
# ملحوظة
# =============
#  الطريقة التانية vs الاولى  
# REGISTRATION vs LOGIN
# دي الطريقة التانية مش الاولى  
#  forms.ModelForm 
# مشهورة أوي أوي  => REGISTRATION 
# ملخص
# ملف فورمس دوت بي واي
#  ( كلاس ميتا: وإللي فيه   (موديل - وفيلدس بتاعته
#   +
# (widget = attrs {placeolder: , class: }) ويدجيتس للتنسيق 
# للتسجيل REGISTRATION 
#    in view => form.cleaned_data['first_name']  # To Match data => in view 

#   ركز ضرور جدا

from django import forms
from .models import Account

class RegistrationForm (forms.ModelForm):
    # تنسيق الحقول أو الانبوتس بواسطة بوتستراب
    # widget = forms.PasswordInput(attrs)
    # attrs  = {placeholder & class} => BOOTSTRAP

    password = forms.CharField(widget = forms.PasswordInput(   # تنسيق الفيلدس 
        attrs= {'placeholder':'Enter Password'}))
    confirm_password = forms.CharField(widget = forms.PasswordInput(
        attrs = {'placeholder':'Confirm Password', 'class':'form-control'}))
    # widget = forms.PasswordInput(attrs= {'placeholder':'Enter Password'})
    
    class Meta:  # (Model & Fields)
        model = Account 
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
        
        # widgets 
        # def __init__(self , ? ,?)
    


    def __init__(self, *args, **kwargs):   # تنسيق الفيلدس 
              # فانكشن بدلاً من كتابة كل تنسيق على حدة             
        super(RegistrationForm , self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone_number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean(self):
        cleaned_data     = super(RegistrationForm, self).clean()    #method password & confirm_password
        password         = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password doesnt match'
            )

    #  clean => مطابقة   
         
                 # __init__(self, *args, **kwargs):
#  نسخة من الموديل أو ريجستريشنفورم
# يتوقع Django أن يكون توقيع منشئ النموذج (self، *args، **kwargs)، أو صورة طبق الأصل معقولة.
                                        
                          # *args & **kwargs     
#   عدد الوسائط التي لا تحتوي على كلمات رئيسية والتي يمكن تمريرها والعمليات التي يمكن تنفيذها على الوظيفة في Python، في حين أن **kwargs هو عدد متغير (غير ثابت) من الوسائط التي تحتوي على بارامترات 
# رئيسية مدخلات والتي يمكن تمريرها إلى الفانكشن
# تحدد args
#   (بيانات مزدوجة ) يمكنها إجراء عمليات القاموس .
 

#                  Note: raise (Exceptios)
# raise ValueError (if not email)
# raise ValidationError( password = confirm_password)
 


                    #messages => success vs error
#  لازم تشمل إينكلود في التمبلت {include}
# messages.success(request , 'Registration Successfull')  #messages.success
# message.error(request , 'invalid login Credential')