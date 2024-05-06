from . models import Category

def menu_links (request): 
    links = Category.objects.all()
    return dict (links = links)


#dict => passing a dictionary to all templates using context_processors
    #1- in Choice


# Try VS Except
    # try: Code that might cause an exception.
    # except: Code that handles the exception.
    # يمكنك تغليف تعليمات برمجية من المحتمل أن تكون عرضة للخطأ داخل كتلة محاولة، ثم تقوم كتل الالتقاط والاستثناء بتحديد الإجراءات للتعامل مع هذه الأخطاء.    


# except VS exception
    #  ولذلك، فإن "باستثناء:" يلتقط جميع الاستثناءات، بما في ذلك الاستثناءات المضمنة والاستثناءات المعرفة من قبل المستخدم، في حين أن "باستثناء الاستثناء:" يلتقط فقط الاستثناءات المشتقة من فئة الاستثناء الأساسية.

# except VS exception

    # except: would handle all exceptions, whereas except Exception: would handle only exceptions derived from 'Exception' class, rest of the exceptions would pass through.
    #  Exception: سيتعامل مع جميع الاستثناءات، في حين أن Exception: سيتعامل فقط مع الاستثناءات المشتقة من فئة 'Exception'، وستمر بقية الاستثناءات.

    # Some system exiting exceptions like Keyboard Interrupt or System Exit would be caught by except: and not by except Exception: as they are based on BaseException
    # سيتم اكتشاف بعض الاستثناءات التي تخرج من النظام مثل مقاطعة لوحة المفاتيح أو خروج النظام من خلال الاستثناء: وليس من خلال الاستثناء: لأنها تعتمد على BaseException