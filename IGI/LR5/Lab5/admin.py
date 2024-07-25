from django.contrib import admin
from .models import *

admin.site.register(Company)
admin.site.register(FAQ)
admin.site.register(Contact)
admin.site.register(Policy)
admin.site.register(Vacancy)
admin.site.register(PromoCode)
admin.site.register(CustomUser)
admin.site.register(PropertyType)
admin.site.register(Owner)
admin.site.register(BuyerOrTenant)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'num_rooms', 'area', 'year_built', 'display_agents']
    list_filter = ['type', 'year_built']

    def display_agents(self, obj):
        return ", ".join([agent.user.get_full_name() for agent in obj.agents.all()])

    display_agents.short_description = 'Agents'

admin.site.register(Property, PropertyAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'text', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('text',)


admin.site.register(Review, ReviewAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')
    list_filter = ('publish_date',)
    search_fields = ('title',)


admin.site.register(Article, ArticleAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')
    search_fields = ('title', 'summary')


admin.site.register(News, NewsAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'hire_date')
    search_fields = ('user__username', 'position')


admin.site.register(Employee, EmployeeAdmin)
