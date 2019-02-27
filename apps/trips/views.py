from django.shortcuts import render, redirect, HttpResponse
from apps.login_register.models import User
from django.contrib import messages
from .models import Trip

# Create your views here.
def show_trips(request):
    user_trips = Trip.objects.filter(attendes = request.session['user_id'])
    other_trips = Trip.objects.exclude(attendes = request.session['user_id'])
    context = {
        'trips':user_trips,
        'other_trips': other_trips
    }

    return render(request, 'trips/trips.html', context)

def show_create_new_trip(request):

    return render(request, 'trips/new_trip.html')

def create_trip(request):
    errors = Trip.objects.create_validator(request.POST)

    if errors != None:
        for tag, message in errors.items():
            messages.error(request, message)
        return redirect ('/trips/new_trip')

    if errors == None:
        created = User.objects.get(id = request.session['user_id'])
        user_trip = Trip.objects.create(destination = request.POST['destination'], plan = request.POST['plans'], start_date = request.POST['start_date'], end_date = request.POST['end_date'], created_by = created)
        user_trip.attendes.add(created)
    return redirect ('/trips')

def view_trip(request, id):
    trip_id = int(id)
    view_trip = Trip.objects.get(id=trip_id)
    going = view_trip.attendes.all()

    context = {
        'trip_info': view_trip,
        'attending' : going
    }

    return render(request, 'trips/view_trip.html', context)

def remove_trip(request, id):
    trip_id = int(id)
    remove_trip = Trip.objects.get(id=trip_id)
    remove_trip.delete()

    return redirect('/trips')

def show_edit_trip(request, id):
    trip_id = int(id)
    edit_trip = Trip.objects.get(id=trip_id)

    context = {
        'edit_trip' : edit_trip
    }
    return render(request, 'trips/edit_trip.html', context)


def edit_trip(request):
    update_trip = Trip.objects.get(id = request.POST['trip_id'])
    errors = Trip.objects.trip_validator(request.POST)

    if errors != None:
        for tag, message in errors.items():
            messages.error(request, message)
        return redirect(f'/trips/edit/{update_trip.id}')

    if errors == None:
        update_trip.destination = request.POST['edit_destination']
        update_trip.start_date = request.POST['edit_start_date']
        update_trip.end_date = request.POST['edit_end_date']
        update_trip.plan = request.POST['edit_plans']
        update_trip.save()

        return redirect('/trips')


def join_trip(request, id):
    trip_id = int(id)
    trip_joining = Trip.objects.get(id = trip_id)
    attendee = User.objects.get(id = request.session['user_id'])
    trip_joining.attendes.add(attendee)

    return redirect('/trips')

def cancel(request, id):
    trip_id = int(id)
    trip_canceling = Trip.objects.get(id = trip_id)
    attendee = User.objects.get(id = request.session['user_id'])
    trip_canceling.attendes.remove(attendee)

    return redirect('/trips')






def logout(request):

    return redirect('/')