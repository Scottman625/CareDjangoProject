from calendar import weekday
import queue
from unicodedata import category
from unittest import case
from interval import Interval
from dateutil.parser import parse
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg ,Count
# Create your views here.
import datetime 
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
import datetime 
from modelCore.models import User, MarkupItem, License, Servant,ServantWeekdayTime, ServantMarkupItemPrice, ServantSkill,UserLicenseShipImage
from modelCore.models import ServantLicenseShipImage, Recipient, ServiceItem, City, CityArea, Transportation, Case,OrderState, Order, OrderReview  
from modelCore.models import CaseServiceItemShip ,ServantServiceItemShip,Message,SystemMessage
from api import serializers

class CreateListModelMixin:

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)
        
class MarkupItemViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = MarkupItem.objects.all()
    serializer_class = serializers.MarkupItemSerializer

class CsrfExemptSessionAuthentication(SessionAuthentication):
    
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class LicenseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = License.objects.all()
    serializer_class = serializers.LicenseSerializer

class ServantSearchViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    # http://127.0.0.1:8000/api/servant_Recommend?sort=HighPrice
    queryset = Servant.objects.all()
    serializer_class = serializers.ServantSerializer
    lookup_url_kwarg = "uid"
    # care_type_id 1=home 2=hospital 3=all
    def filter_queryset(self, queryset):
        queryset = self.queryset 
        care_type_id = self.request.GET.get('care_type_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        city_id = self.request.GET.get('city_id')
        area = self.request.GET.get('area_id')
        all_time_service = self.request.GET.get('all_time_service')
        weekday_choose = self.request.GET.get('weekday_choose')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        start_time = self.request.GET.get('start_time')
        end_time = self.request.GET.get('end_time')
        sort = self.request.GET.get('sort')
        start_time = datetime.time(int(start_time.split(':')[0]),int(start_time.split(':')[1]))
        end_time = datetime.time(int(end_time.split(':')[0]),int(end_time.split(':')[1]))

        if cityarea_id != None:
            queryset = queryset.filter(transportations__cityarea=CityArea.objects.get(id=cityarea_id))
        if (city_id and area) != None :
            queryset = queryset.filter(transportations=Transportation.objects.filter(cityarea=CityArea.objects.get(city=City.objects.get(id=city_id),area=area)))
        
        if all_time_service != None:
            queryset.filter(is_alltime_service=True)
        elif weekday_choose != None:
            weekday_list = weekday_choose.split(',')
            for i in range(len(weekday_list)):
                queryset = queryset.filter(weekdayTimes__weekday=weekday_list[i],weekdayTimes__start_time__lte=start_time,weekdayTimes__end_time__gte=end_time)
        if care_type_id == '1':
            queryset = queryset.filter(is_home=True)
            caretype = '????????????'
        elif care_type_id == '2':
            queryset = queryset.filter(is_hospital=True)
            caretype = '????????????'
        elif care_type_id == '3':
            caretype = '????????????'
        for i in range(len(queryset)):
            Score_Dict = OrderReview.objects.filter(order__case__servant=queryset[i],servant_is_rated=True).aggregate(avg_rating=Avg('servant_score'))
            queryset[i].score = Score_Dict['avg_rating']
            queryset[i].save()
            print(queryset[i].score)
            Num_Dict = OrderReview.objects.filter(order__case__servant=queryset[i],servant_is_rated=True).aggregate(num=Count('servant_score'))
            queryset[i].servant_ratedNum = Num_Dict['num']
            serviceCityList = {}
            serviceCity = Transportation.objects.filter(servant=queryset[i])
            for x in range(len(serviceCity)):  
                serviceCityList['serviceCity'+str(x+1)] = str(serviceCity[x].cityarea.city)
            queryset[i].service_city = serviceCityList
            queryset[i].search_result_city = CityArea.objects.get(id=cityarea_id).city
            queryset[i].search_result_date = start_date + "~" + end_date
            queryset[i].search_result_caretype = caretype
            
        if sort == 'HighScore':
            return queryset.order_by('-score')
        elif sort == 'LowScore':
            return queryset.order_by('score')
        elif sort == 'HighPrice':
            return queryset.order_by('-home_hourly_wage')
        elif sort == 'LowPrice':
            return queryset.order_by('home_hourly_wage')
        else:
            return queryset

    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        theServant = Servant.objects.get(id=uid)
        Num_Dict = OrderReview.objects.filter(order__case__servant=theServant,servant_is_rated=True).aggregate(num=Count('servant_score'))
        theServant.servant_ratedNum = Num_Dict['num']
        Score_Dict = OrderReview.objects.filter(order__case__servant=theServant,servant_is_rated=True).aggregate(avg_rating=Avg('servant_score'))
        theServant.score = Score_Dict['avg_rating']
        CareType_Dict = {}
        if theServant.is_home == True :
            CareType_Dict['1'] = '????????????'
        if theServant.is_hospital == True :
            CareType_Dict['2'] = '????????????'
        LanguageSkill_Dict = {}
        for i in range(len(ServantSkill.objects.filter(servant=theServant))):
            LanguageSkill_Dict[str(i+1)] = ServantSkill.objects.filter(servant=theServant)[i].languageSkill
        theServant.Languageskill = LanguageSkill_Dict

        ServiceRegion_Dict = {}
        for i in range(len(Transportation.objects.filter(servant=theServant))):
            ServiceRegion_Dict[str(i+1)] = Transportation.objects.filter(servant=theServant)[i].cityarea.city + Transportation.objects.filter(servant=theServant)[i].cityarea.area
        theServant.service_region = ServiceRegion_Dict

        ServiceItem_Dict = {}
        for i in range(len(ServantServiceItemShip.objects.filter(servant=theServant))):
            ServiceItem_Dict[str(i+1)] = ServantServiceItemShip.objects.filter(servant=theServant)[i].service_item
        theServant.service_item = ServiceItem_Dict

        License_Dict = {}
        for i in range(len(ServantLicenseShipImage.objects.filter(servant=theServant))):
            License_Dict[str(i+1)] = ServantLicenseShipImage.objects.filter(servant=theServant)[i].license
        theServant.licenses = License_Dict

        Review_Dict = {}
        for i in range(len(OrderReview.objects.filter(order__case__servant=theServant))):
            Review_Dict['user_'+str(i+1)] = OrderReview.objects.filter(order__case__servant=theServant)[i].order.case.recipient.user
            Review_Dict['create_date_'+str(i+1)] = OrderReview.objects.filter(order__case__servant=theServant)[i].servant_review_createdate
            Review_Dict['score_'+str(i+1)] = OrderReview.objects.filter(order__case__servant=theServant)[i].servant_score
            Review_Dict['content_'+str(i+1)] = OrderReview.objects.filter(order__case__servant=theServant)[i].servant_content
        theServant.order_review = Review_Dict

        serializer = self.get_serializer(theServant)
        return Response(serializer.data)


class ServantMarkupItemPriceViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ServantMarkupItemPrice.objects.all()
    serializer_class = serializers.ServantMarkupItemPriceSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        markupItem_id = self.request.GET.get('markupItem_id')
        queryset = queryset.filter(servant__user=theUser)
        if markupItem_id != None:
            queryset = queryset.filter(markup_item=MarkupItem.objects.get(id=markupItem_id))
        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].markup_item_name = queryset[i].markup_item.name
        return queryset



class UserLicenseShipImageViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserLicenseShipImage.objects.all()
    serializer_class = serializers.UserLicenseShipImageSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        license_id = self.request.GET.get('license_id')
        queryset = queryset.filter(user=user)
        if license_id != None:
            queryset = queryset.filter(license=License.objects.get(id=license_id))
        for i in range(len(queryset)):
            queryset[i].user_name = queryset[i].user.name
            queryset[i].license_name = queryset[i].license.name
        return queryset

class ServantLicenseShipImageViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ServantLicenseShipImage.objects.all()
    serializer_class = serializers.ServantLicenseShipImageSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        
        license_id = self.request.GET.get('license_id')
        queryset = queryset.filter(servant__user=theUser)
        if license_id != None:
            queryset = queryset.filter(license=License.objects.get(id=license_id))
        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].license_name = queryset[i].license.name
        return queryset

class RecipientViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipient.objects.all()
    serializer_class = serializers.RecipientSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        recipient_name = self.request.GET.get('recipient_name')
        queryset = queryset.filter(user=theUser)
        if recipient_name != None:
            queryset = queryset.filter(name=recipient_name)
        # for i in range(len(queryset)):
        #     queryset[i].user_name = queryset[i].user.name
        return queryset

class ServiceItemViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    queryset = ServiceItem.objects.all()
    serializer_class = serializers.ServiceItemSerializer

class CaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(recipient__user=theUser)
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        if servant_id != None:
            queryset = queryset.filter(servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(cityarea=CityArea.objects.get(id=cityarea_id))
        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].recipient_name = queryset[i].recipient.name
            queryset[i].cityarea_name = queryset[i].cityarea.city + queryset[i].cityarea.area

        return queryset

class CaseSearchViewSet(APIView):
 
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def post(self,request):
        queryset = self.queryset
        cityarea = request.data.get('cityarea')
        startDate_set = request.data.get('startDate_set')
        endDate_set = request.data.get('endDate_set')
        care_type = request.data.get('care_type')
        startDate_set = datetime.date(int(startDate_set.split('-')[0]),int(startDate_set.split('-')[1]),int(startDate_set.split('-')[2]))
        endDate_set = datetime.date(int(endDate_set.split('-')[0]),int(endDate_set.split('-')[1]),int(endDate_set.split('-')[2]))

        if cityarea != None:
            queryset = queryset.filter(case__cityarea=CityArea.objects.get(name=cityarea))
        if (startDate_set != None) and (endDate_set != None):
            queryset = queryset.filter(start_date__gte=startDate_set,end_date__lte=endDate_set)
            print(queryset)
        
        if care_type == '????????????':
            queryset = queryset.filter(servant__is_home=True)
        elif care_type == '????????????':
            queryset = queryset.filter(servant__is_hospital=True)
        else: 
            pass

        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].recipient_name = queryset[i].recipient.name
            queryset[i].cityarea_name = queryset[i].cityarea.city + queryset[i].cityarea.area
            CareTypeDict = {}
            if queryset[i].servant.is_home == True:
                CareTypeDict['caretype_1'] = '????????????'
            if queryset[i].servant.is_hospital == True:
                CareTypeDict['caretype_2'] = '????????????'
            queryset[i].CareType = CareTypeDict
            if queryset[i].servant.is_alltime_service == True:
                queryset[i].TimeType = '????????????'
            else:
                queryset[i].TimeType = '????????????'

        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class CaseDetailViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):


    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer
    lookup_url_kwarg = "uid"

    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        case = Case.objects.get(id=uid)
        if case.is_taken == True:
            case.status = '???????????????'
        else:
            case.status = '?????????????????????'
        if case.is_taken == True:
            case.servant_name = case.servant.user.name
            if case.servant.is_home == True :
                hour_wage = case.servant.home_hourly_wage
            else:
                hour_wage = case.servant.hospital_hourly_wage

            working_hours = ((case.end_time).hour - (case.start_time).hour) * (((case.end_date) - (case.start_date)).days)
            case.working_hours =  working_hours 
            case.basic_price =  hour_wage * working_hours
            case.hour_wage =  hour_wage 
            case.markup_price = round(((case.markup_item.pricePercent)-1) * hour_wage * working_hours)
            case.platform_fee = round((case.markup_item.pricePercent) * 0.15 * hour_wage * working_hours)
            case.total_price = round((case.markup_item.pricePercent) *(1-0.15)  * hour_wage * working_hours)

        
        case.recipient_name = case.recipient.name
        case.recipient_gender = case.recipient.gender
        case.recipient_age = case.recipient.age
        case.recipient_weight = case.recipient.weight
        case.recipient_disease = case.recipient.disease
        case.recipient_conditions = case.recipient.conditions
        case.recipient_disease_info = case.recipient.disease_info
        case.recipient_conditions_info = case.recipient.conditions_info
        case.cityarea_name = case.cityarea.city + case.cityarea.area
        
        if case.is_alltime_service == True:
            case.TimeType = '????????????'
        else:
            case.TimeType = '????????????'
        case.case_date = str(case.start_date) + ' ~ ' + str(case.end_date)
        case.markup_Item = case.markup_item.markup_item
        case.markup_Item_percent =  str(((case.markup_item.pricePercent)*100) - 100) + '%'
        service_Items = CaseServiceItemShip.objects.filter(case=case)
        All_service_item = {}
        for x in range(len(service_Items)):                
            All_service_item['serviveItem'+str(x+1)] = str(service_Items[x].service_item)
        case.service_Item =  All_service_item
        print(case.care_type)

        serializer = self.get_serializer(case)
        return Response(serializer.data)

class OrderStateViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = OrderState.objects.all()
    serializer_class = serializers.OrderStateSerializer

class OrderViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(case__recipient__user=theUser)
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        if servant_id != None:
            queryset = queryset.filter(case__servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(case__cityarea=CityArea.objects.get(id=cityarea_id))

        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].case.servant.user.name
            queryset[i].recipient_name = queryset[i].case.recipient.name
            queryset[i].cityarea_name = queryset[i].case.cityarea.city + queryset[i].case.cityarea.area
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, cashflowState='unPaid')

class OrderReviewViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(order__case__recipient__user=theUser)
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        if servant_id != None:
            queryset = queryset.filter(order__case__servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(order__case__cityarea=CityArea.objects.get(id=cityarea_id))

        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].recipient_name = queryset[i].order.case.recipient.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
        
        return queryset

class MYPostCaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer
    lookup_url_kwarg = "uid"

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
 
        queryset = queryset.filter(recipient__user=theUser)
        for i in range(len(queryset)):
            CareTypeDict = {}
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].recipient_name = queryset[i].recipient.name
            if queryset[i].servant.is_home == True:
                CareTypeDict['caretype_1'] = '????????????'
            if queryset[i].servant.is_hospital == True:
                CareTypeDict['caretype_2'] = '????????????'
            queryset[i].CareType = CareTypeDict
            if queryset[i].servant.is_alltime_service == True:
                queryset[i].TimeType = '????????????'
            else:
                queryset[i].TimeType = '????????????'
            queryset[i].case_date = str(queryset[i].start_date) + ' ~ ' + str(queryset[i].end_date)

        return queryset
       
    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        theUser = self.request.user
        case = Case.objects.get(id=uid)
    
        if case.recipient.user == theUser:
            if case.servant.is_home == True :
                hour_wage = case.servant.home_hourly_wage
            else:
                hour_wage = case.servant.hospital_hourly_wage

            working_hours = ((case.end_time).hour - (case.start_time).hour) * (((case.end_date) - (case.start_date)).days)
            CareTypeDict = {}
            case.quservant_name = case.servant.user.name
            case.recipient_name = case.recipient.name
            case.recipient_gender = case.recipient.gender
            case.recipient_age = case.recipient.age
            case.recipient_weight = case.recipient.weight
            case.recipient_disease = case.recipient.disease
            case.recipient_conditions = case.recipient.conditions
            case.recipient_disease_info = case.recipient.disease_info
            case.recipient_conditions_info = case.recipient.conditions_info
            case.cityarea_name = case.cityarea.city + case.cityarea.area
            if case.servant.is_home == True:
                CareTypeDict['caretype_1'] = '????????????'
            if case.servant.is_hospital == True:
                CareTypeDict['caretype_2'] = '????????????'
            case.CareType = CareTypeDict
            if case.servant.is_alltime_service == True:
                case.TimeType = '????????????'
            else:
                case.TimeType = '????????????'
            case.case_date = str(case.start_date) + ' ~ ' + str(case.end_date)
            case.basic_price =  hour_wage * working_hours
            case.hour_wage =  hour_wage 
            case.working_hours =  working_hours 
            case.markup_Item = case.markup_item.markup_item
            case.markup_Item_percent =  str(((case.markup_item.pricePercent)*100) - 100) + '%'
            case.markup_price = round(((case.markup_item.pricePercent)-1) * hour_wage * working_hours)
            case.total_price = round((case.markup_item.pricePercent) * hour_wage * working_hours)
            service_Items = CaseServiceItemShip.objects.filter(case=case)
            All_service_item = {}
            for x in range(len(service_Items)):                
                All_service_item['serviveItem'+str(x+1)] = str(service_Items[x].service_item)
            case.service_Item =  All_service_item

            serializer = self.get_serializer(case)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})
        
class MYTakeCaseViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer
    lookup_url_kwarg = "uid"

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(servant__user=theUser)
        
        
        for i in range(len(queryset)):
            queryset[i].user_name = queryset[i].recipient.user.name
            queryset[i].servant_name = queryset[i].servant.user.name
            queryset[i].recipient_name = queryset[i].recipient.name
            CareTypeDict = {}
            if queryset[i].servant.is_home == True:
                CareTypeDict['caretype_1'] = '????????????'
            if queryset[i].servant.is_hospital == True:
                CareTypeDict['caretype_2'] = '????????????'
            queryset[i].CareType = CareTypeDict
            if queryset[i].servant.is_alltime_service == True:
                queryset[i].TimeType = '????????????'
            else:
                queryset[i].TimeType = '????????????'
            queryset[i].case_date = str(queryset[i].start_date) + ' ~ ' + str(queryset[i].end_date)

        return queryset
    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        theUser = self.request.user
        case = Case.objects.get(id=uid)
        if case.servant.user == theUser:
            if case.servant.is_home == True :
                hour_wage = case.servant.home_hourly_wage
            else:
                hour_wage = case.servant.hospital_hourly_wage

            working_hours = ((case.end_time).hour - (case.start_time).hour) * (((case.end_date) - (case.start_date)).days)
            CareTypeDict = {}
            case.quservant_name = case.servant.user.name
            case.recipient_name = case.recipient.name
            case.recipient_gender = case.recipient.gender
            case.recipient_age = case.recipient.age
            case.recipient_weight = case.recipient.weight
            case.recipient_disease = case.recipient.disease
            case.recipient_conditions = case.recipient.conditions
            case.recipient_disease_info = case.recipient.disease_info
            case.recipient_conditions_info = case.recipient.conditions_info
            case.cityarea_name = case.cityarea.city + case.cityarea.area
            if case.servant.is_home == True:
                CareTypeDict['caretype_1'] = '????????????'
            if case.servant.is_hospital == True:
                CareTypeDict['caretype_2'] = '????????????'
            case.CareType = CareTypeDict
            if case.servant.is_alltime_service == True:
                case.TimeType = '????????????'
            else:
                case.TimeType = '????????????'
            case.case_date = str(case.start_date) + ' ~ ' + str(case.end_date)
            case.basic_price =  hour_wage * working_hours
            case.hour_wage =  hour_wage 
            case.working_hours =  working_hours 
            case.markup_Item = case.markup_item.markup_item
            case.markup_Item_percent =  str(((case.markup_item.pricePercent)*100) - 100) + '%'
            case.markup_price = round(((case.markup_item.pricePercent)-1) * hour_wage * working_hours)
            case.platform_fee = round((case.markup_item.pricePercent) * 0.15 * hour_wage * working_hours)
            case.total_price = round((case.markup_item.pricePercent) *(1-0.15)  * hour_wage * working_hours)
            service_Items = CaseServiceItemShip.objects.filter(case=case)
            All_service_item = {}
            for x in range(len(service_Items)):                
                All_service_item['serviveItem'+str(x+1)] = str(service_Items[x].service_item)
            case.service_Item =  All_service_item

            serializer = self.get_serializer(case)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})

class NotRatedYetViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(order__case__recipient__user=theUser)
        queryset = queryset.filter(servant_is_rated=False)
        servant_id = self.request.GET.get('servant_id')
        cityarea_id = self.request.GET.get('cityarea_id')
        if servant_id != None:
            queryset = queryset.filter(order__case__servant=Servant.objects.get(id=servant_id))
        
        if cityarea_id != None:
            queryset = queryset.filter(order__case__cityarea=CityArea.objects.get(id=cityarea_id))

        for i in range(len(queryset)):
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].recipient_name = queryset[i].order.case.recipient.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
            CareTypeDict = {}
            if queryset[i].case.servant.is_home == True:
                CareTypeDict['caretype_1'] = '????????????'
            if queryset[i].case.servant.is_hospital == True:
                CareTypeDict['caretype_2'] = '????????????'
            queryset[i].CareType = CareTypeDict
            if queryset[i].case.servant.is_alltime_service == True:
                queryset[i].TimeType = '????????????'
            else:
                queryset[i].TimeType = '????????????'
            queryset[i].case_date = str(queryset[i].order.case.start_date) + ' ~ ' + str(queryset[i].order.case.end_date)
        
        return queryset

class AddServantRateViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def post(self, request, format=None):
        user = self.request.user
        order_id = request.data.get('order_id')
        servantContent = request.data.get('servantContent')
        servantScore = request.data.get('servantScore')
        orderReview = OrderReview.objects.get(order=order_id)

        if orderReview.order.case.recipient.user == user:
            orderReview.servant_content = servantContent
            orderReview.servant_score = servantScore
            orderReview.servant_is_rated = True
            orderReview.servant_review_createdate = datetime.now()
            orderReview.save()
            return Response({'message': "ok"})
        else:
            return Response({'message': "have no authority"})

class AddUserRateViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def post(self, request, format=None):
        user = self.request.user
        order_id = request.data.get('order_id')
        userContent = request.data.get('userContent')
        userScore = request.data.get('userScore')
        orderReview = OrderReview.objects.get(order=order_id)

        if orderReview.order.case.servant.user == user:
            orderReview.user_content = userContent
            orderReview.user_score = userScore
            orderReview.user_is_rated = True
            orderReview.user_review_createdate = datetime.now()
            orderReview.save()
            return Response({'message': "ok"})
        else:
            return Response({'message': "have no authority"})

class ServantRateViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer
    lookup_url_kwarg = "uid"

    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(order__case__recipient__user=theUser)
        queryset = queryset.filter(servant_is_rated=True)
        print(theUser)

        for i in range(len(queryset)):
            queryset[i].user_name = theUser
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
            CareTypeDict = {}
            if queryset[i].case.servant.is_home == True:
                CareTypeDict['caretype_1'] = '????????????'
            if queryset[i].case.servant.is_hospital == True:
                CareTypeDict['caretype_2'] = '????????????'
            queryset[i].CareType = CareTypeDict
            if queryset[i].case.servant.is_alltime_service == True:
                queryset[i].TimeType = '????????????'
            else:
                queryset[i].TimeType = '????????????'
            queryset[i].case_date = str(queryset[i].order.case.start_date) + ' ~ ' + str(queryset[i].order.case.end_date)
        
        return queryset

    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        theUser = self.request.user
        orderReview = self.queryset.get(id=uid)
        if orderReview.order.case.recipient.user == theUser:
            orderReview.servant_name = orderReview.order.case.servant.user
            serializer = self.get_serializer(orderReview)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})

class UserRateViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrderReview.objects.all()
    serializer_class = serializers.OrderReviewSerializer
    lookup_url_kwarg = "uid"
    
    def get_queryset(self):
        queryset = self.queryset
        theUser = self.request.user
        queryset = queryset.filter(order__case__recipient__user=theUser)
        queryset = queryset.filter(user_is_rated=True)
        
        for i in range(len(queryset)):
            queryset[i].user_name = theUser
            queryset[i].servant_name = queryset[i].order.case.servant.user.name
            queryset[i].cityarea_name = queryset[i].order.case.cityarea.city + queryset[i].order.case.cityarea.area
            CareTypeDict = {}
            if queryset[i].case.servant.is_home == True:
                CareTypeDict['caretype_1'] = '????????????'
            if queryset[i].case.servant.is_hospital == True:
                CareTypeDict['caretype_2'] = '????????????'
            queryset[i].CareType = CareTypeDict
            if queryset[i].case.servant.is_alltime_service == True:
                queryset[i].TimeType = '????????????'
            else:
                queryset[i].TimeType = '????????????'
            queryset[i].case_date = str(queryset[i].order.case.start_date) + ' ~ ' + str(queryset[i].order.case.end_date)
        
        return queryset

    def retrieve(self, request,uid):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        theUser = self.request.user
        orderReview = self.queryset.get(id=uid)
        if orderReview.order.case.recipient.user == theUser:
            orderReview.servant_name = orderReview.order.case.servant.user
            serializer = self.get_serializer(orderReview)
            return Response(serializer.data)
        else:
            return Response({'message': "have no authority"})

class ChangeBasicInfoViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.OrderReviewSerializer

    def post(self, request, format=None):
        theuser = self.request.user
        phone = request.data.get('phone')
        gender = request.data.get('gender')
        address = request.data.get('address')
        email = request.data.get('email')
        line_id = request.data.get('line_id')
        image = request.data.get('image')
        user = theuser
        if user == theuser:
            user.phone = phone
            user.gender = gender
            user.address = address
            user.email = email
            user.line_id = line_id
            user.image = image
            user.save()
            return Response({'message': "ok"})
        else:
            return Response({'message': "have no authority"})

class MyDocumentViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserLicenseShipImage.objects.all()
    serializer_class = serializers.UserLicenseShipImageSerializer

    def post(self, request, format=None):
        queryset = self.queryset
        theuser = self.request.user
        queryset = queryset.filter(user=theuser)
        ID_card_front = request.data.get('ID_card_front')
        ID_card_back = request.data.get('ID_card_back')
        health_ID_card = request.data.get('health_ID_card')

        queryset_front = queryset.get(license=License.objects.get(id=1))
        queryset_back = queryset.get(license=License.objects.get(id=2))
        queryset_health = queryset.get(license=License.objects.get(id=3))

        if queryset_front.user == theuser:
            queryset_front.image = ID_card_front
            queryset_front.save()
            queryset_back.image = ID_card_back
            queryset_back.save()
            queryset_health.image = health_ID_card
            queryset_health.save()
            return Response({'message': "ok"})

            
        else:
            return Response({'message': "have no authority"})

class ServiceSettingsViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ServantSerializer
    # ?????? gender : M
    # ????????????  monday : True , monday_startTime : 11:30 , monday_endTime : 21:30
    # ?????? Chinese : True
    # ???????????? hospital_care : True , hospital_hourly_wage : 300
    # ???????????? add_region_num???1 , city_1 : ????????? , area_1 : ?????? , transportation_1 : 200
    # ???????????? service_item_id_1 : ????????????
    # ???????????? license_name_1 : ??????????????? , license_image_1 : image_001.jpeg

    def post(self,request):
        theUser = self.request.user
        theServant = Servant.objects.get(user=theUser)
        gender = request.data.get('gender')
        
        all_time = request.data.get('all_time')
        monday = request.data.get('monday')
        monday_startTime = request.data.get('monday_startTime')
        monday_endTime = request.data.get('monday_endTime')
        tuesday = request.data.get('tuesday')
        tuesday_startTime = request.data.get('tuesday_startTime')
        tuesday_endTime = request.data.get('tuesday_endTime')
        wednesday = request.data.get('wednesday')
        wednesday_startTime = request.data.get('wednesday_startTime')
        wednesday_endTime = request.data.get('wednesday_endTime')
        thursday = request.data.get('thursday')
        thursday_startTime = request.data.get('thursday_startTime')
        thursday_endTime = request.data.get('thursday_endTime')
        friday = request.data.get('friday')
        friday_startTime = request.data.get('friday_startTime')
        friday_endTime = request.data.get('friday_endTime')
        saturday = request.data.get('saturday')
        saturday_startTime = request.data.get('saturday_startTime')
        saturday_endTime = request.data.get('saturday_endTime')
        sunday = request.data.get('sunday')
        sunday_startTime = request.data.get('sunday_startTime')
        sunday_endTime = request.data.get('sunday_endTime')
        

        Chinese = request.data.get('Chinese')
        Taiwanese = request.data.get('Taiwanese')
        Hakka = request.data.get('Hakka')
        Cantonese = request.data.get('Cantonese')
        Aboriginal = request.data.get('Aboriginal')
        Aboriginal_Type = request.data.get('Aboriginal_Type')
        Japanese = request.data.get('Japanese')
        English = request.data.get('English')
        other= request.data.get('other')
        other_Language = request.data.get('other_Language')
        home_care = request.data.get('home_care')
        hospital_care = request.data.get('hospital_care')
        home_hourly_wage = request.data.get('home_hourly_wage')
        home_halfday_wage = request.data.get('home_halfday_wage')
        home_oneday_wage = request.data.get('home_oneday_wage')
        hospital_hourly_wage = request.data.get('hospital_hourly_wage')
        hospital_halfday_wage = request.data.get('hospital_halfday_wage')
        hospital_oneday_wage = request.data.get('hospital_oneday_wage')
        add_region_num = request.data.get('add_region_num')
        is_emergency = request.data.get('is_emergency')
        emergency_pricePercent = request.data.get('emergency_pricePercent')
        is_contagious = request.data.get('is_contagious')
        contagious_pricePercent= request.data.get('contagious_pricePercent')
        is_over70 = request.data.get('is_over70')
        over70_pricePercent= request.data.get('over70_pricePercent')
        is_over90 = request.data.get('is_over90')
        over90_pricePercent= request.data.get('over90_pricePercent')
        info = request.data.get('info')
        background_image = request.data.get('background_image')
        service_item_num = ServiceItem.objects.all().count()
        licenses = License.objects.all()
        print(emergency_pricePercent)
        theServant.gender = gender

        if all_time  == 'True' :
            timeship = ServantWeekdayTime()
            timeship.servant = theServant
            timeship.weekday = '7'
            timeship.start_time = datetime.time(0,0,0)
            timeship.end_time = datetime.time(23,59,59)
            timeship.save()
        else:
            if monday == 'True' :
                if ServantWeekdayTime.objects.filter(servant=theServant,weekday='1').exists() != True:
                    timeship = ServantWeekdayTime()
                    
                else:
                    timeship = ServantWeekdayTime.objects.get(servant=theServant,weekday='1')
                timeship.servant = theServant
                timeship.weekday = '1'
                timeship.start_time = datetime.time(int(monday_startTime.split(':')[0]),int(monday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(monday_endTime.split(':')[0]),int(monday_endTime.split(':')[1]))
                timeship.save()

            if tuesday == 'True' :
                if ServantWeekdayTime.objects.filter(servant=theServant,weekday='2').exists() != True:
                    timeship = ServantWeekdayTime()
                    
                else:
                    timeship = ServantWeekdayTime.objects.get(servant=theServant,weekday='2')
                timeship.servant = theServant
                timeship.weekday = '2'
                timeship.start_time = datetime.time(int(tuesday_startTime.split(':')[0]),int(tuesday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(tuesday_endTime.split(':')[0]),int(tuesday_endTime.split(':')[1]))
                timeship.save()
                
            if wednesday == 'True' :
                if ServantWeekdayTime.objects.filter(servant=theServant,weekday='3').exists() != True:
                    timeship = ServantWeekdayTime()
                    
                else:
                    timeship = ServantWeekdayTime.objects.get(servant=theServant,weekday='3')
                timeship.servant = theServant
                timeship.weekday = '3'
                timeship.start_time = datetime.time(int(wednesday_startTime.split(':')[0]),int(wednesday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(wednesday_endTime.split(':')[0]),int(wednesday_endTime.split(':')[1]))
                timeship.save()
            if thursday == 'True' :
                if ServantWeekdayTime.objects.filter(servant=theServant,weekday='4').exists() != True:
                    timeship = ServantWeekdayTime()
                    
                else:
                    timeship = ServantWeekdayTime.objects.get(servant=theServant,weekday='4')
                timeship.servant = theServant
                timeship.weekday = '4'
                timeship.start_time = datetime.time(int(thursday_startTime.split(':')[0]),int(thursday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(thursday_endTime.split(':')[0]),int(thursday_endTime.split(':')[1]))
                timeship.save()
            if friday == 'True' :
                if ServantWeekdayTime.objects.filter(servant=theServant,weekday='5').exists() != True:
                    timeship = ServantWeekdayTime()
                    
                else:
                    timeship = ServantWeekdayTime.objects.get(servant=theServant,weekday='5')
                timeship.servant = theServant
                timeship.weekday = '5'
                timeship.start_time = datetime.time(int(friday_startTime.split(':')[0]),int(friday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(friday_endTime.split(':')[0]),int(friday_endTime.split(':')[1]))
                timeship.save()
            if saturday == 'True' :
                if ServantWeekdayTime.objects.filter(servant=theServant,weekday='6').exists() != True:
                    timeship = ServantWeekdayTime()
                    
                else:
                    timeship = ServantWeekdayTime.objects.get(servant=theServant,weekday='6')
                timeship.servant = theServant
                timeship.weekday = '6'
                timeship.start_time = datetime.time(int(saturday_startTime.split(':')[0]),int(saturday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(saturday_endTime.split(':')[0]),int(saturday_endTime.split(':')[1]))
                timeship.save()
            if sunday == True :
                if ServantWeekdayTime.objects.filter(servant=theServant,weekday='0').exists() != True:
                    timeship = ServantWeekdayTime()
                    
                else:
                    timeship = ServantWeekdayTime.objects.get(servant=theServant,weekday='0')
                timeship.servant = theServant
                timeship.weekday = '0'
                timeship.start_time = datetime.time(int(sunday_startTime.split(':')[0]),int(sunday_startTime.split(':')[1]))
                timeship.end_time = datetime.time(int(sunday_endTime.split(':')[0]),int(sunday_endTime.split(':')[1]))
                timeship.save()

        if (Chinese == 'True') and (ServantSkill.objects.filter(servant=theServant,languageSkill='??????').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '??????'
            servantskill.save()

        if (Taiwanese == 'True')and (ServantSkill.objects.filter(servant=theServant,languageSkill='??????').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '??????'
            servantskill.save()

        if (Hakka == 'True')and (ServantSkill.objects.filter(servant=theServant,languageSkill='?????????').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '?????????'
            servantskill.save()

        if (Cantonese == 'True')and (ServantSkill.objects.filter(servant=theServant,languageSkill='??????').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '??????'
            servantskill.save()

        if (Aboriginal == 'True')and (ServantSkill.objects.filter(servant=theServant,languageSkill=Aboriginal_Type).exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = Aboriginal_Type
            servantskill.save()

        if (Japanese == 'True') and (ServantSkill.objects.filter(servant=theServant,languageSkill='??????').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '??????'
            servantskill.save()

        if (English == 'True') and (ServantSkill.objects.filter(servant=theServant,languageSkill='??????').exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = '??????'
            servantskill.save()

        if (other == 'True') and (ServantSkill.objects.filter(servant=theServant,languageSkill=other_Language).exists() == False):
            servantskill = ServantSkill()
            servantskill.servant = theServant
            servantskill.languageSkill = other_Language
            servantskill.save()

        if home_care == 'True':
            
            theServant.is_home = True
            theServant.home_hourly_wage = home_hourly_wage
            theServant.home_halfday_wage = home_halfday_wage
            theServant.home_oneday_wage = home_oneday_wage
            

        if hospital_care == 'True':

            theServant.is_hospital = True
            theServant.hospital_hourly_wage = hospital_hourly_wage
            theServant.hospital_halfday_wage = hospital_halfday_wage
            theServant.hospital_oneday_wage = hospital_oneday_wage


        cityArealist = []
        transportation_dict = {}
        for i in range(int(add_region_num)):
            cityArealist.append({'city':request.data.get('city_'+str(i+1)),'area':request.data.get('area_'+str(i+1)),'transportation':request.data.get('transportation_'+str(i+1))})
            if  Transportation.objects.filter(servant=theServant,cityarea=CityArea.objects.get(city=cityArealist[i]['city'],area=cityArealist[i]['area'])).exists() == False:
               transportation = Transportation()
            else:
                transportation = Transportation.objects.get(servant=theServant,cityarea=CityArea.objects.get(city=cityArealist[i]['city'],area=cityArealist[i]['area']))
            transportation.servant = theServant
            transportation.cityarea = CityArea.objects.get(city=cityArealist[i]['city'],area=cityArealist[i]['area'])
            transportation.price = int(cityArealist[i]['transportation'])
            transportation.save()

        service_item_list = []
        service_item_count = 0
        for i in range(service_item_num):
            if request.data.get('service_item_'+str(i+1))  != None:
                service_item_count += 1
        for n in range(service_item_count):
            service_item_list.append({'service_item':request.data.get('service_item_'+str(n+1))}) 
            if  ServantServiceItemShip.objects.filter(servant=theServant,service_item=ServiceItem.objects.get(name=service_item_list[n]['service_item'])).exists() == False:
                servantItemShip = ServantServiceItemShip()
            else:
                servantItemShip = ServantServiceItemShip.objects.get(servant=theServant,service_item=ServiceItem.objects.get(name=service_item_list[n]['service_item']))

            servantItemShip.servant = theServant
            servantItemShip.service_item = ServiceItem.objects.get(name=service_item_list[n]['service_item'])
            servantItemShip.save()

        if is_emergency == 'True':
            if ServantMarkupItemPrice.objects.filter(servant=theServant,markup_item=MarkupItem.objects.get(id=1)).exists() == True :
                servantmarkupItemPrice = ServantMarkupItemPrice.objects.get(servant=theServant,markup_item=MarkupItem.objects.get(id=1))
            else:
                servantmarkupItemPrice = ServantMarkupItemPrice()
                servantmarkupItemPrice.servant = theServant
                servantmarkupItemPrice.markup_item = MarkupItem.objects.get(id=1)
            servantmarkupItemPrice.pricePercent = float(emergency_pricePercent)
            servantmarkupItemPrice.save()

        if is_contagious == 'True':
            if ServantMarkupItemPrice.objects.filter(servant=theServant,markup_item=MarkupItem.objects.get(id=2)).exists() == True :
                servantmarkupItemPrice = ServantMarkupItemPrice.objects.get(servant=theServant,markup_item=MarkupItem.objects.get(id=2))
            else:
                servantmarkupItemPrice = ServantMarkupItemPrice()
                servantmarkupItemPrice.servant = theServant
                servantmarkupItemPrice.markup_item = MarkupItem.objects.get(id=2)
            servantmarkupItemPrice.pricePercent = float(contagious_pricePercent)
            servantmarkupItemPrice.save()

        if is_over70 == 'True':
            if ServantMarkupItemPrice.objects.filter(servant=theServant,markup_item=MarkupItem.objects.get(id=3)).exists() == True :
                servantmarkupItemPrice = ServantMarkupItemPrice.objects.get(servant=theServant,markup_item=MarkupItem.objects.get(id=3))
            else:
                servantmarkupItemPrice = ServantMarkupItemPrice()
                servantmarkupItemPrice.servant = theServant
                servantmarkupItemPrice.markup_item = MarkupItem.objects.get(id=3)
            servantmarkupItemPrice.pricePercent = float(over70_pricePercent)
            servantmarkupItemPrice.save()

        if is_over90 == 'True':
            if ServantMarkupItemPrice.objects.filter(servant=theServant,markup_item=MarkupItem.objects.get(id=4)).exists() == True :
                servantmarkupItemPrice = ServantMarkupItemPrice.objects.get(servant=theServant,markup_item=MarkupItem.objects.get(id=4))
            else:
                servantmarkupItemPrice = ServantMarkupItemPrice()
                servantmarkupItemPrice.servant = theServant
                servantmarkupItemPrice.markup_item = MarkupItem.objects.get(id=4)
            servantmarkupItemPrice.pricePercent = float(over90_pricePercent)
            servantmarkupItemPrice.save()

        licenseImage_count = 0
        licenseImage_list = []
        for i in range(len(licenses)):
             if request.data.get('license_name_'+str(i+1))  != None:
                licenseImage_count += 1

        for n in range(licenseImage_count):
            licenseImage_list.append({'license_name':request.data.get('license_name_'+str(n+1))})
            if ServantLicenseShipImage.objects.filter(servant=theServant,license=License.objects.get(name=licenseImage_list[n]['license_name']),is_upload_image=True).exists() == True :
                licenseImage = ServantLicenseShipImage.objects.get(servant=theServant,license=License.objects.get(name=licenseImage_list[n]['license_name']))
            else:
                licenseImage = ServantLicenseShipImage()
                licenseImage.servant = theServant
                licenseImage.license = License.objects.get(name=licenseImage_list[n]['license_name'])
            licenseImage.image = request.data.get('license_image_'+str(n+1))
            licenseImage.is_upload_image = True
            licenseImage.save()

        theServant.info = info
        theServant.background_image = background_image

        # return data
        service_time_dict={}
        service_time = ServantWeekdayTime.objects.filter(servant=theServant)
        
        if service_time.filter(weekday='7').exists() == True :
            service_time_dict['????????????'] = '??????????????????'
        else:
            if service_time.filter(weekday='1').exists() == True :
                service_time_dict['monday'] = '?????????' + str(service_time.get(weekday='1').start_time) + '~' + str(service_time.get(weekday='1').end_time)
            if service_time.filter(weekday='2').exists() == True :
                service_time_dict['tuesday'] = '?????????' + str(service_time.get(weekday='2').start_time) + '~' + str(service_time.get(weekday='2').end_time)
            if service_time.filter(weekday='3').exists() == True :
                service_time_dict['wednesday'] = '?????????' + str(service_time.get(weekday='3').start_time) + '~' + str(service_time.get(weekday='3').end_time)
            if service_time.filter(weekday='4').exists() == True :
                service_time_dict['thursday'] = '?????????' + str(service_time.get(weekday='4').start_time) + '~' + str(service_time.get(weekday='4').end_time)
            if service_time.filter(weekday='5').exists() == True :
                service_time_dict['friday'] = '?????????' + str(service_time.get(weekday='5').start_time) + '~' + str(service_time.get(weekday='5').end_time)
            if service_time.filter(weekday='6').exists() == True :
                service_time_dict['saturday'] = '?????????' + str(service_time.get(weekday='6').start_time) + '~' + str(service_time.get(weekday='6').end_time)
            if service_time.filter(weekday='0').exists() == True :
                service_time_dict['sunday'] = '?????????' + str(service_time.get(weekday='0').start_time) + '~' + str(service_time.get(weekday='0').end_time)
        theServant.serviceTime = service_time_dict

        servant_skill_dict={}
        theServantSkill = ServantSkill.objects.filter(servant=theServant)
        for x in range(len(theServantSkill)):
            servant_skill_dict['servant_skill'+str(x+1)] = theServantSkill[x].languageSkill
        theServant.Languageskill = servant_skill_dict

        transportation_list = []
        transportation = Transportation.objects.filter(servant=theServant)
        for x in range(len(transportation)):
            transportation_list.append({'city':transportation[x].cityarea.city,'area':transportation[x].cityarea.area,'transportation':transportation[x].price})
            transportation_dict[str(x+1)] = transportation_list[x]
        theServant.transportation = transportation_dict

        service_Item_dict = {}
        service_item = ServantServiceItemShip.objects.filter(servant=theServant)
        for x in range(len(service_item)):
            service_Item_dict['service_item'+str(x+1)] = service_item[x].service_item.name
        theServant.service_item = service_Item_dict

        markup_item_dict = {}
        markup_items = ServantMarkupItemPrice.objects.filter(servant=theServant)
        for x in range(len(markup_items)):
            markup_item_dict['markup_item'+str(x+1)] = markup_items[x].markup_item
            markup_item_dict['markup_pricePercent'+str(x+1)] = markup_items[x].pricePercent
        theServant.mark_up_item = markup_item_dict

        license_image_dict = {}
        licenseimages = ServantLicenseShipImage.objects.filter(servant=theServant)
        for x in range(len(licenseimages)):
            license_image_dict['license_name'+str(x+1)] = licenseimages[x].license
            license_image_dict['license_image'+str(x+1)] = licenseimages[x].image
        theServant.license_image = license_image_dict

        serializer = self.serializer_class(theServant)
        return Response(serializer.data)

class FillOrderViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Case.objects.all()
    serializer_class = serializers.CaseSerializer

    def post(self, request, format=None):
        case = Case()
        theUser = self.request.user
        caretype = request.data.get('caretype')
        Servant_id = request.data.get('Servant_id')
        cityarea_id = request.data.get('cityarea_id')
        timetype = request.data.get('timetype')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        weekday_choose = request.data.get('weekday_choose')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        apply_recipient_info = request.data.get('apply_recipient_info')
        recipient_nameSet = request.data.get('recipient_nameSet')
        recipient_genderSet = request.data.get('recipient_genderSet')
        recipient_weightSet = request.data.get('recipient_weightSet')
        recipient_ageSet = request.data.get('recipient_ageSet')
        infectious_disease = request.data.get('infectious_disease')
        addition_conditions_info = request.data.get('addition_conditions_info')
        markup_item_id = request.data.get('markup_item_id')
        theServant = Servant.objects.get(id=Servant_id) 
        if apply_recipient_info != None:
            recipient = Recipient.objects.get(user=theUser)
        else:
            recipient = Recipient()
            recipient.user = theUser
        recipient.name = recipient_nameSet
        recipient.gender = recipient_genderSet
        recipient.weight = recipient_weightSet
        recipient.age = recipient_ageSet
        disease_count = 0
        disease_list = []
        disease_str = ''
        for i in range(18):
            if request.data.get('disease_'+str(i+1))  != None:
                disease_count += 1

        for n in range(disease_count):
            disease_list.append({'disease_name':request.data.get('disease_'+str(n+1))})
            disease_str += disease_list[n]['disease_name'] + ','

        if infectious_disease != None :
            disease_str += infectious_disease
        recipient.disease = disease_str

        conditions_count = 0
        conditions_list = []
        conditions_str = ''
        for i in range(10):
            if request.data.get('conditions_'+str(i+1))  != None:
                conditions_count += 1

        for n in range(conditions_count):
            conditions_list.append({'conditions_name':request.data.get('conditions_'+str(n+1))})
            conditions_str += conditions_list[n]['conditions_name'] + ','
        if addition_conditions_info != None :
            conditions_str += addition_conditions_info
        recipient.conditions = conditions_str
        recipient.save()

        case.markup_item = ServantMarkupItemPrice.objects.filter(servant=theServant)[int(markup_item_id)-1]
        case.recipient = recipient
        case.disease = recipient.disease
        case.conditions = recipient.conditions
        case.start_time = datetime.time(int(start_time.split(':')[0]),int(start_time.split(':')[1]))
        case.end_time = datetime.time(int(end_time.split(':')[0]),int(end_time.split(':')[1]))
        case.start_date = datetime.date(int(start_date.split('-')[0]),int(start_date.split('-')[1]),int(start_date.split('-')[2]))
        case.end_date = datetime.date(int(end_date.split('-')[0]),int(end_date.split('-')[1]),int(end_date.split('-')[2]))
        case.cityarea = CityArea.objects.get(id=cityarea_id)
        case.save()

        serializer = self.serializer_class(case)
        return Response(serializer.data)