from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from . import models

admin.site.register(models.Category)
admin.site.register(models.Institution)
admin.site.register(models.Donation)

User = get_user_model()
min_admins = 2


def delete_user(request, obj):
    current_user = request.user
    deletions = 0
    message = ""
    try:
        if obj.pk == current_user.pk:
            message = _("Nie możesz usunąć samego siebie")
        elif obj.is_staff:
            staff_users = User.objects.filter(is_staff=True).exclude(pk=current_user.pk)
            if len(staff_users) < min_admins:
                message = _("Nie może zostać mniej niż dwóch adminów")
            else:
                obj.delete()
                deletions += 1
        else:
            obj.delete()
            deletions += 1
    except AttributeError as e:
        # obj.delete()
        message = _("To nie jest obiekt użytkownika")
    except Exception as e:
        # print(e)
        message = _("Wystąpił nieznany błąd")
    return deletions, message


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ["username", "is_staff", "is_superuser", "is_active"]

    def delete_model(self, request, obj):
        deletions, message = delete_user(request, obj)
        if deletions == 0:
            self.message_user(request, message, messages.ERROR)
        else:
            self.message_user(request, _("Użytkownik pomyślnie usunięty"), messages.SUCCESS)

    def delete_queryset(self, request, queryset):
        all_deletions = 0
        all_messages = []
        for obj in queryset:
            deletions, message = delete_user(request, obj)
            if deletions == 0:
                all_messages.append(message)
            else:
                all_deletions += deletions

        if all_deletions:
            self.message_user(request, _(f"Liczba pomyślnie usuniętych wpisów: {all_deletions}"), messages.SUCCESS)

        if all_messages:
            for message in all_messages:
                self.message_user(request, message, messages.ERROR)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
