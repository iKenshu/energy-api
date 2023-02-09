import datetime, calendar

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .validators import validate_date, validate_period
from .models import Energy
from .serializers import EnergySerializer


class ListAPIView(APIView):
    def _compare_items(self, item, prev_item, date):
        if item:
            total_energy = item.active_energy - prev_item
            prev_item = item.active_energy
            item.active_energy = total_energy
        else:
            item = Energy(meter_date=date, active_energy=0.0)
        return item, prev_item

    def _get_energy(self, energy, days):
        days_data = []
        prev_item = 0
        for date in days:
            format_date = date.strftime("%Y-%m-%d")
            item = energy.filter(meter_date__contains=format_date).last()
            item, prev_item = self._compare_items(item, prev_item, date)
            days_data.append(item)
        return days_data

    def _get_daily(self, qs, date):
        hours = []
        prev_day = (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        prev_item = qs.filter(meter_date__contains=prev_day).last()
        if prev_item:
            prev_item = prev_item.active_energy
        else:
            prev_item = 0

        qs = qs.filter(meter_date__contains=date.strftime("%Y-%m-%d"))

        for hour in range(0, 24):
            item = qs.filter(meter_date__hour=hour).last()
            item, prev_item = self._compare_items(item, prev_item, date)
            date += datetime.timedelta(hours=1)
            if item not in hours:
                hours.append(item)
        return hours

    def get(self, request, format=None):
        energy = Energy.objects.all()
        serializer = EnergySerializer(energy, many=True)

        period = request.query_params.get("period")
        date = request.query_params.get("date")

        validate_date(date)
        validate_period(period)

        if not date:
            date = datetime.date.today()

        qs = energy.filter(meter_date__contains=date)

        if qs:
            current_date = qs.first().meter_date

        if period == "daily":
            current_date = current_date.replace(hour=0)
            energy = self._get_daily(energy, current_date)
        elif period == "weekly":
            dates = [
                current_date + datetime.timedelta(days=i)
                for i in range(
                    0 - current_date.weekday(), 7 - current_date.weekday()
                )
            ]
            energy = self._get_energy(energy, dates)
        elif period == "monthly":
            num_days = calendar.monthrange(
                current_date.year, current_date.month
            )[1]
            days = [
                datetime.datetime(
                    current_date.year, current_date.month, day, 0, 0, 0
                )
                for day in range(1, num_days + 1)
            ]
            energy = self._get_energy(energy, days)

        serializer = EnergySerializer(energy, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
