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
            first_name  = first_name,
            last_name   = last_name,
            username    = username,
            email       = self.normalize_email(email),
    )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self, first_name , last_name , username , email , password):
        user = self.create_user(
            first_name = first_name,
            last_name  = last_name,
            username   = username,
            email      = self.normalize_email(email),
            password   = password,
        )
        user.is_admin      = True
        user.is_active     = True
        user.is_staff      = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user

 # raise استثناءات عند كتابة برمجية وسيطة

    # user.setpassword 
 # إعدادات الباسورد Single Function
 
 #  self.normalize_email(email)   => من غير كإبيتإل 

 #AbstractBaseUser (أسهل طريقة لإنشاء نموذج مستخدم مخصص متوافق هي الوراثة من . يوفر   في ذلك كلمات المرور المجزأة وإعادة تعيين كلمات المرور المميزة. ة)
# يجب عليك بعد ذلك تقديم بعض تفاصيل التنفيذ الرئيس USERNAME_FIELD¶
# USERNAME_FIELD = "المعرف"
#سلسلة تصف اسم حقل البريد الإلكتروني في نموذج المستخدم. يتم إرجاع هذه القيمة بواسطة get_email_field_name().
# الحقول المطلوبة¶
#قائمة بأسماء الحقول التي سيتم المطالبة بها عند إنشاء مستخدم عبر أمر إدارة createsuperuser. سيُطلب من المستخدم توفير قيمة لكل حقل من هذه الحقول. يجب أن يتضمن أي حقل يكون الفراغ فيه خطأ أو غير محدد وقد يتضمن حقولًا إضافية تريد المطالبة بها عند إنشاء مستخدم بشكل تفاعلي. REQUIRED_FIELDS ليس له أي تأثير في أجزاء أخرى من Django، مثل إنشاء مستخدم في المشرف.


class Account (AbstractBaseUser): #(5 +6)
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
    #     متاح يطلع على الابليكيشن    
                   # def has_perm(self, perm, obj=None):
    # "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
    # return True

                   # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True



                        # auto_add  vs  auto_add_now
                        # تحديث     vs  انشاء أول مرة


#               _db =>  using=self._db
# تم استخدام هذا في حالة وجود قواعد بيانات متعددة
#  يمكنك من خلالها تحديد قاعدة البيانات التي تحتاج إلى استخدامها للتشغيل     
#                 +
# ثم إذا كنت تريد استخدام قاعدة البيانات الافتراضية، فاستخدم
# user.save(using=self._db)
#  فاستخدم new_users إذا كنت تريد استخدام قاعدة بيانات 
#   user.save(using=new_users)


#                          self.model
#  إذن هنا تقوم عادةً بإنشاء مثيل مستخدم (أو مثيل لنموذج آخر استخدمته لتمثيل المستخدمين). يمكنك بعد ذلك استخدام
#   user.save()‎ لحفظ هذا المثيل في قاعدة البيانات وإعادته 
             

# __iexact => (SEARC) مزاوجة غير حساسة لحالة الأحرف