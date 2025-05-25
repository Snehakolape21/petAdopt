from django.contrib import admin
from petadoptapp.models import pet,cart,adopt,Contact
# Register your models here.


class petAdmin(admin.ModelAdmin):
    list_display=['id','name','age','gender','type','description','price','image']
    list_filter=['type','price']
    
class cartAdmin(admin.ModelAdmin):
    list_display=['id','uid','petid']
    
class adoptAdmin(admin.ModelAdmin):
    list_display=['id','adoptid','petid','userid','adopt_date'] 
    list_filter=['petid','userid'] 
    
class contactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'message', 'submitted_at']
    search_fields = ['name', 'email', 'message']
    list_filter = ['submitted_at']
    
admin.site.register(pet,petAdmin)
admin.site.register(cart,cartAdmin)
admin.site.register(adopt,adoptAdmin)   
admin.site.register(Contact,contactAdmin) 