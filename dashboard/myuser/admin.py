from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Benutzer, Book, Author, Rating, Movie
from django import forms
from django.utils.html import format_html
from .filters import DecadeBornListFilter
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from django.utils.html import format_html_join
#from django.utils.safestring import mark_saf
admin.site.site_header = "Zakaria Application"
admin.site.index_title ="module"
admin.site.site_title= " Uni"


def export_selected_objects(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))



@admin.register(Benutzer)
class USERAdmin(admin.ModelAdmin):

    list_display= ('title','first_name','upper_case_name','email_in_farbe',"email",'view_first_name',
     "last_name", "date_joined",'jahr','role','is_active' )

    #list_filter = ( "last_name", "date_joined",'role','is_active' )
    search_fields = ("date_joined",'role','is_active' )
    actions = ['aktivieren_status', 'deaktivieren_status', 'make_pulished']
    list_filter = (DecadeBornListFilter,)

     #hier kann man die die values in table bearbeiten
    #list_editable = ('last_name', 'first_name')
    ordering = ['last_name']
    prepopulated_fields = {"last_name": ("first_name",)}
    #autocomplete_fields = ['role']
     #choice auswählen
    radio_fields = {"role": admin.VERTICAL}
    admin.site.add_action(export_selected_objects, 'export_selected')


    #list_display_links =('date_joined', 'is_active')
    fieldsets= (
    (None, {
    'fields':('email', 'last_name')
    }),
    ('Advanced options',{
    #'classes': ('collapse',), hier sind die Advanced ausblend
    'classes': ('wide', 'extrapretty'),
    'fields': ('first_name', 'role')
    }),
    )



    def get_ordering(self, request):
        if request.user.is_superuser:
            return ['last_name', 'first_name']
        else:
            return ['first_name']


    def make_pulished(self, request, queryset):
        rows_update=queryset.update(title='p')
        if rows_update==1:
            message_bit="1 story gefunden"
        else:
            message_bit = "%s stories wer" % rows_update
        self.message_user(request, "erfolgreich makiert" % message_bit)
    make_pulished.short_description = "Markiere ausgewählte Titele as published"


    # gib name in größe Bchstaben zurücombak

    def upper_case_name(self, obj):
        return ('%s %s' %(obj.last_name, obj.first_name)).upper()
    upper_case_name.short_description=("Name")

    #gib die email in farbe zurük

    def email_in_farbe(self, obj):
        return format_html(
        '<span style= color:red;>{} {}</span>',
        obj.email,
        obj.role,
        )



    #raw_id_fields = ("Pages",)
    #list_filter = (AlphabetFilter,)

# with this method i get jsut the activ user in the list
    '''
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_active=True)
    '''

    def deaktivieren_status(self, request, queryset):
        return queryset.update(is_active=False)
    deaktivieren_status.short_description =(" User Deactivieren")

    def aktivieren_status(self, request, queryset):
        return queryset.update(is_active=True)
    aktivieren_status.short_description =(" User Aktivieren")

    def view_first_name(self, obj):
        return obj.first_name
    view_first_name.empty_value_display ='???'




class UserForm(forms.ModelForm):
    model = Benutzer
    exclude = ["first_name"]



class BookInline(admin.TabularInline):
    model= Book

    #list_display= ('title', 'author', 'created')


class AuthorAdmin(admin.ModelAdmin):

    #list_display= ('name', 'geburtsdatum')

    inlines = [
    BookInline,
    ]

admin.site.register(Book)
admin.site.register(Author)

admin.site.register(Movie)
admin.site.register(Rating)


 #
