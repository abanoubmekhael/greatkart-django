from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
class MyAccountManager (BaseUserManager):
    def create_user(self, first_name , last_name , username , email , password=None):
        if not email:
            raise ValueError('User must an email')
        if not username:
            raise ValueError('User must ave an username')
        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name,
    )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self, first_name , last_name , username , email , password):
        user = self.create_user(
            email      = self.normalize_email(email),
            username   = username,
            first_name = first_name,
            password   = password,
            last_name  = last_name,
        )
        user.is_admin      = True
        user.is_active     = True
        user.is_staff      = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user


    # user.setpassword 
 # إغد‘دعت إلبإسورد Single Function
 
 
 #AbstractBaseUser (أسهل طريقة لإنشاء نموذج مستخدم مخصص متوافق هي الوراثة من . يوفر   في ذلك كلمات المرور المجزأة وإعادة تعيين كلمات المرور المميزة. ة)
# يجب عليك بعد ذلك تقديم بعض تفاصيل التنفيذ الرئيس USERNAME_FIELD¶
# USERNAME_FIELD = "المعرف"
#سلسلة تصف اسم حقل البريد الإلكتروني في نموذج المستخدم. يتم إرجاع هذه القيمة بواسطة get_email_field_name().
# الحقول المطلوبة¶
#قائمة بأسماء الحقول التي سيتم المطالبة بها عند إنشاء مستخدم عبر أمر إدارة createsuperuser. سيُطلب من المستخدم توفير قيمة لكل حقل من هذه الحقول. يجب أن يتضمن أي حقل يكون الفراغ فيه خطأ أو غير محدد وقد يتضمن حقولًا إضافية تريد المطالبة بها عند إنشاء مستخدم بشكل تفاعلي. REQUIRED_FIELDS ليس له أي تأثير في أجزاء أخرى من Django، مثل إنشاء مستخدم في المشرف.


class Account (AbstractBaseUser):
    first_name     = models.CharField(max_length = 50  )
    last_name      = models.CharField(max_length = 50  )
    username       = models.CharField(max_length = 50 , unique = True  )
    email          = models.EmailField(max_length = 100 , unique = True  )
    phone_number   = models.CharField(max_length = 50 )

    date_joined    = models.DateTimeField(auto_now_add = True)
    last_login     = models.DateTimeField(auto_now_add = True)
    is_admin       = models.BooleanField(default       = False)
    is_staff       = models.BooleanField(default       = False)
    is_active      = models.BooleanField(default       = False)
    is_superadmin  = models.BooleanField(default       = False)

    USERNAME_FIELD  = 'email'   
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()   # للربط
    def __str__(self):
        return self.email
    
    def has_perm (self , perm , obj=None):
        return self.is_admin
        # لو اليوز هو الادمن فله صلاحيات عمل تغييرات
    def has_module_perms (self, add_label):
        return True
    #     متإح يطلع على إلإب    
    #     def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True



   
    

