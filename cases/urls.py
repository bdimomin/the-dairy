from django.urls import path

from . import views

urlpatterns = [
    path('cases/', views.cases , name='cases'),
    
    # <---------- CaseType Section ------------->
    path('case-type/',views.casetype_setup, name='case-type'),
    path('case-type/<int:id>/',views.casetype_update, name='edit-case-type'),
    path('casetype-bulk-upload/', views.bulk_upload_casetype, name='bulk_upload_casetype'),
    path('bulk-casetype-download/',views.bulk_download_casetype, name='bulk_download_casetype'),


    # <---------- Courts Section ------------->
    path('courts/',views.court_setup, name='courts'),
    path('courts/<int:court_id>/',views.court_update, name='edit-court'),
    path('courts-bulk-upload/', views.bulk_upload_courts, name='bulk_upload_courts'),
    path('bulk-courts-download/',views.bulk_download_courts, name='bulk_download_courts'),

    # <---------- Stations Section ------------->
    path('stations/',views.police_station_setup, name='stations'),
    path('stations/<int:station_id>/',views.police_station_update, name='edit-stations'),
    path('stations-bulk-upload/', views.bulk_upload_police_stations, name='bulk_upload_stations'),
    path('bulk-police-station-download/',views.bulk_download_police_station, name='bulk_download_police_station'),

    # <---------- Client Section ------------->
    path('add-client/',views.addClient, name='add-client'),
    path('update-client/<int:client_id>',views.client_update, name='update-client'),
    path('all-client/',views.getAllClients, name='all-client'),
    path('client-bulk-upload/', views.bulk_upload_clients, name='bulk_upload_clients'),
    path('bulk-client-download/',views.bulk_download_client, name='bulk_download_client'),

    path('create-case/',views.createCase, name='create-case'),
    path('all-cases/',views.getAllCases,name='all-cases'),
    path('todays-cases/',views.todays_case_list,name='todays-cases'),
    path('tomorrows-cases/',views.tomorrows_case_list,name='tomorrows-cases'),
    path('running-cases/',views.running_case_list,name='running-cases'),
    path('decided-cases/',views.decided_case_list,name='decided-cases'),
    path('abandoned-cases/',views.abandoned_case_list,name='abandoned-cases'),
    path('notupdated-cases/',views.not_updated_case_list,name='notupdated-cases'),
    
    path('important-links/', views.importantLinks, name="important-links"),
    path('important-links/barcouncil/', views.barcouncil, name="barcouncil"),
    path('important-links/dhakabarassociation/', views.dhakabarassociation, name="dhakabarassociation"),
    path('important-links/dhakataxbarassociation/', views.dhakataxbarassociation, name="dhakataxbarassociation"),
    path('important-links/lawsofbd/', views.lawsofbd, name="lawsofbd"),
    path('important-links/lawyerclubbd/', views.lawyerclubbd, name="lawyerclubbd"),
    path('important-links/nationalportalbd/', views.nationalportalbd, name="nationalportalbd"),
    path('important-links/supremecourtbd/', views.supremecourtbd, name="supremecourtbd"),
    
    
    path('draftings/', views.draftings, name="draftings"),
    path('drafting/', views.onedrafting, name="onedrafting"),
    path('drafting/<int:case_id>/<int:drafting_id>/', views.preparedrafting, name="preparedrafting"),
    
    path('calculators/', views.calculators, name="calculators"),
    path('calculators/custody/', views.custodycalculation, name="custodycalculation"),
     
]