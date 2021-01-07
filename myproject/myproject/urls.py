
from django.contrib import admin
from django.urls import include, path

from planer import views as pviews

urlpatterns = [
    path('', pviews.index, name = 'index'),
    path('signin/', pviews.signin, name = 'signin'),
    path('signup/', pviews.signup, name = 'signup'),
    path('logout/', pviews.signout, name = 'signup'),
    path('eventcreation/', pviews.create_event, name = 'eventcreation'),
    path('eventdelete/', pviews.delete_event, name = 'evntdelete'),
    path('eventedit/', pviews.edit_event, name = 'evntedit'),
    path('eventmove/', pviews.move_event, name = 'evntmove'),
    path('planner/<str:user>', pviews.show_planner, name = 'planner'),
    path('planner/<str:user>/<str:month>', pviews.show_month, name = 'month'),
    path('makecyclical/', pviews.make_cyclical, name = 'makecyclical'),
    path('admin/', admin.site.urls),
]
