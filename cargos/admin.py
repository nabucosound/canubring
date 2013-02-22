from django.contrib import admin
from cargos.models import Cargo, CargoComment


class CargoAdmin(admin.ModelAdmin):
    list_display = ('trip', 'requesting_user', 'traveller_user', 'state')
    search_fields = ('requesting_user', 'traveller_user')


class CargoCommentAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'user', 'content')
    search_fields = ('cargo__trip', 'user__username', 'content')

admin.site.register(Cargo, CargoAdmin)
admin.site.register(CargoComment, CargoCommentAdmin)

