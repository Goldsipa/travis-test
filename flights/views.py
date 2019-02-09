from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
  context = {
    'flights': Flight.objects.all() # pylint: disable=no-member
  }
  return render(request, 'flights/index.html', context)

def flight(request, flight_id):
  try:
    flight = Flight.objects.get(pk=flight_id) # pylint: disable=no-member
  except Flight.DoesNotExist: # pylint: disable=no-member
    raise Http404('Flight does not exist.')
  context = {
    'flight': flight,
    'passengers': flight.passengers.all(),
    'non_passengers': Passenger.objects.exclude(flights=flight).all() # pylint: disable=no-member
  }
  return render(request, "flights/flight.html", context)

def book(request, flight_id):
  try:
    passenger_id = int(request.POST['passenger'])
    passenger = Passenger.objects.get(pk=passenger_id) # pylint: disable=no-member
    flight = Flight.objects.get(pk=flight_id) # pylint: disable=no-member
  except KeyError:
    return render(request, 'flights/error.html', {'message': 'No selection'})
  except Flight.DoesNotExist: # pylint: disable=no-member
    return render(request, 'flights/error.html', {'message': 'No flight.'})
  except Passenger.DoesNotExist: # pylint: disable=no-member
    return render(request, 'flights/error.html', {'message': 'No passenger.'})

  passenger.flights.add(flight)
  return HttpResponseRedirect(reverse("flight", args=(flight_id,)))