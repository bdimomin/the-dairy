from django.urls import path

from . import views

urlpatterns = [
    path('cases/', views.cases , name='cases'),
    
    # <---------- CaseType Section ------------->
    path('case-type/',views.casetype_setup, name='case-type'),
    path('case-type/<int:id>/',views.casetype_update, name='edit-case-type'),
    path('casetype-bulk-upload/', views.bulk_upload_casetype, name='bulk_upload_casetype'),

    # <---------- Courts Section ------------->
    path('courts/',views.court_setup, name='courts'),
    path('courts/<int:court_id>/',views.court_update, name='edit-court'),
    path('courts-bulk-upload/', views.bulk_upload_courts, name='bulk_upload_courts'),

    # <---------- Stations Section ------------->
    path('stations/',views.police_station_setup, name='stations'),
    path('stations/<int:station_id>/',views.police_station_update, name='edit-stations'),
    path('stations-bulk-upload/', views.bulk_upload_police_stations, name='bulk_upload_stations'),

    # <---------- Client Section ------------->
    path('add-client/',views.addClient, name='add-client'),
    path('update-client/<int:client_id>',views.client_update, name='update-client'),
    path('all-client/',views.getAllClients, name='all-client'),
    path('client-bulk-upload/', views.bulk_upload_clients, name='bulk_upload_clients'),

    path('create-case/',views.createCase, name='create-case'),
    path('all-cases/',views.getAllCases,name='all-cases'),
    path('todays-cases/',views.todays_case_list,name='todays-cases'),
    path('tomorrows-cases/',views.tomorrows_case_list,name='tomorrows-cases'),
    path('running-cases/',views.running_case_list,name='running-cases'),
    path('decided-cases/',views.decided_case_list,name='decided-cases'),
    path('abandoned-cases/',views.abandoned_case_list,name='abandoned-cases'),
    path('notupdated-cases/',views.not_updated_case_list,name='notupdated-cases'),
]