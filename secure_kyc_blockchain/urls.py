"""secure_kyc_blockchain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from customer import views as customerviews
from bank import views as bankviews
from django.conf.urls.static import static
from secure_kyc_blockchain import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', customerviews.customer_index, name="customer_index"),
    url(r'^customer_login/$',customerviews.customer_login, name="customer_login"),
    url(r'^customer_register/$',customerviews.customer_register, name="customer_register"),
    url(r'^customer_home/$',customerviews.customer_home, name="customer_home"),
    url(r'^customer_home1/$',customerviews.customer_home1, name="customer_home1"),
    url(r'^share_hash/$',customerviews.share_hash, name="share_hash"),
    url(r'^viewbank_request/$',customerviews.viewbank_request, name="viewbank_request"),
    url(r'^customer_share1/(?P<pk>\d+)/$',customerviews.customer_share1,name="customer_share1"),
    url(r'^viewpkey_request/$',customerviews.viewpkey_request, name="viewpkey_request"),
    url(r'^customer_share2/(?P<pk>\d+)/$',customerviews.customer_share2,name="customer_share2"),

    url(r'^bank_login/$',bankviews.bank_login, name="bank_login"),
    url(r'^bank_register/$',bankviews.bank_register, name="bank_register"),
    url(r'^bank_home/$',bankviews.bank_home, name="bank_home"),

    url(r'^verify_kyc/(?P<pk>\d+)/$',bankviews.verify_kyc,name="verify_kyc"),
    url(r'^view_kyc/(?P<pk>\d+)/$',bankviews.view_kyc,name="view_kyc"),
    url(r'^encryption_success/$',bankviews.encryption_success,name="encryption_success"),
    url(r'^share_request/$',bankviews.share_request,name="share_request"),
    url(r'^share_request1/$',bankviews.share_request1,name="share_request1"),
    url(r'^viewencrypted_kyc/$',bankviews.viewencrypted_kyc,name="viewencrypted_kyc"),
    url(r'^unsuccesskys/$',bankviews.unsuccesskys,name="unsuccesskys"),
    url(r'^decrypt_file/(?P<pk>\d+)/$', bankviews.decrypt_file, name="decrypt_file"),
    url(r'^decrypt_request1/$',bankviews.decrypt_request1,name="decrypt_request1"),

    url(r'^decrypted_kyc/$',bankviews.decrypted_kyc,name="decrypted_kyc"),
    url(r'^unsuccesskyc1/$',bankviews.unsuccesskyc1,name="unsuccesskyc1"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

