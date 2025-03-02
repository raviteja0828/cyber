from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=50)
    user_email = models.EmailField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_phone = models.CharField(max_length=50)
    user_location = models.CharField(max_length=50,default='Unknown')
    user_profile = models.ImageField(upload_to='images/user')
    status = models.CharField(max_length=15,default='Pending')
    otp = models.CharField(max_length=6,default=0) 
  
  

    class Meta:
        db_table = 'User_details'



class UserFeedbackModels(models.Model):
    feed_id = models.AutoField(primary_key=True)
    star_feedback = models.TextField(max_length=900)
    star_rating = models.IntegerField()
    star_Date = models.DateTimeField(auto_now_add=True, null=True)
    user_details = models.ForeignKey(User, on_delete=models.CASCADE)
    sentment = models.TextField(max_length=20,null=True)
    class Meta:
        db_table = 'feedback_table'


from django.db import models

class CyberSecurityPrediction(models.Model):
    # Input values
    diff_srv_rate = models.FloatField()
    dst_host_srv_diff_host_rate = models.FloatField()
    dst_host_same_src_port_rate = models.FloatField()
    srv_count = models.FloatField()
    protocol_type = models.CharField(max_length=10)
    dst_host_count = models.FloatField()
    logged_in = models.CharField(max_length=10)
    dst_bytes = models.FloatField()
    count = models.FloatField()

    # Prediction result
    prediction_result = models.CharField(max_length=50)

    # Intimations content
    intimations_content = models.TextField()

    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction: {self.prediction_result} at {self.timestamp}"

