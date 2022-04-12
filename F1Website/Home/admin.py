from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Race_History, Driver_Standing, Driver, Circuit, Constructor, Constructor_Standing

# ------------------------------ CSV UPLOAD ------------------------------
# I don't know a better method, so for now we do this one by one per model
# FUTURE NOTE: make this easier


class UploadCSVForm(forms.Form):
    upload_csv = forms.FileField()

class RaceHistoryAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self,request):

        # Check we are uploading a csv
        if request.method == "POST":
            csv_file = request.FILES['upload_csv']

            if not csv_file.name.endswith('.csv'):
                message.warning(request, 'Invalid file type')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for _ in csv_data:
                fields = _.split(",")
                created = Race_History.objects.update_or_create(
                    season = fields[0],
                    round = fields[1],
                    circuit_id = fields[2],
                    status = fields[3],
                    position = fields[4],
                    points = fields[5],
                    driver_id = fields[6],
                    team_id = fields[7],
                    date = fields[8],
                    true_time = fields[9]
                )

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = UploadCSVForm()
        data = {"form": form}

        return render(request, "admin/upload_csv.html", data)

class DriverStandingAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self,request):

        # Check we are uploading a csv
        if request.method == "POST":
            csv_file = request.FILES['upload_csv']

            if not csv_file.name.endswith('.csv'):
                message.warning(request, 'Invalid file type')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for _ in csv_data:
                fields = _.split(",")
                created = Driver_Standing.objects.update_or_create(
                    season = fields[0],
                    round = fields[1],
                    position = fields[2],
                    driver_id = fields[3],
                    team_id = fields[4],
                    points = fields[5],
                    wins = fields[6]
                )

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = UploadCSVForm()
        data = {"form": form}

        return render(request, "admin/upload_csv.html", data)

class DriverAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self,request):

        # Check we are uploading a csv
        if request.method == "POST":
            csv_file = request.FILES['upload_csv']

            if not csv_file.name.endswith('.csv'):
                message.warning(request, 'Invalid file type')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for _ in csv_data:
                fields = _.split(",")
                created = Driver.objects.update_or_create(
                    driver_id = fields[0],
                    permanentNumber = fields[1],
                    givenName = fields[2],
                    familyName = fields[3],
                    dateOfBirth = fields[4],
                    nationality = fields[5]
                )

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = UploadCSVForm()
        data = {"form": form}

        return render(request, "admin/upload_csv.html", data)

class ConstructorStandingAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self,request):

        # Check we are uploading a csv
        if request.method == "POST":
            csv_file = request.FILES['upload_csv']

            if not csv_file.name.endswith('.csv'):
                message.warning(request, 'Invalid file type')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for _ in csv_data:
                fields = _.split(",")
                created = Constructor_Standing.objects.update_or_create(
                    season = fields[0],
                    team_id = fields[1],
                    position = fields[2],
                    points = fields[3],
                    wins = fields[4]
                )

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = UploadCSVForm()
        data = {"form": form}

        return render(request, "admin/upload_csv.html", data)

class ConstructorAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self,request):

        # Check we are uploading a csv
        if request.method == "POST":
            csv_file = request.FILES['upload_csv']

            if not csv_file.name.endswith('.csv'):
                message.warning(request, 'Invalid file type')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for _ in csv_data:
                fields = _.split(",")
                created = Constructor.objects.update_or_create(
                    team_id = fields[0],
                    team_name = fields[1],
                    nationality = fields[2]
                )

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = UploadCSVForm()
        data = {"form": form}

        return render(request, "admin/upload_csv.html", data)

class CircuitAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self,request):

        # Check we are uploading a csv
        if request.method == "POST":
            csv_file = request.FILES['upload_csv']

            if not csv_file.name.endswith('.csv'):
                message.warning(request, 'Invalid file type')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for _ in csv_data:
                fields = _.split(",")
                created = Circuit.objects.update_or_create(
                    circuit_id = fields[0],
                    circuit_name = fields[1],
                    location = fields[2],
                    country = fields[3],
                )

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = UploadCSVForm()
        data = {"form": form}

        return render(request, "admin/upload_csv.html", data)


admin.site.register(Race_History, RaceHistoryAdmin)
admin.site.register(Driver_Standing, DriverStandingAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Constructor_Standing, ConstructorStandingAdmin)
admin.site.register(Constructor, ConstructorAdmin)
admin.site.register(Circuit, CircuitAdmin)