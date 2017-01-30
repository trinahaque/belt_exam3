from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Appointment
from datetime import datetime, date


def index(request):
    if 'first_name' in request.session:
        return redirect('/success')
    return render(request, "first_app/index.html")

def success(request):
    if 'first_name' in request.session:
        request.session['today'] = unicode(datetime.today().date())
        appointments = Appointment.objects.filter(user_id=request.session['id']).exclude(date=unicode(datetime.today().date()))
        todays_appointments = Appointment.objects.filter(user_id=request.session['id'], date=unicode(datetime.today().date()))
        context = {
            "appointments": appointments,
            "today": todays_appointments
        }
        return render(request, "first_app/success.html", context)
    return redirect('/')


def registration(request):
    if request.method == "POST":
        result = User.objects.registration(request)
        if result[0] == False:
            for error in result[1]:
                messages.add_message(request, messages.INFO, error)
        else:
            messages.success(request, 'Registration successful')
    return redirect("/")


def login(request):
    if request.method == "POST":
        result = User.objects.login(request)
        if result[0] == False:
            for error in result[1]:
                messages.add_message(request, messages.INFO, error)
        else:
            request.session['first_name']= result[1].first_name
            request.session['id'] = result[1].id
            return redirect('/success')
    return redirect("/")

def add_appointment(request, id):
    date = request.POST['date']
    time = request.POST['time']
    task = request.POST['task']

    valid = True
    if len(date) < 1 or len(time) < 1 or len(task)<1:
        messages.warning(request, "A field can not be empty")
        valid = False
    else:
        if date < unicode(datetime.today().date()):
            messages.warning(request, 'Appointment can not be in the past')
            valid = False
    if valid:
        user = User.objects.get(id=id)
        add_appointment = Appointment.objects.create(date=date, time=time, task =task, user=user)
    return redirect('/success')

def appointments(request):
    if 'first_name' in request.session:
        # request.session['appointment_id']=id
        # new_task = request.POST['task']
        # status = request.POST['status']
        # date = request.POST['date']
        # time = request.POST['time']
        #
        # valid = True
        # if len(new_task)< 1 or len(status) < 1 or len(date) < 1 or len(time) < 1:
        #     messages.warning(request, 'A field can not be empty')
        #     valid = False
        # else:
        #     if date < unicode(datetime.today().date()):
        #         messages.warning(request, 'Appointment can not be in the past')
        #         valid = False
        return render(request, 'first_app/appointments.html')

def update(request, id):
    if 'first_name' in request.session:
        new_task = request.POST['task']
        status = request.POST['status']
        date = request.POST['date']
        time = request.POST['time']

        valid = True
        if len(new_task)< 1 or len(status) < 1 or len(date) < 1 or len(time) < 1:
            messages.warning(request, 'A field can not be empty')
            valid = False
        else:
            if date < unicode(datetime.today().date()):
                messages.warning(request, 'Appointment can not be in the past')
                valid = False
        if valid:
            update_task = Appointment.objects.filter(user_id=request.session['id'], id=id).update(task=new_task, date=date, time=time, status=status)
            return redirect('/success')
        return redirect('/appointments')

    return redirect('/')

def delete(request, id, aid):
    user = User.objects.get(id=request.session['id'])
    delete_appointment = Appointment.objects.get(user=user, id=aid).delete()
    return redirect('/success')

def logout(request):
    if 'first_name' in request.session:
        request.session.pop('first_name')
    return redirect('/')
