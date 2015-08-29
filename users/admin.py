from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont

admin.site.unregister(User)

class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    exclude = ('position',)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (CustomUserInline,)
    can_delete = False
    actions = ['print_cards',]
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'first_name', 'last_name', 'email')}
        ),
        (_('Status'), {
            'classes': ('wide', 'collapse',),
            'fields': ('is_active', 'is_superuser', 'is_staff',)}
        ),
        (_('Dates'), {
            'classes': ('wide', 'collapse',),
            'fields': ('last_login', 'date_joined',)}
        ),
    )

    #TODO: Print multiple cards one below each other.
    def print_cards(self, request, queryset):
        for user in queryset:
            if not user.customuser.is_member():
                continue
            im = Image.open('static/member_card.png')
            width = 300
            height = 190
            header_height = 40.0
            interspace = 9.0
            big_width = 70.0
            diff_big_small_width = 6.0
            info_height = 23
            color1 = (52,152,219)
            info = [str(user.customuser.last_membership().expiration_date),
                    str(user.id), user.first_name, user.last_name]
            id_photo = Image.open(user.customuser.id_photo.path)
            font = ImageFont.truetype('DroidSansMono.ttf', 12)
            id_ratio = 45/35

            #Crop the photo to match an id photo ratio.
            if id_photo.height / id_photo.width > id_ratio:
                new_height = id_photo.width * id_ratio
                diff_height = (id_photo.height - new_height)
                id_photo = id_photo.crop((0, int(diff_height/2), id_photo.width,
                    int(id_photo.height - diff_height/2)))
            elif id_photo.height / id_photo.width < id_ratio:
                new_width = id_photo.height / id_ratio
                diff_width = (id_photo.width - new_width)
                id_photo = id_photo.crop((int(diff_width/2), 0,
                    int(id_photo.width - diff_width/2), id_photo.height))

            height_id = int(height - header_height - 25)
            width_id = int(height_id / id_ratio)
            id_photo = id_photo.resize((width_id, height_id))

            draw = ImageDraw.Draw(im)

            space = interspace + header_height
            for value in info:
                #Adapt font size to available space.
                font_size = 15
                font = ImageFont.truetype('DroidSansMono.ttf', font_size)
                (value_width, value_height) = draw.textsize(value, font=font)
                while value_width > width - (big_width + width_id):
                    if font_size == 1:
                        break
                    font_size -= 1
                    font = ImageFont.truetype('DroidSansMono.ttf', font_size)
                    (value_width, value_height) = draw.textsize(value, font=font)

                draw.text((2 + big_width, space + \
                            (info_height - value_height ) / 2), value,
                            fill=color1, font=font)
                space = space + interspace + info_height
                big_width = big_width - diff_big_small_width - \
                    (diff_big_small_width) * (interspace / info_height)


            im.paste(id_photo, (width - id_photo.width - 2, int(header_height + 5)))

            del draw
            response = HttpResponse(content_type='image/png')
            im.save(response, 'PNG')
            return response


    print_cards.short_description = _('Print member cards for the selected users.')
