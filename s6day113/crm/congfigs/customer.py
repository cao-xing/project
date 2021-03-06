import json
import datetime
from django.conf.urls import url
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponse,redirect
from django.forms import ModelForm

from crm import models
from stark.service import v1

class SingleModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant','status','recv_date','last_consult_date']



class CustomerConfig(v1.StarkConfig):

    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return '性别'
        return obj.get_gender_display()

    def display_education(self,obj=None,is_header=False):
        if is_header:
            return '学历'
        return obj.get_education_display()

    def display_course(self,obj=None,is_header=False):
        if is_header:
            return '咨询课程'
        course_list = obj.course.all()
        html = []
        # self.request.GET
        # self._query_param_key
        # 构造QueryDict
        # urlencode()
        for item in course_list:
            temp = "<a style='display:inline-block;padding:3px 5px;border:1px solid blue;margin:2px;' href='/stark/crm/customer/%s/%s/dc/'>%s X</a>" %(obj.pk,item.pk,item.name)
            html.append(temp)

        return mark_safe("".join(html))

    def display_status(self,obj=None,is_header=False):
        if is_header:
            return '状态'
        return obj.get_status_display()

    def record(self,obj=None,is_header=False):
        if is_header:
            return '跟进记录'
        # /stark/crm/consultrecord/?customer=11
        return mark_safe("<a href='/stark/crm/consultrecord/?customer=%s'>查看跟进记录</a>" %(obj.pk,))

    list_display = ['qq','name',display_gender,display_education,display_course,display_status,record]
    edit_link = ['qq']



    def delete_course(self,request,customer_id,course_id):
        """
        删除当前用户感兴趣的课程
        :param request: 
        :param customer_id: 
        :param course_id: 
        :return: 
        """
        customer_obj = self.model_class.objects.filter(pk=customer_id).first()
        customer_obj.course.remove(course_id)
        # 跳转回去时，要保留原来的搜索条件
        return redirect(self.get_list_url())

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        patterns = [
            url(r'^(\d+)/(\d+)/dc/$', self.wrap(self.delete_course), name="%s_%s_dc" %app_model_name),
            url(r'^public/$', self.wrap(self.public_view), name="%s_%s_public" %app_model_name),
            url(r'^user/$', self.wrap(self.user_view), name="%s_%s_user" %app_model_name),
            url(r'^(\d+)/competition/$', self.wrap(self.competition_view), name="%s_%s_competition" %app_model_name),
            url(r'^single/$', self.wrap(self.single_view), name="%s_%s_single" %app_model_name),
        ]
        return patterns

    def public_view(self,request):
        """
        公共客户资源
        :param request: 
        :return: 
        """
        # 条件：未报名 并且 （ 15天未成单(当前时间-15 > 接客时间) or  3天未跟进(当前时间-3天>最后跟进日期) ） Q对象
        # status=2
        import datetime


        ctime = datetime.datetime.now().date()
        no_deal = ctime - datetime.timedelta(days=15)  # 接客
        no_follow = ctime - datetime.timedelta(days=3) # 最后跟进日期

        #current_user = 1
        # models.Customer.objects.filter(Q(recv_date__lt=no_deal)|Q(last_consult_date__lt=no_follow),status=2).exclude(consultant_id=1)
        # 作业：两种方法实现
        customer_list = models.Customer.objects.filter(Q(recv_date__lt=no_deal)|Q(last_consult_date__lt=no_follow),status=2)
        return render(request,'public_view.html',{'customer_list':customer_list})

    def competition_view(self,request,cid):
        """
        抢单
        :param request: 
        :param nid: 
        :return: 
        """
        current_user_id = 6
        # 修改客户表
        # recv_date
        # last_consult_date
        # consultant
        ctime = datetime.datetime.now().date()
        # 必须原顾问不是自己
        # 状态必须是未报名
        # 3/15天
        # models.Customer.objects.filter(id=cid).
        # update(recv_date=ctime,last_consult_date=ctime,consultant_id=current_user_id)
        ctime = datetime.datetime.now().date()
        no_deal = ctime - datetime.timedelta(days=15)  # 接客
        no_follow = ctime - datetime.timedelta(days=3)  # 最后跟进日期

        row_count = models.Customer.objects.filter(Q(recv_date__lt=no_deal) | Q(last_consult_date__lt=no_follow), status=2,id=cid).exclude(consultant_id=current_user_id).update(recv_date=ctime,last_consult_date=ctime,consultant_id=current_user_id)
        if not row_count:
            return HttpResponse('手速太慢了')

        models.CustomerDistribution.objects.create(user_id=current_user_id,customer_id=cid,ctime=ctime)

        return HttpResponse('抢单成功')

    def user_view(self,request):
        """
        当前登录用户的所有客户
        :param request: 
        :return: 
        """
        # 去session中获取当前登录用户ID
        current_user_id = 6

        # 当前用户的所有客户列表
        customers = models.CustomerDistribution.objects.filter(user_id=current_user_id).order_by('status')

        return render(request,'user_view.html',{'customers':customers})


    def single_view(self,request):
        """
        单条录入客户信息
        :param request: 
        :return: 
        """

        if request.method == "GET":
            form = SingleModelForm()
            return render(request,'single_view.html',{'form':form})
        else:
            from xxxxxx import XXX
            form = SingleModelForm(request.POST)

            if form.is_valid():
                print(form.cleaned_data)
                sale_id = XXX.get_sale_id()
                """客户表新增数据：
                    - 获取该分配的课程顾问id
                    - 当前时间
                 客户分配表中新增数据
                    - 获取新创建的客户ID
                    - 顾问ID
                """

                return HttpResponse('录入成功')

            else:
                return render(request, 'single_view.html', {'form': form})

















