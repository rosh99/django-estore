from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from storeapp import views
from django.contrib.auth import views as auth_views

app_name = 'storeapp'

urlpatterns = [
    url(r'^$',views.Indexview.as_view(),name='index'),
    url(r'^login/$',views.loginview,name='login'),
    url(r'^logout/$',auth_views.logout,{'next_page':'storeapp:index'},name='logout'),
    url(r'^item/(?P<slug>[-\w]+)/$',views.item_detail,name='item_detail'),
    url(r'^items/(?P<cat_slug>[-\w]+)/$',views.cat_query,name='cat_query'),
    url(r'^brand/(?P<brand_slug>[-\w]+)/$',views.brand_query,name='brand_query'),
    url(r'^signup/$',views.signupview,name='signup'),
    url(r'^confirm-order/$',views.con_order,name='con_order'),
    url(r'^order-succes/$',views.fin_order,name="fin_order"),
    url(r'^item-search/$',views.searchview,name='item-search')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
