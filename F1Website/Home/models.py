from django.db import models

# Create your models here.
class Race_History(models.Model):
    # season,round,circuit_id,status,position,points,driver_id,team_id,date,true_time
    season = models.IntegerField()
    round = models.IntegerField()
    circuit_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    position = models.IntegerField()
    points = models.FloatField()
    driver_id = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    date = models.DateField()
    true_time = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.season} - {self.round} - {self.circuit_id} - {self.driver_id}'

class Driver_Standing(models.Model):
    # season, round, position, driverID, constructorId, points, wins
    season = models.IntegerField()
    round = models.IntegerField()
    position = models.IntegerField()
    driver_id = models.CharField(max_length=100)
    team_id = models.CharField(max_length=100)
    points = models.FloatField()
    wins = models.IntegerField()

    def __str__(self):
        return f'{self.season} - {self.round} - {self.position} - {self.driver_id}'

class Driver(models.Model):
    # driverId,permanentNumber,givenName,familyName,dateOfBirth,nationality
    driver_id = models.CharField(max_length=100)
    permanentNumber = models.IntegerField()
    givenName = models.CharField(max_length=100)
    familyName = models.CharField(max_length=100)
    dateOfBirth = models.DateField()
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.driver_id} - {self.permanentNumber} - {self.nationality}'

class Constructor(models.Model):
    # driverId,permanentNumber,givenName,familyName,dateOfBirth,nationality
    team_id = models.CharField(max_length=100)
    team_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.team_id} - {self.team_name} - {self.nationality}'

class Constructor_Standing(models.Model):
    # driverId,permanentNumber,givenName,familyName,dateOfBirth,nationality
    season = models.IntegerField()
    team_id = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    points = models.FloatField()
    wins = models.IntegerField()

    def __str__(self):
        return f'{self.season} - {self.team_id} - {self.position} - {self.points} - {self.wins}'

class Circuit(models.Model):
    # circuit_id,circuit_name,location,country
    circuit_id = models.CharField(max_length=100)
    circuit_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.circuit_name} - {self.location} - {self.country}'