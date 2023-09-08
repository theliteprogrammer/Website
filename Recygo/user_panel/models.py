# from django.db import models

# from django.db import models

# class User(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     address = models.CharField(max_length=200)
#     phone_number = models.CharField(max_length=20)
#     # Add other user-related fields

# class RecyclingType(models.Model):
#     name = models.CharField(max_length=50)

# class Transaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     recycling_type = models.ForeignKey(RecyclingType, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50)  # e.g., "Pending", "Completed"
#     # Add fields for transaction status, payment method, etc.

# class Employee(models.Model):
#     name = models.CharField(max_length=100)
#     ROLES = (
#         ('Collector', 'Collector'),
#         ('Sorter', 'Sorter'),
#         ('Driver', 'Driver'),
#     )
#     role = models.CharField(max_length=50, choices=ROLES)
#     on_duty = models.BooleanField(default=False)

# class WasteItem(models.Model):
#     name = models.CharField(max_length=50)
#     weight = models.DecimalField(max_digits=10, decimal_places=2)
#     type = models.CharField(max_length=50)  # e.g., "Plastic", "Glass"
#     # Add fields for waste item properties, source, etc.

# class Client(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     location = models.CharField(max_length=200)
#     subscription_status = models.BooleanField(default=True)
#     # Add fields for subscription plan, contact information, etc.

# class Revenue(models.Model):
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)

# # You can add additional models for graphs and statistics data if necessary

