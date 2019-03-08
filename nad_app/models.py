# -*- coding: utf-8 -*-
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from enumfields import EnumField
from future.utils import python_2_unicode_compatible
from enum import Enum  # Uses Ethan Furman's "enum34" backport


class ReserveType(Enum):
    Hourly = 0
    Daily = 1


class State(Enum):
    In = 0
    Out = 1


@python_2_unicode_compatible
class ParkingType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ReserveStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, max_length=255)
    isAvailable = models.BooleanField(default=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Parking(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, max_length=255)
    type = models.ForeignKey(ParkingType, blank=True, on_delete=models.CASCADE, verbose_name="ParkingType")
    capacity = models.IntegerField(default=50, verbose_name="Capacity")
    entrancePrice = models.FloatField(default=0, verbose_name="EntrancePrice")
    priceForEachHour = models.FloatField(default=0, verbose_name="PriceForEachHour")
    priceForEachDay = models.FloatField(default=0, verbose_name="PriceForEachDay")
    isDaily = models.BooleanField(default=True)
    # this column is an aggregate data for more efficiency
    availableSpace = models.IntegerField(default=50, verbose_name="AvailableSpace")

    def _do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
        return super(Parking, self)._do_update(base_qs, using, pk_val, values, update_fields, forced_update)

    def _do_insert(self, manager, using, fields, update_pk, raw):
        self.availableSpace = self.capacity
        return super(Parking, self)._do_insert(manager, using, fields, update_pk, raw)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        old = Parking.objects.get(id=self.id)
        diff = self.capacity - old.capacity
        self.availableSpace += diff

        super(Parking, self).save(force_insert, force_update, using, update_fields)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "capacity": self.capacity,
            "entrancePrice": self.entrancePrice,
            "priceForEachHour": self.priceForEachHour,
            "priceForEachDay": self.priceForEachDay,
            "isDaily": self.isDaily,
            "availableSpace": self.availableSpace,

        }

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ParkingInOut(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name="User")
    parking = models.ForeignKey(Parking, blank=True, on_delete=models.CASCADE, verbose_name="Parking")
    reserveType = EnumField(ReserveType, max_length=1)
    state = EnumField(State, max_length=1)
    carNumber = models.CharField(max_length=255, verbose_name="carNumber")
    dateTime = models.DateTimeField(auto_now_add=True)
    exited = models.BooleanField(default=False)

    def updateParkingAvailableSpace(self, state, parkingId):
        parking = Parking.objects.get(id=parkingId)
        if state == State.In:
            parking.availableSpace -= 1
        else:
            parking.availableSpace += 1

        parking.save()

    def updateParkingInOutExited(self, user, parkingId):
        parkingInOut = ParkingInOut.objects.get(state=State.In, exited=False, user_id=user, parking_id=parkingId)
        parkingInOut.exited = True
        parkingInOut.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        parkingInNoExited = ParkingInOut.objects.filter(user_id=self.user_id, carNumber=self.carNumber, state=State.In,
                                                        exited=False).all()
        haveToSave = False

        if self.state == State.In:
            if not parkingInNoExited.count() > 0:
                haveToSave = True
                self.updateParkingAvailableSpace(self.state, self.parking_id)
            else:
                if self.exited:
                    haveToSave = True
        else:
            if parkingInNoExited.count() > 0:
                haveToSave = True
                self.updateParkingInOutExited(self.user_id,self.parking_id)
                self.updateParkingAvailableSpace(self.state, self.parking_id)

        if haveToSave:
            super(ParkingInOut, self).save(force_insert, force_update, using, update_fields)

    def as_dict(self):
        return {
            "id": self.id,
            "parking": self.parking,
            "user": self.user,
            "reserveType": self.reserveType,
            "state": self.state,
            "carNumber": self.carNumber,
            "dateTime": self.dateTime,
            "exited": self.exited,
        }

    def __str__(self):
        return self.carNumber


@python_2_unicode_compatible
class CustomerInvoice(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, verbose_name="User")
    parking = models.ForeignKey(Parking, blank=True, on_delete=models.CASCADE, verbose_name="Parking")
    reserveType = EnumField(ReserveType, max_length=1)
    state = EnumField(State, max_length=1)
    entrancePrice = models.FloatField(default=0, verbose_name="EntrancePrice")
    priceForEachHour = models.FloatField(default=0, verbose_name="PriceForEachHour")
    priceForEachDay = models.FloatField(default=0, verbose_name="PriceForEachDay")
    carNumber = models.CharField(max_length=255, verbose_name="carNumber")
    startDateTime = models.DateTimeField(auto_now_add=True)
    finishDateTime = models.DateTimeField()
    totalHours = models.FloatField(default=0, verbose_name="TotalHours")
    totalDays = models.FloatField(default=0, verbose_name="TotalDays")
    totalPrice = models.FloatField(default=0, verbose_name="TotalPrice")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "capacity": self.capacity,
            "entrancePrice": self.entrancePrice,
            "priceForEachHour": self.priceForEachHour,
            "priceForEachDay": self.priceForEachDay,
            "isDaily": self.isDaily,
            "availableSpace": self.availableSpace,

        }

    def __str__(self):
        return self.name
