from django.shortcuts import render,redirect
from django.contrib import messages
# Create your views here.
from bank.models import bankreg, sharekey_request, encrypted_kycdata, pkey_request
from customer.models import customerreg, upload_kyc, upload_kycdet
from secure_kyc_blockchain.settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
def customer_index(request):

    return render(request,'customer/customer_index.html')

def customer_register(request):
    if request.method == "POST":
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        location = request.POST.get('location')
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        if customerreg.objects.filter(uname=uname):
            messages.success(request, 'Username Already Exists')
        else:
            customerreg.objects.create(name=name, email=email, mobile=mobile,
                                   location=location, uname=uname, password=password)
        return redirect('customer_login')
    return render(request,'customer/customer_register.html')


def customer_login(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pswd = request.POST.get('password')
        try:
            check = customerreg.objects.get(uname=uname, password=pswd)
            print(check)
            request.session['customerid'] = check.id
            request.session['customername'] = check.uname
            return redirect('customer_home1')
        except:
            pass
        return redirect('customer_login')
    return render(request,'customer/customer_login.html')

def customer_home1(request):
    cid = request.session['customerid']
    cname = request.session['customername']
    if upload_kyc.objects.filter(cid=cid):
        return redirect('share_hash')
    else:
        return redirect('customer_home')
    return render(request,'customer/customer_home1.html')

def customer_home(request):
    bankdetails=bankreg.objects.all()
    status="pending"
    cid=request.session['customerid']
    cname=request.session['customername']
    if request.method == "POST" and request.FILES['aadhar'] and request.FILES['voter_id'] and request.FILES['pan_card']:
        fullname = request.POST.get('fullname')
        bankname = request.POST.get('bankname')
        banklocation = request.POST.get('banklocation')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        location = request.POST.get('location')
        aadhar = request.FILES['aadhar']
        voter_id = request.FILES['voter_id']
        pan_card = request.FILES['pan_card']
        if upload_kyc.objects.filter(cid=cid,cname=cname,bankname=bankname):
            messages.success(request, 'Already Have a Account in this bank')
        else:
            upload_kyc.objects.create(cid=cid,cname=cname,fullname=fullname,email=email,mobile=mobile,
                                  gender=gender,address=address,location=location,bankname=bankname,
                                  banklocation=banklocation)
            upload_kycdet.objects.create(cid=cid, cname=cname, aadhar=aadhar,
                                  voter_id=voter_id, pan_card=pan_card, status=status, bankname=bankname,
                                  banklocation=banklocation)

    return render(request,'customer/customer_home.html',{'bankdetails':bankdetails})


def share_hash(request):
    bankdetails = bankreg.objects.all()
    status = "pending"
    cid = request.session['customerid']
    cname = request.session['customername']
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        bankname = request.POST.get('bankname')
        banklocation = request.POST.get('banklocation')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        location = request.POST.get('location')

        if upload_kyc.objects.filter(cid=cid, cname=cname, bankname=bankname):
            messages.success(request, 'Already Have a Account in this bank')
        else:
            upload_kyc.objects.create(cid=cid, cname=cname, fullname=fullname, email=email, mobile=mobile,
                                      gender=gender, address=address, location=location, bankname=bankname,
                                      banklocation=banklocation)

    return render(request,'customer/share_hash.html',{'bankdetails':bankdetails})


def viewbank_request(request):
    cid=request.session['customerid']
    requestdetails = sharekey_request.objects.filter(cid=cid)


    return render(request,'customer/viewbank_request.html',{'requestdetails':requestdetails})


def customer_share1(request,pk):
    uniquedet=sharekey_request.objects.get(id=pk)
    unid=uniquedet.id
    bemail=uniquedet.bemail
    cid=uniquedet.cid
    hashvalue1=encrypted_kycdata.objects.filter(cid=cid)
    for aa in hashvalue1:
        hash1=aa.newhash1
    print(hash1)
    status1="send"

    subject = "Hash Value"
    text_content = ""

    cont1 = "Hash Value:"
    html_content = "<br/><p>Hash Value:<strong>" + str(
        hash1) + "</strong></p>"
    from_mail = DEFAULT_FROM_EMAIL
    to_mail = [bemail]
    # if send_mail(subject,message,from_mail,to_mail):
    msg = EmailMultiAlternatives(subject, text_content, from_mail, to_mail)
    msg.attach_alternative(html_content, "text/html")
    if msg.send():
        sharekey_request.objects.filter(id=unid).update(hashvalue=hash1,status=status1)

    return render(request,'customer/customer_share1.html')

def viewpkey_request(request):
    cid=request.session['customerid']
    requestdetails = pkey_request.objects.filter(cid=cid)


    return render(request,'customer/viewpkey_request.html',{'requestdetails':requestdetails})


def customer_share2(request,pk):
    uniquedet=sharekey_request.objects.get(id=pk)
    unid=uniquedet.id
    bemail=uniquedet.bemail
    cid=uniquedet.cid
    otp1 = User.objects.make_random_password(length=5, allowed_chars="01234567889")
    status1="send"

    subject = "Private Key"
    text_content = ""

    cont1 = "Hash Value:"
    html_content = "<br/><p>Private Key:<strong>" + str(
        otp1) + "</strong></p>"
    from_mail = DEFAULT_FROM_EMAIL
    to_mail = [bemail]
    # if send_mail(subject,message,from_mail,to_mail):
    msg = EmailMultiAlternatives(subject, text_content, from_mail, to_mail)
    msg.attach_alternative(html_content, "text/html")
    if msg.send():
        pkey_request.objects.filter(id=unid).update(pkey1=otp1,status=status1)

    return render(request,'customer/customer_share2.html')