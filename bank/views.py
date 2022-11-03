from django.shortcuts import render,redirect

# Create your views here.
from bank.models import bankreg, encrypted_kycdata, sharekey_request, pkey_request
from customer.models import upload_kyc, upload_kycdet
import hashlib
import datetime
import json
from django.core.files.storage import FileSystemStorage
from fpdf import FPDF
import os
import PyPDF2
from six import b
from cryptography.fernet import Fernet
class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(nonce = 1, previous_hash = '0')

    def create_block(self, nonce, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

def bank_login(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pswd = request.POST.get('password')
        try:
            check = bankreg.objects.get(uname=uname, password=pswd)
            print(check)
            request.session['bankid'] = check.id
            request.session['buname'] = check.uname
            request.session['bankname'] = check.bankname
            request.session['bankemail'] = check.email
            return redirect('bank_home')
        except:
            pass
        return redirect('bank_login')
    return render(request,'bank/bank_login.html')


def bank_register(request):
    if request.method == "POST":
        name = request.POST.get('bank_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        location = request.POST.get('location')
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        bankreg.objects.create(bankname=name, email=email, mobile=mobile,
                                   location=location, uname=uname, password=password)
        return redirect('bank_login')
    return render(request,'bank/bank_register.html')


def bank_home(request):
    bankid=request.session['bankid']
    buname=request.session['buname']

    bankname = request.session['bankname']

    bankdetails = upload_kyc.objects.filter(bankname=bankname)
    print(bankdetails)
    return render(request,'bank/bank_home.html',{'bankdetails':bankdetails})


def verify_kyc(request,pk):
    uniquerow = upload_kycdet.objects.get(id=pk)
    unid = uniquerow.id
    cid = uniquerow.cid
    cname = uniquerow.cname
    bname = uniquerow.bankname

    aadhar1 = uniquerow.aadhar
    pan1 = uniquerow.pan_card
    voter1 = uniquerow.voter_id

    fs = FileSystemStorage()
    filename1 = fs.save(aadhar1.name, aadhar1)
    print(filename1)
    filename2 = fs.save(voter1.name, voter1)
    print(filename2)
    filename3 = fs.save(pan1.name, pan1)
    uploaded_file_url1 = fs.url(filename1)
    print(uploaded_file_url1)
    uploaded_file_url2 = fs.url(filename2)
    print(uploaded_file_url2)
    uploaded_file_url3 = fs.url(filename3)
    print(uploaded_file_url3)
    ROOT_DIR1 = os.path.dirname(os.path.abspath(filename1))
    print(ROOT_DIR1)
    ROOT_DIR2 = os.path.dirname(os.path.abspath(filename2))
    print(ROOT_DIR2)
    ROOT_DIR3 = os.path.dirname(os.path.abspath(filename3))
    print(ROOT_DIR3)
    mainpath1 = ROOT_DIR1 + "/" + "assests" + uploaded_file_url1
    print(mainpath1)
    mainpath2 = ROOT_DIR2 + "/" + "assests" + uploaded_file_url2
    print(mainpath2)
    mainpath3 = ROOT_DIR3 + "/" + "assests" + uploaded_file_url3
    print(mainpath3)

    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(mainpath1, 'rb') as file:
        original = file.read()
        print(original)
    pdfFileObj = open(mainpath1, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # printing number of pages in pdf file
    print(pdfReader.numPages)

    # creating a page object
    pageObj = pdfReader.getPage(0)

    # extracting text from page
    aa = pageObj.extractText()
    print(aa)

    # closing the pdf file object
    pdfFileObj.close()


    # key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(mainpath2, 'rb') as file1:
        original1 = file1.read()
        print(original1)
    pdfFileObj1 = open(mainpath2, 'rb')

    # creating a pdf reader object
    pdfReader1 = PyPDF2.PdfFileReader(pdfFileObj1)

    # printing number of pages in pdf file
    print(pdfReader1.numPages)

    # creating a page object
    pageObj1 = pdfReader1.getPage(0)

    # extracting text from page
    atext = pageObj1.extractText()
    print(atext)

    # closing the pdf file object
    pdfFileObj1.close()

    # key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(mainpath3, 'rb') as file2:
        original3 = file2.read()
        print(original3)
    pdfFileObj2 = open(mainpath3, 'rb')

    # creating a pdf reader object
    pdfReader2 = PyPDF2.PdfFileReader(pdfFileObj2)

    # printing number of pages in pdf file
    print(pdfReader2.numPages)

    # creating a page object
    pageObj3 = pdfReader2.getPage(0)

    # extracting text from page
    atext1 = pageObj3.extractText()
    print(atext1)

    # closing the pdf file object
    pdfFileObj2.close()

    # encrypting the file1
    encrypted = fernet.encrypt(b(aa))
    print(encrypted)
    encryptpath = ROOT_DIR1 + "/assests/media/encrypt/" + filename1
    print(encryptpath)
    with open(encryptpath, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
        pdf = FPDF()

        # Add a page
        pdf.add_page()

        # set style and size of font
        # that you want in the pdf
        pdf.set_font("Arial", size=15)

        # create a cell

        # add another cell
        pdf.cell(200, 10, txt=str(encrypted), ln=2, align='C')

        # save the pdf with name .pdf
        pdf.output(encryptpath)

    # encrypting the file2
    encrypted1 = fernet.encrypt(b(atext))
    print(encrypted1)
    encryptpath1 = ROOT_DIR2 + "/assests/media/encrypt/" + filename2
    print(encryptpath1)
    with open(encryptpath1, 'wb') as encrypted_file:
        encrypted_file.write(encrypted1)
        pdf1 = FPDF()

        # Add a page
        pdf1.add_page()

        # set style and size of font
        # that you want in the pdf
        pdf1.set_font("Arial", size=15)

        # create a cell

        # add another cell
        pdf1.cell(200, 10, txt=str(encrypted1), ln=2, align='C')

        # save the pdf with name .pdf
        pdf1.output(encryptpath1)

    # encrypting the file3
    encrypted2 = fernet.encrypt(b(atext1))
    print(encrypted2)
    encryptpath2 = ROOT_DIR3 + "/assests/media/encrypt/" + filename2
    print(encryptpath2)
    with open(encryptpath2, 'wb') as encrypted_file:
        encrypted_file.write(encrypted2)
        pdf2 = FPDF()

        # Add a page
        pdf2.add_page()

        # set style and size of font
        # that you want in the pdf
        pdf2.set_font("Arial", size=15)

        # create a cell

        # add another cell
        pdf2.cell(200, 10, txt=str(encrypted2), ln=2, align='C')

        # save the pdf with name .pdf
        pdf2.output(encryptpath2)

    blockchain = Blockchain()
    previous_block1 = blockchain.get_previous_block()
    previous_nonce1 = previous_block1['nonce']
    print(previous_nonce1)
    nonce1 = blockchain.proof_of_work(previous_nonce1)
    previous_hash1 = blockchain.hash(previous_block1)
    block1 = blockchain.create_block(nonce1, previous_hash1)
    atimestamp = str(datetime.datetime.now())
    apphash = encrypted_kycdata.objects.all().count()
    print(apphash)
    if apphash == 0:
        encrypted_kycdata.objects.create(unid=unid, cid=cid, cname=cname,
                                           aadharorignal_data=aa, aadharencrypted_data=encrypted,voterencrypted_data=encrypted1,
                                         panencrypted_data=encrypted2,
                                           bankname=bname, phash1=apphash, newhash1=previous_hash1,
                                           atimestamp=atimestamp)
        return redirect("encryption_success")
    else:
        ahash22 = encrypted_kycdata.objects.all().last()
        aphash = ahash22.newhash1
        encrypted_kycdata.objects.create(unid=unid, cid=cid, cname=cname, aadharorignal_data=aa, aadharencrypted_data=encrypted,voterencrypted_data=encrypted1,
                                         panencrypted_data=encrypted2,
                                           bankname=bname, phash1=aphash, newhash1=previous_hash1,
                                           atimestamp=atimestamp)
        return redirect("encryption_success")
    return render(request,'bank/verify_kyc.html')

def encryption_success(request):

    return render(request,'bank/encryption_success.html')

def view_kyc(request,pk):
    bankid = request.session['bankid']
    buname = request.session['buname']

    bankname = request.session['bankname']
    uniquerow1 = upload_kyc.objects.get(id=pk)
    cid=uniquerow1.cid
    request.session['cid']=cid
    cname1=uniquerow1.cname
    request.session['cname1'] = cname1
    if upload_kycdet.objects.filter(bankname=bankname,cid=cid):
        kycdetails = upload_kycdet.objects.filter(bankname=bankname)
        print(kycdetails)
    else:
        return redirect('share_request')
    return render(request,'bank/view_kyc.html',{'kycdetails':kycdetails})


def share_request(request):
    bankid = request.session['bankid']
    buname = request.session['buname']

    bankname = request.session['bankname']

    return render(request,'bank/share_request.html')


def share_request(request):
    bankid = request.session['bankid']
    buname = request.session['buname']

    bankname = request.session['bankname']
    cname1=request.session['cname1']
    cid1=request.session['cid']
    if request.method == "POST":
        hash_value = request.POST.get('hash_value')
        if sharekey_request.objects.filter(bankname=bankname,hashvalue=hash_value):
            return redirect('viewencrypted_kyc')
        else:
            return redirect('unsuccesskys')
    return render(request,'bank/share_request.html')

def share_request1(request):
    bankid = request.session['bankid']
    buname = request.session['buname']
    status1="pending"
    bankname = request.session['bankname']
    cname1=request.session['cname1']
    cid1=request.session['cid']
    email1=request.session['bankemail']
    sharekey_request.objects.create(cid=cid1,cname=cname1,bankid=bankid,bankname=bankname,
                                    buname=buname,bemail=email1,
                                    hashvalue=status1,status=status1)
    return render(request,'bank/share_request1.html')

def share_request1(request):
    bankid = request.session['bankid']
    buname = request.session['buname']
    status1="pending"
    bankname = request.session['bankname']
    cname1=request.session['cname1']
    cid1=request.session['cid']
    email1=request.session['bankemail']
    sharekey_request.objects.create(cid=cid1,cname=cname1,bankid=bankid,bankname=bankname,
                                    buname=buname,bemail=email1,
                                    hashvalue=status1,status=status1)
    return render(request,'bank/share_request1.html')

def viewencrypted_kyc(request):
    cid1 = request.session['cid']
    enc_details=encrypted_kycdata.objects.filter(cid=cid1)
    return render(request,'bank/viewencrypted_kyc.html',{'enc_details':enc_details})


def unsuccesskys(request):

    return render(request, 'bank/unsuccesskys.html')


def decrypt_file(request,pk):
    bankid = request.session['bankid']
    buname = request.session['buname']

    bankname = request.session['bankname']
    uniquerow1 = encrypted_kycdata.objects.get(id=pk)
    cid11=uniquerow1.cid
    request.session['cid11']=cid11
    cname11=uniquerow1.cname
    request.session['cname11'] = cname11
    if request.method == "POST":
        private_key = request.POST.get('private_key')
        if pkey_request.objects.filter(bankname=bankname,pkey1=private_key):
            return redirect('decrypted_kyc')
        else:
            return redirect('unsuccesskyc1')

    email1 = request.session['bankemail']

    return render(request,'bank/decrypt_file.html')

def decrypt_request1(request):
    bankid = request.session['bankid']
    buname = request.session['buname']
    status1 = "pending"
    bankname = request.session['bankname']
    cname111 = request.session['cname11']
    cid111 = request.session['cid11']
    email1 = request.session['bankemail']
    pkey_request.objects.create(cid=cid111, cname=cname111, bankid=bankid, bankname=bankname,
                                    buname=buname, bemail=email1,
                                    pkey1=status1, status=status1)
    return render(request,'bank/decrypt_request1.html')



def decrypted_kyc(request):
    cid111 = request.session['cid11']
    dec_details=upload_kycdet.objects.filter(cid=cid111)
    return render(request,'bank/decrypted_kyc.html',{'dec_details':dec_details})


def unsuccesskyc1(request):

    return render(request, 'bank/unsuccesskyc1.html')