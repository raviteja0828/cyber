from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
import random
from django.contrib.auth import logout
import pickle
import os
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect


# Create your views here.

import urllib.request
import urllib.parse


def index(request):
    return render(request,'user/index.html')



def about(request):
    return render(request,'user/about.html')



def admin_login(request):
    if request.method == "POST":
        # Get username and password from the form
        username = request.POST.get('name')
        password = request.POST.get('password')
        
        # Authenticate user using Django's built-in authentication system
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:  # Check if the user exists and is a superuser
            login(request, user)  # Log in the user
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard')  # Redirect to the admin dashboard
        else:
            messages.error(request, 'Invalid details or you are not a superuser!')
            return redirect('admin_login')  # Redirect back to login if credentials are incorrect

    return render(request, 'user/admin-login.html') 



def contact(request):
    return render(request,'user/contact.html')




def otp(request):
    user_id = request.session.get('user_id')  # Retrieve the user session ID
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Invalid user')
        return redirect('user_register')

    # Preprocess email for masking
    email = user.user_email  # Ensure the `user_email` field exists in the User model
    if email:
        username, domain = email.split('@', 1)  # Split username and domain
        
        # Mask email as per requirement: first letter, '****', last 3 letters before '@', and domain
        if len(username) > 3:
            masked_email = f"{username[:1]}****{username[-3:]}@{domain}"
        else:
            # If the username is less than 4 characters, just mask as much as possible
            masked_email = f"{username[:1]}{'*' * (len(username) - 1)}@{domain}"
    else:
        masked_email = "Email not available"

    if request.method == "POST":
        otp_entered = request.POST.get('otp')  # Get OTP entered by the user
        if str(user.otp) == otp_entered:
            messages.success(request, 'OTP verification and Registration successfully completed!')
            user.status = "Verified"
            user.save()  # Save the updated user instance
            return redirect('user_login')
        else:
            messages.error(request, 'Invalid OTP entered')
            return redirect('otp')

    # Pass preprocessed email to the template
    return render(request, 'user/otp.html', {'user': user, 'masked_email': masked_email})








def services(request):
    return render(request,'user/service.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(user_email=email)   
            if user.user_password == password:
                request.session['user_id'] = user.user_id
                if user.status == 'Accepted':
                    messages.success(request, 'Login Successful')
                    return redirect('user_dashboard')
                elif user.status == 'Pending':
                    messages.info(request, 'Otp verification is compalsary otp is sent to ' + str(user.user_email))
                    return redirect('otp')
                else:
                    messages.error(request, 'Your account is not approved yet.')
                    return redirect('user_login')
            else:
                messages.error(request, 'Invalid Login Details')
                return redirect('user_login')
        except User.DoesNotExist:
            messages.error(request, 'Invalid Login Details')
            return redirect('user_login')
    return render(request,'user/user-login.html')

from .models import CyberSecurityPrediction

def user_dashboard(request):

    predictions = CyberSecurityPrediction.objects.all()


    return render(request,'user/user-dashboard.html', {'predictions': predictions})


def user_profile(request):
    user_id  = request.session['user_id']
    user = User.objects.get(pk= user_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            profile = request.FILES['profile']
            user.user_profile = profile
        except MultiValueDictKeyError:
            profile = user.user_profile
        password = request.POST.get('password')
        location = request.POST.get('location')
        user.user_name = name
        user.user_email = email
        user.user_phone = phone
        user.user_password = password
        user.user_location = location
        user.save()
        messages.success(request , 'updated succesfully!')
        return redirect('user_profile')
    return render(request,'user/user-profile.html',{'user':user})





def generate_otp(length=4):
    otp = ''.join(random.choices('0123456789', k=length))
    return otp




def user_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        location = request.POST.get('address')
        profile = request.FILES.get('profile')
        try:
            User.objects.get(user_email =   email)
            messages.info(request, 'Email Already Exists!')
            return redirect('user_register')
        except:
            otp = generate_otp()
            user = User.objects.create(user_name=name, user_email=email, user_phone=phone, user_profile=profile, user_password=password, user_location=location,otp=otp)
            print(user)
            user_id_new = request.session['user_id'] = user.user_id
            print(user_id_new)
            mail_message = f"Registration Successfully\n Your 4 digit Pin is below\n {otp}"
            send_mail("User Password", mail_message, settings.EMAIL_HOST_USER, [email])
            messages.success(request, "Your account was created..")
            return redirect('otp')
    return render(request,'user/user-register.html')





def user_logout(request):
    logout(request)
    return redirect('user_login')


from django.shortcuts import render, redirect
from django.utils.timezone import now
import os
import pickle
from .models import CyberSecurityPrediction
from django.shortcuts import render, redirect
from django.utils.timezone import now
import os
import pickle
from .models import CyberSecurityPrediction

def cyber_sec(request):
    if request.method == 'POST':
        # Collecting form data
        diff_srv_rate = float(request.POST['diff_srv_rate'])
        dst_host_srv_diff_host_rate = float(request.POST['dst_host_srv_diff_host_rate'])
        dst_host_same_src_port_rate = float(request.POST['dst_host_same_src_port_rate'])
        srv_count = float(request.POST['srv_count'])
        protocol_type = str(request.POST['protocol_type'])
        dst_host_count = float(request.POST['dst_host_count'])
        logged_in = str(request.POST['logged_in'])
        dst_bytes = float(request.POST['dst_bytes'])
        count = float(request.POST['count'])

        # Converting protocol_type to integer
        protocol_type_to_int = {'tcp': 0, 'udp': 1, 'icmp': 2}
        protocol_type_int = protocol_type_to_int.get(protocol_type.lower(), 0)

        # Loading the ML model
        model_path = os.path.join(os.path.dirname(__file__), 'rfc.pkl')
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        # Preparing input data for prediction
        input_data = [[diff_srv_rate, dst_host_srv_diff_host_rate, dst_host_same_src_port_rate, 
                       srv_count, protocol_type_int, dst_host_count, logged_in == 'yes', 
                       dst_bytes, count]]

        # Making the prediction
        prediction_result = model.predict(input_data)[0]

        # Define intimations based on prediction result
        intimations_mapping = {
            'dos': "Steps to Secure:\n1. Disconnect from the internet\n2. Contact your ISP\n3. Install and configure a firewall\n4. Update all software\n5. Implement rate limiting.",
            'normal': "Maintain Security:\n1. Keep all systems updated\n2. Use strong passwords\n3. Enable two-factor authentication\n4. Regularly back up your data.",
            'probe': "Steps to Secure:\n1. Review firewall rules\n2. Disable unnecessary services\n3. Implement intrusion detection systems (IDS)\n4. Regularly scan for vulnerabilities.",
            'r2l': "Steps to Secure:\n1. Change all passwords immediately\n2. Enable strict access controls\n3. Use strong encryption for remote access.",
            'u2r': "Steps to Secure:\n1. Isolate affected systems\n2. Revoke user credentials\n3. Apply security patches\n4. Implement least privilege."
        }
        
        intimations_content = intimations_mapping.get(prediction_result, "No specific steps available.")

        # Store prediction details in the database
        prediction_entry = CyberSecurityPrediction.objects.create(
            diff_srv_rate=diff_srv_rate,
            dst_host_srv_diff_host_rate=dst_host_srv_diff_host_rate,
            dst_host_same_src_port_rate=dst_host_same_src_port_rate,
            srv_count=srv_count,
            protocol_type=protocol_type,
            dst_host_count=dst_host_count,
            logged_in=logged_in,
            dst_bytes=dst_bytes,
            count=count,
            prediction_result=prediction_result,
            intimations_content=intimations_content,
            timestamp=now()
        )

        # Redirect to result page with prediction details (pass ID)
        return redirect('cyber_sec_result', prediction_id=prediction_entry.id)

    return render(request, 'user/cyber-security.html')


def cyber_sec_result(request, prediction_id):
    # Fetch prediction details from database
    prediction_entry = CyberSecurityPrediction.objects.get(id=prediction_id)
    
    return render(request, 'user/cyber-security-result.html', {'prediction_entry': prediction_entry})





from userapp.models import UserFeedbackModels

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def feedback(request):
    views_id = request.session['user_id']
    user = User.objects.get(user_id=views_id)
    if request.method == 'POST':
        u_feedback = request.POST.get('review')
        u_rating = request.POST.get('rating')

        if not u_feedback:
            return redirect('')  # Specify the appropriate redirect target

        # Sentiment analysis
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(u_feedback)
        sentiment = None
        if score['compound'] > 0 and score['compound'] <= 0.5:
            sentiment = 'positive'
        elif score['compound'] > 0.5:
            sentiment = 'very positive'
        elif score['compound'] < -0.5:
            sentiment = 'very negative'
        elif score['compound'] < 0 and score['compound'] >= -0.5:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        print(sentiment)
        user.star_feedback = u_feedback
        user.star_rating = u_rating
        user.save()

        UserFeedbackModels.objects.create(
            user_details=user,
            star_feedback=u_feedback,
            star_rating=u_rating,
            sentment=sentiment
        )
        
        # Send feedback to user's email
        mail_message = f"Thank you for your feedback!\n\nYour review: {u_feedback}\nYour rating: {u_rating}\nSentiment: {sentiment}"
        send_mail(
            "Thank you for your feedback",
            mail_message,
            settings.EMAIL_HOST_USER,
            [user.user_email]
        )

        rev = UserFeedbackModels.objects.filter()
        messages.success(request,'Feedback sent successfully')

    return render(request, "user/feedback.html")

