import os
from django.shortcuts import render, redirect,get_list_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date,datetime
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import CaseForm, CaseTypeForm, CourtForm, PoliceStationForm, ClientForm, BulkUploadForm
from .models import Case, CaseType, Court, PoliceStation, Client, DefaultDrafting, Draftings
from users.models import User
from datetime import date, timedelta
import pandas as pd
from django.http import FileResponse
from django.conf import settings
import os


# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

@login_required(login_url="/login/")
def cases(request):
    return render(request, 'cases/cases.html')

# Case Types
@login_required(login_url="/login/")
def casetype_setup(request):
    if request.method == 'POST':
        form = CaseTypeForm(request.POST)
        if form.is_valid():
            form.instance.user_id= request.user.id
            form.save()
            return redirect('case-type')
    else:
        form = CaseTypeForm()
        user = request.user.id
    casetypes = CaseType.objects.filter(user=user)

    return render(request, 'cases/case_type.html',{'form':form, 'casetypes': casetypes,})

@login_required(login_url="/login/")
def bulk_upload_casetype(request):
    if request.method == 'POST':
        bulk_form = BulkUploadForm(request.POST, request.FILES)
        if bulk_form.is_valid():
            uploaded_file = request.FILES['file']

            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                return render(request, 'cases/unsupported_file.html')

            user = request.user if request.user.is_authenticated else None

            for index, row in df.iterrows():
                case_types = CaseType(
                    user=user,  # Set the user for the Client object
                    case_type=row['Case Types'],
                )
                case_types.save()

            return redirect('case-type')
    else:
        bulk_form = BulkUploadForm()

    return render(request, 'cases/bulk_upload_casetype.html', {'bulk_form': bulk_form})


@login_required(login_url="/login/")
def bulk_download_casetype(request):
    file = os.path.join(settings.BASE_DIR,'static/files/bulk-case-type.xlsx')
    fileOpened = open(file,'rb')
    return FileResponse(fileOpened)
    

@login_required(login_url="/login/")
def casetype_update(request, id):
    casetype = CaseType.objects.get(pk=id)

    if request.method == 'POST':
        casetypeupdate = CaseTypeForm(request.POST, instance =casetype)
        if casetypeupdate.is_valid():
            casetypeupdate.save()
            return redirect('case-type')
    else:
        casetypeupdate = CaseTypeForm(instance =casetype)

    user = request.user.id
    casetypes = CaseType.objects.filter(user=user)
    return render(request, 'cases/case_type.html', {'casetypeupdate': casetypeupdate, 'casetypes': casetypes})

@login_required(login_url="/login/")
def court_setup(request):
    if request.method == 'POST':
        form = CourtForm(request.POST)
        if form.is_valid():
            form.instance.user_id= request.user.id
            form.save()
            return redirect('courts')
    else:
        form = CourtForm()
        user = request.user.id
    courts = Court.objects.filter(user=user)

    return render(request, 'cases/courts.html',{'form':form, 'courts': courts})

@login_required(login_url="/login/")
def bulk_upload_courts(request):

    if request.method == 'POST':
        bulk_form = BulkUploadForm(request.POST, request.FILES)
        if bulk_form.is_valid():
            uploaded_file = request.FILES['file']
            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                return render(request, 'cases/unsupported_file.html')

            user = request.user if request.user.is_authenticated else None

            for index, row in df.iterrows():
                courts = Court(
                    user=user,  # Set the user for the Client object
                    court=row['Courts'],
                )
                courts.save()

            return redirect('courts')
    else:
        bulk_form = BulkUploadForm()

    return render(request, 'cases/bulk_upload_courts.html', {'bulk_form': bulk_form})


@login_required(login_url="/login/")
def bulk_download_courts(request):
    file = os.path.join(settings.BASE_DIR,'static/files/bulk-court.xlsx')
    fileOpened = open(file,'rb')
    return FileResponse(fileOpened)


@login_required(login_url="/login/")
def court_update(request, court_id):
    court = Court.objects.get(id=court_id)

    if request.method == 'POST':
        form = CourtForm(request.POST, instance=court)
        if form.is_valid():
            form.save()
            return redirect('courts')
    else:
        form = CourtForm(instance=court)

    user = request.user.id
    courts = Court.objects.filter(user=user)

    return render(request, 'cases/courts.html',{'form':form, 'courts': courts})

# Poice Station
@login_required(login_url="/login/")
def police_station_setup(request):
    if request.method == 'POST':
        form = PoliceStationForm(request.POST)
        if form.is_valid():
            form.instance.user_id= request.user.id
            form.save()
            return redirect('stations')
    else:
        form = PoliceStationForm()
        user = request.user.id
    stations = PoliceStation.objects.filter(user=user)
    return render(request, 'cases/police_stations.html',{'form':form, 'stations': stations})

@login_required(login_url="/login/")
def bulk_upload_police_stations(request):
    if request.method == 'POST':
        bulk_form = BulkUploadForm(request.POST, request.FILES)
        if bulk_form.is_valid():
            uploaded_file = request.FILES['file']

            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                return render(request, 'cases/unsupported_file.html')

            user = request.user if request.user.is_authenticated else None

            for index, row in df.iterrows():
                police_station = PoliceStation(
                    user=user,  # Set the user for the Client object
                    station=row['station'],
                )
                police_station.save()

            return redirect('stations')
    else:
        bulk_form = BulkUploadForm()

    return render(request, 'cases/bulk_upload_stations.html', {'bulk_form': bulk_form})


@login_required(login_url="/login/")
def bulk_download_police_station(request):
    file = os.path.join(settings.BASE_DIR,'static/files/bulk-police-station.xlsx')
    fileOpened = open(file,'rb')
    return FileResponse(fileOpened)



@login_required(login_url="/login/")
def police_station_update(request, station_id):
    station = PoliceStation.objects.get(id=station_id)

    if request.method == 'POST':
        form = PoliceStationForm(request.POST, instance=station)
        if form.is_valid():
            form.save()
            return redirect('stations')
    else:
        form = PoliceStationForm(instance=station)

    user = request.user.id
    stations = PoliceStation.objects.filter(user=user)
    return render(request, 'cases/police_stations.html',{'form':form, 'stations': stations})

@login_required(login_url="/login/")
def getAllCases(request):
    current_user = request.user
    cases = Case.objects.filter(user=current_user)
    return render(request, 'cases/all_cases.html', {'cases': cases})

@login_required(login_url="/login/")
def addClient(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('all-client')
    else:
        form = ClientForm()

    return render(request, 'cases/add_client.html', {'form':form})

@login_required(login_url="/login/")
def bulk_upload_clients(request):
    if request.method == 'POST':
        bulk_form = BulkUploadForm(request.POST, request.FILES)
        if bulk_form.is_valid():
            uploaded_file = request.FILES['file']

            if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                return render(request, 'cases/unsupported_file.html')

            user = request.user if request.user.is_authenticated else None

            for index, row in df.iterrows():
                client = Client(
                    user=user,  # Set the user for the Client object
                    name=row['name'],
                    branch=row['branch'],
                    chamber_file_number=row['chamber_file_number'],
                    Representative=row['Representative'],
                    mobile=row['mobile'],
                    additional_mobile=row['additional_mobile'],
                    email=row['email'],
                    address=row['address'],
                    short_note=row['short_note'],
                )
                client.save()

            return redirect('all-client')  # Redirect to a success page or client list page
    else:
        bulk_form = BulkUploadForm()

    return render(request, 'cases/bulk_upload_clients.html', {'bulk_form': bulk_form})


@login_required(login_url="/login/")
def bulk_download_client(request):
    file = os.path.join(settings.BASE_DIR,'static/files/bulk-client-add.xlsx')
    fileOpened = open(file,'rb')
    return FileResponse(fileOpened)


@login_required(login_url="/login/")
def client_update(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClientForm(instance=client)

    return render(request, 'cases/add_client.html', {'form':form})

@login_required(login_url="/login/")
def getAllClients(request):
    current_user = request.user
    clients = Client.objects.filter(user=current_user)
    return render(request, 'cases/all_client.html', {'clients': clients})

@login_required(login_url="/login/")
def createCase(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('dashboard')
    else:
        form = CaseForm()
    return render(request, 'cases/create_case.html', {'form': form})

# Todays Cases
@login_required(login_url="/login/")
def todays_case_list(request):
    current_user = request.user
    today = date.today()
    todays_cases = Case.objects.filter(date=today, user=current_user)
    return render(request, 'cases/todays_cases.html', {'todays_cases': todays_cases})

# Tomorrows Cases
@login_required(login_url="/login/")
def tomorrows_case_list(request):
    current_user = request.user
    tomorrow = date.today() + timedelta(days=1)
    tomorrows_cases = Case.objects.filter(date=tomorrow, user=current_user)
    return render(request, 'cases/tomorrows_cases.html', {'tomorrows_cases': tomorrows_cases})

# Running Cases
@login_required(login_url="/login/")
def running_case_list(request):
    current_user = request.user
    running_cases = Case.objects.filter(status='Running', user=current_user)
    return render(request, 'cases/running_cases.html', {'running_cases': running_cases})

# Abandoned Cases
@login_required(login_url="/login/")
def abandoned_case_list(request):
    current_user = request.user
    abandoned_cases = Case.objects.filter(status='Abandoned', user=current_user)
    return render(request, 'cases/abandoned_cases.html', {'abandoned_cases': abandoned_cases})

# Decided Cases
@login_required(login_url="/login/")
def decided_case_list(request):
    current_user = request.user
    decided_cases = Case.objects.filter(status='Decided', user=current_user)
    return render(request, 'cases/decided_cases.html', {'decided_cases': decided_cases})

# Not Updated Cases
@login_required(login_url="/login/")
def not_updated_case_list(request):
    current_user = request.user
    not_updated_cases = Case.objects.filter(updated=False, user=current_user)
    return render(request, 'cases/not_updated_cases.html', {'not_updated_cases': not_updated_cases})



@login_required(login_url="/login/")
def importantLinks(request):
    return render(request,'links/importantlinks.html')
@login_required(login_url="/login/")
def barcouncil(request):
    return render(request,'links/barcouncil.html')

@login_required(login_url="/login/")
def dhakabarassociation(request):
    return render(request,'links/dhakabarassociation.html')

@login_required(login_url="/login/")
def dhakataxbarassociation(request):
    return render(request,'links/dhakataxbarassociation.html')

@login_required(login_url="/login/")
def lawsofbd(request):
    return render(request,'links/lawsofbd.html')

@login_required(login_url="/login/")
def lawyerclubbd(request):
    return render(request,'links/lawyerclubbd.html')

@login_required(login_url="/login/")
def nationalportalbd(request):
    return render(request,'links/nationalportalbd.html')

@login_required(login_url="/login/")
def supremecourtbd(request):
    return render(request,'links/supremecourtbd.html')

@login_required(login_url="/login/")
def draftings(request):
    cases = Case.objects.filter(user=request.user)
    context={
        'cases':cases,
    }

    return render(request,'draftings/caseselect.html',context)

@login_required(login_url="/login/")
def onedrafting(request):
    case_id = request.POST.get('case_id')
    cases = Case.objects.filter(id=case_id,user=request.user)
    defaults = DefaultDrafting.objects.all()
    context={
        'cases':cases,
        'defaults':defaults,
        'case_id':case_id
    }
    return render(request,'draftings/onedrafting.html', context)

@login_required(login_url="/login/")

def preparedrafting(request, case_id, drafting_id):
    case= Case.objects.get(id=case_id)
    draft = DefaultDrafting.objects.get(id=drafting_id)

    context={
        'case':case,
        'draft':draft,
    }

    if request.method == 'POST':
        case_id = request.POST.get('case_id')
        case_no =request.POST.get('case_no')
        law_section = request.POST.get('law_section')
        first_party = request.POST.get('first_party')
        second_party = request.POST.get('second_party')
        title = request.POST.get('title')
        title2 = request.POST.get('title2')
        text1 = request.POST.get('text1')
        text2 = request.POST.get('text2')
        text3 = request.POST.get('text3')
        text4 = request.POST.get('text4')
        text5 = request.POST.get('text5')
        text6 = request.POST.get('text6')
        text7 = request.POST.get('text7')
        text8 = request.POST.get('text8')
        text9 = request.POST.get('text9')
        text10 = request.POST.get('text10')

        user= User.objects.get(id=request.user.id)
        case = Case.objects.get(id=case_id)

        # Draftings.objects.create(user=user,cases=case,title=title,title2=title2,text1=text1, text2=text2, text3=text3, text4=text4, text5=text5, text6=text6,text7=text7, text8=text8,text9=text9,text10=text10).save()


        # template_path = 'draftings/draftingpdf.html'
        # context = {'case_no': case_no,
        #            'law_section':law_section,
        #            'first_party':first_party,
        #            'second_party':second_party,
        #            'title':title,
        #            'title2':title2,
        #            'text1': text1,
        #            'text2': text2,
        #            'text3': text3,
        #            'text4': text4,
        #            'text5': text5,
        #            'text6': text6,
        #            'text7': text7,
        #            'text8': text8,
        #            'text9': text9,
        #            'text10': text10,
        #            }
        # # Create a Django response object, and specify content_type as pdf
        # response = HttpResponse(content_type='application/pdf')

        # response['Content-Disposition'] = 'filename="drafting.pdf"'
        # # find the template and render it.
        # template = get_template(template_path)
        # html = template.render(context)

        # # create a pdf
        # pisa_status = pisa.CreatePDF(
        # html, dest=response)
        # # if error then show some funny view
        # if pisa_status.err:
        #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
        # return response


        context = {
                    'case':case,
                    'case_no': case_no,
                   'law_section':law_section,
                   'first_party':first_party,
                   'second_party':second_party,
                   'title':title,
                   'title2':title2,
                   'text1': text1,
                   'text2': text2,
                   'text3': text3,
                   'text4': text4,
                   'text5': text5,
                   'text6': text6,
                   'text7': text7,
                   'text8': text8,
                   'text9': text9,
                   'text10': text10,
                   }
        return render(request, 'draftings/pdf.html',context)




    return render(request, 'draftings/drafting.html', context)


@login_required(login_url="/login/")
def calculators(request):
    return render(request,'dashboard/calculator.html')

@login_required(login_url="/login/")
def custodycalculation(request):


    if request.method == 'POST':
        custody= request.POST.get('custodydate')
        hearing= request.POST.get('hearing')
        d1 = datetime.strptime(custody, "%Y-%m-%d")
        d2 = datetime.strptime(hearing, "%Y-%m-%d")
        calculate = d2-d1

        context={
            'calculate': calculate
        }

        return render(request,'dashboard/custodycalculator.html',context)

    return render(request,'dashboard/custodycalculator.html')

# def generate_pdf(request):
#     from io import BytesIO

#     # Get the data from the Case model (you may need to modify this query based on your use case)
#     cases = Case.objects.all()

#     # Create a BytesIO buffer to hold the PDF
#     buffer = BytesIO()

#     # Create the PDF canvas with the buffer and set the page size to letter
#     p = canvas.Canvas(buffer, pagesize=letter)

#     # Add content to the PDF
#     p.setFont("Helvetica", 12)
#     p.drawString(100, 800, "Case List")

#     # Iterate through the cases and add the data to the PDF
#     y = 780  # Initial y position for the content
#     for case in cases:
#         p.drawString(100, y, f"Case No: {case.case_no}")
#         p.drawString(100, y - 20, f"Status: {case.status}")
#         # Add more data here if needed
#         y -= 40  # Decrement y position for the next case

#     # Save the PDF
#     p.save()

#     # Get the value of the buffer and create the HTTP response with PDF content
#     pdf_data = buffer.getvalue()
#     buffer.close()

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="case_list.pdf"'
#     response.write(pdf_data)

#     return response



