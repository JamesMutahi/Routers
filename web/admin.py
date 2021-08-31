from django.contrib import admin
from django.contrib.auth.models import Group

from web.models import *

admin.site.site_header = 'Routers Admin'
admin.site.site_title = 'Routers Admin'
# admin.site.site_url = ''
admin.site.index_title = ''


class CommuteInline(admin.TabularInline):
    model = Commute
    extra = 0


class FareInline(admin.TabularInline):
    model = Fare
    extra = 0


class FareAdmin(admin.ModelAdmin):
    list_display = ['route', 'distance', 'fare', ]
    search_fields = ['fare', 'tld', ]
    fieldsets = [
        (None, {'fields': ['route', 'distance', 'fare', ]}),
    ]


admin.site.register(Fare, FareAdmin)


class BusStopInline(admin.TabularInline):
    model = BusStop
    extra = 0


class BusStopAdmin(admin.ModelAdmin):
    list_display = ['bus_stop', 'tld', ]
    search_fields = ['bus_stop', 'tld', ]
    fieldsets = [
        (None, {'fields': ['bus_stop', 'tld', ]}),
    ]


admin.site.register(BusStop, BusStopAdmin)


class TLDAdmin(admin.ModelAdmin):
    list_display = ['number', 'route', ]
    search_fields = ['number', 'route', ]
    fieldsets = [
        (None, {'fields': ['number', 'route', ]}),
    ]
    inlines = [BusStopInline, ]


admin.site.register(TLD, TLDAdmin)


class TLDInline(admin.TabularInline):
    model = TLD
    extra = 0
    verbose_name = "TLD"
    verbose_name_plural = "TLDs"
    show_change_link = True


class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]
    fieldsets = [
        (None, {'fields': ['name', 'starting_point', 'saccos', ]}),
    ]
    filter_horizontal = ('saccos',)
    inlines = [TLDInline, ]


admin.site.register(Route, RouteAdmin)


class RouteInline(admin.TabularInline):
    model = Route.saccos.through
    extra = 0
    verbose_name = "Route"
    verbose_name_plural = "Routes"


class SaccoAdmin(admin.ModelAdmin):
    list_display = ['name', 'ending_point', ]
    search_fields = ['name', 'ending_point', ]
    fieldsets = [
        (None, {'fields': ['name', 'ending_point', ]}),
    ]
    inlines = [RouteInline, ]


admin.site.register(Sacco, SaccoAdmin)

admin.site.unregister(Group)
