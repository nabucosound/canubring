from django.contrib import admin
from cargos.models import Cargo, CargoComment


class CargoCommentInline(admin.TabularInline):
    model = CargoComment
    raw_id_fields = ('user',)


class CargoAdmin(admin.ModelAdmin):
    list_display = ('trip', 'requesting_user', 'traveller_user', 'state')
    search_fields = ('requesting_user', 'traveller_user')
    raw_id_fields = ('requesting_user', 'traveller_user')
    inlines = [CargoCommentInline]


class CargoCommentAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'user', 'content')
    search_fields = ('cargo__trip', 'user__username', 'content')
    raw_id_fields = ('cargo', 'user')

admin.site.register(Cargo, CargoAdmin)
admin.site.register(CargoComment, CargoCommentAdmin)

