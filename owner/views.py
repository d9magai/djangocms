from __future__ import absolute_import

import base64
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic.list import ListView
import hashlib
import hmac
import json

from .forms import LoginForm, BookForm, ImpressionForm
from .models import Book, Impression


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('owner:mypage')
    template_name = 'owner/login.html'

    def get_success_url(self):
        # here method should be GET or POST.
        next_url = self.request.POST.get('next', None)
        if next_url:
            # you can include some query strings as well
            return "%s" % (next_url)
        else:
            return reverse('owner:mypage')  # what url you wish to return

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        next_url = self.request.GET.get('next', None)
        n = self.request.GET.get('next', '/')

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


def index(request):
    return render(request, 'owner/index.html')


@login_required(login_url='/owner/login/')
def mypage(request):
    return render(request, 'owner/mypage.html')


@login_required(login_url='/owner/login/')
def redirect(request):
    return render(request, 'owner/redirect.html')


@method_decorator(login_required(login_url='owner:login'), name='dispatch')
class BookList(ListView):
    context_object_name = 'books'
    template_name = 'owner/book_list.html'
    paginate_by = 2  # １ページは最大2件ずつでページングする
    login_url = 'owner:login'

    def dispatch(self, *args, **kwargs):
        return super(BookList, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        books = Book.objects.all().order_by('id')
        self.object_list = books
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


@login_required(login_url='/owner/login/')
def book_edit(request, book_id=None):
    """書籍の編集"""
    if book_id:   # book_id が指定されている (修正時)
        book = get_object_or_404(Book, pk=book_id)
    else:         # book_id が指定されていない (追加時)
        book = Book()

    if request.method == 'POST':
        # POST された request データからフォームを作成
        form = BookForm(request.POST, instance=book)
        if form.is_valid():    # フォームのバリデーション
            book = form.save(commit=False)
            book.save()
            return HttpResponseRedirect(reverse('owner:book_list'))
    else:    # GET の時
        form = BookForm(instance=book)  # book インスタンスからフォームを作成

    return render(request, 'owner/book_edit.html', dict(form=form, book_id=book_id))


@login_required(login_url='/owner/login/')
def book_del(request, book_id):
    """書籍の削除"""
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return HttpResponseRedirect(reverse('owner:book_list'))


@method_decorator(login_required(login_url='owner:login'), name='dispatch')
class ImpressionList(ListView):
    """感想の一覧"""
    context_object_name = 'impressions'
    template_name = 'owner/impression_list.html'
    paginate_by = 2  # １ページは最大2件ずつでページングする

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['book_id'])  # 親の書籍を読む
        impressions = book.impressions.all().order_by('id')   # 書籍の子供の、感想を読む
        self.object_list = impressions

        context = self.get_context_data(
            object_list=self.object_list, book=book)
        return self.render_to_response(context)


@login_required(login_url='/owner/login/')
def impression_edit(request, book_id, impression_id=None):
    """感想の編集"""
    book = get_object_or_404(Book, pk=book_id)  # 親の書籍を読む
    if impression_id:   # impression_id が指定されている (修正時)
        impression = get_object_or_404(Impression, pk=impression_id)
    else:               # impression_id が指定されていない (追加時)
        impression = Impression()

    if request.method == 'POST':
        # POST された request データからフォームを作成
        form = ImpressionForm(request.POST, instance=impression)
        if form.is_valid():    # フォームのバリデーション
            impression = form.save(commit=False)
            impression.book = book  # この感想の、親の書籍をセット
            impression.save()
            return HttpResponseRedirect(reverse('owner:impression_list', kwargs={'book_id': book_id}))
    else:    # GET の時
        # impression インスタンスからフォームを作成
        form = ImpressionForm(instance=impression)

    return render(request,
                  'owner/impression_edit.html',
                  dict(form=form, book_id=book_id, impression_id=impression_id))


@login_required(login_url='/owner/login/')
def impression_del(request, book_id, impression_id):
    """感想の削除"""
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    return HttpResponseRedirect(reverse('owner:impression_list', kwargs={'book_id': book_id}))


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


@login_required(login_url='/owner/login/')
@csrf_exempt
def policies(request):
    key = '%s/%s' % (request.user.id, datetime.now().strftime("%Y%m%d%H%M%S"))
    content_type = request.POST['content_type']
    size = request.POST['size']
    t = datetime.utcnow()
    dict = {
        'expiration': (t + timedelta(minutes=1)).isoformat(),
        'conditions': [
            {'bucket': settings.S3_BUCKET},
            {'key': key},
            {'Content-Type': content_type},
            ['content-length-range', size, size]
        ]
    }
    policy_document = json.dumps(dict)
    policy = base64.b64encode(policy_document.encode('utf-8'))

    date_stamp = t.strftime('%Y%m%d')
    service = 's3'
    region = 'ap-northeast-1'
    signing_key = getSignatureKey(settings.AWS_SECRET_ACCESS_KEY, date_stamp, region, service)
    signature = hmac.new(signing_key, policy, hashlib.sha256).hexdigest()

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
    signed_headers = 'content-type;host;x-amz-date;x-amz-target'
    authorization_header = algorithm + ' ' + 'Credential=' + settings.AWS_ACCESS_KEY_ID + '/' + credential_scope + ', ' + 'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    array = {
        "url": "https://" + settings.S3_BUCKET + ".s3.amazonaws.com/",
        'form': {
            'AWSAccessKeyId': settings.AWS_ACCESS_KEY_ID,
            'signature': signature,
            'policy': policy.decode('utf-8'),
            'key': key,
            'Content-Type': content_type,
            'X-Amz-Date': amz_date,
            'Authorization': authorization_header
        }
    }
    return JsonResponse(array)
