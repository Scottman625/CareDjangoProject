import csv
import os
import datetime 
from datetime import timedelta
from .models import  User, MarkupItem, License, Servant, ServantMarkupItemPrice
from .models import ServantSkill,UserLicenseShipImage, ServantLicenseShipImage,  Recipient, ServiceItem,  CityArea, Transportation, Case,OrderState, Order, OrderReview , CaseServiceItemShip 
from .models import City, CityArea, ServantWeekdayTime, ServantServiceItemShip,Message,SystemMessage

def importCityCounty():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'county.csv')

    file = open(file_path)
    reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(reader):
        if index != 0:
            if City.objects.filter(name=row[0]).count()==0:
                city = City()
                city.name = row[0]
                city.save()
            else:
                city = City.objects.get(name=row[0])

            county_name = row[2].replace(row[0],'')
            county = CityArea()
            county.city = city
            county.area = county_name
            county.save()
            print(city.name + " " + county.area)
            

def fakeData():
    user = User()
    user.name = 'user01'
    user.phone = '0915323131'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'user02'
    user.phone = '0985463816'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'user03'
    user.phone = '0985463888'
    user.is_active = True
    user.is_staff =  False
    user.is_servant = True
    user.save()

    user = User()
    user.name = 'user04'
    user.phone = '0985490816'
    user.is_active = True
    user.is_staff =  False
    user.is_servant = True
    user.save()

    user = User()
    user.name = 'user05'
    user.phone = '0985478816'
    user.is_active = True
    user.is_staff =  False
    user.is_servant = True
    user.save()


    user = User.objects.all()[0]

    item = MarkupItem()
    item.name = '?????????'
    item.save()

    item = MarkupItem()
    item.name = '???????????????'
    item.save()

    item = MarkupItem()
    item.name = '???????????? 70 ??????'
    item.save()

    item = MarkupItem()
    item.name = '???????????? 90 ??????'
    item.save()


    license = License()
    license.name = '???????????????'
    license.save()

    license = License()
    license.name = '???????????????'
    license.save()

    license = License()
    license.name = '???????????????'
    license.save()

    license = License()
    license.name = 'COVID-19 ????????????????????? /n????????????????????????????????????????????????????????????????????????'
    license.save()

    license = License()
    license.name = '??????????????????-??????????????????????????? /n????????????????????????????????????????????????????????????????????????'
    license.save()

    license = License()
    license.name = '???????????????????????????B??????????????? & ?????? X ??????/n????????????????????????????????????????????????????????????????????????'
    license.save()
    
    license = License()
    license.name = '?????????????????????'
    license.save()
    
    license = License()
    license.name = '????????????????????????'
    license.save()
    
    license = License()
    license.name = '???????????????'
    license.save()
    
    license = License()
    license.name = '????????????????????????'
    license.save()

    servant = Servant()
    servant.user = User.objects.get(id=4)
    servant.gender = 'M'
    servant.home_hourly_wage = 250
    servant.home_halfday_wage = 1500
    servant.home_oneday_wage = 3300
    servant.hospital_hourly_wage = 270
    servant.hospital_halfday_wage = 1600
    servant.hospital_oneday_wage = 3400
    servant.info = 'test'
    servant.is_home = True
    servant.save()

    servant = Servant()
    servant.user = User.objects.get(id=5)
    servant.gender = 'M'
    servant.home_hourly_wage = 240
    servant.home_halfday_wage = 1450
    servant.home_oneday_wage = 3000
    servant.hospital_hourly_wage = 250
    servant.hospital_halfday_wage = 1550
    servant.hospital_oneday_wage = 3300
    servant.info = 'test'
    servant.is_hospital = True
    servant.save()

    servant = Servant()
    servant.user = User.objects.get(id=6)
    servant.gender = 'F'
    servant.home_hourly_wage = 330
    servant.home_halfday_wage = 1800
    servant.home_oneday_wage = 3700
    servant.hospital_hourly_wage = 350
    servant.hospital_halfday_wage = 1950
    servant.hospital_oneday_wage = 4000
    servant.info = 'test'
    servant.is_home = True
    servant.is_hospital = True
    servant.is_alltime_service = True
    servant.save()

 

    markup_price = ServantMarkupItemPrice()
    markup_price.servant = Servant.objects.get(id=1)
    markup_price.markup_item = MarkupItem.objects.get(id=2)
    markup_price.pricePercent = 1.25
    markup_price.save()

    markup_price = ServantMarkupItemPrice()
    markup_price.servant = Servant.objects.get(id=2)
    markup_price.markup_item = MarkupItem.objects.get(id=4)
    markup_price.pricePercent = 1.45
    markup_price.save()

    markup_price = ServantMarkupItemPrice()
    markup_price.servant = Servant.objects.get(id=3)
    markup_price.markup_item = MarkupItem.objects.get(id=1)
    markup_price.pricePercent = 1.3
    markup_price.save()


    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=2)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=2)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=2)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=3)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=3)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=3)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=4)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=4)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=4)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=5)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=5)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=5)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=6)
    userlicense.license = License.objects.get(id=1)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=6)
    userlicense.license = License.objects.get(id=2)
    userlicense.save()

    userlicense = UserLicenseShipImage()
    userlicense.user = User.objects.get(id=6)
    userlicense.license = License.objects.get(id=3)
    userlicense.save()


    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=4)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=7)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=8)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=1)
    servantlicense.license = License.objects.get(id=9)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=2)
    servantlicense.license = License.objects.get(id=4)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=2)
    servantlicense.license = License.objects.get(id=7)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=3)
    servantlicense.license = License.objects.get(id=6)
    servantlicense.save()

    servantlicense = ServantLicenseShipImage()
    servantlicense.servant = Servant.objects.get(id=3)
    servantlicense.license = License.objects.get(id=8)
    servantlicense.save()

    recipient = Recipient()
    recipient.name = 'recipient01'
    recipient.user = User.objects.get(id=2)
    recipient.gender = 'M'
    recipient.age = 65
    recipient.weight = 70
    recipient.disease = '???'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient02'
    recipient.user = User.objects.get(id=2)
    recipient.gender = 'M'
    recipient.age = 65
    recipient.weight = 70
    recipient.disease = '???'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient03'
    recipient.user = User.objects.get(id=2)
    recipient.gender = 'M'
    recipient.age = 80
    recipient.weight = 67
    recipient.disease = '?????????'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient04'
    recipient.user = User.objects.get(id=3)
    recipient.gender = 'F'
    recipient.age = 70
    recipient.weight = 55
    recipient.disease = '?????????'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient05'
    recipient.user = User.objects.get(id=3)
    recipient.gender = 'M'
    recipient.age = 68
    recipient.weight = 95
    recipient.disease = '?????????'
    recipient.disease_info = 'test'
    recipient.save()

    recipient = Recipient()
    recipient.name = 'recipient06'
    recipient.user = User.objects.get(id=3)
    recipient.gender = 'F'
    recipient.age = 72
    recipient.weight = 60
    recipient.disease = '????????????'
    recipient.disease_info = 'test'
    recipient.save()

    serviceitem = ServiceItem()
    serviceitem.name = '????????????'
    serviceitem.info = '??????????????????????????????????????????????????????'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '????????????'
    serviceitem.info = '????????????????????????'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '????????????'
    serviceitem.info = '?????????????????????????????????????????????'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '????????????'
    serviceitem.info = '???????????????'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '????????????'
    serviceitem.info = '????????????????????????????????????'
    serviceitem.save()
    
    serviceitem = ServiceItem()
    serviceitem.name = '????????????'
    serviceitem.save()

    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=1)
    transportation.cityarea = CityArea.objects.get(id=1)
    transportation.price = 500
    transportation.save()
 
    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=2)
    transportation.cityarea = CityArea.objects.get(id=5)
    transportation.price = 500
    transportation.save()

    transportation = Transportation()
    transportation.servant = Servant.objects.get(id=3)
    transportation.cityarea = CityArea.objects.get(id=7)
    transportation.price = 500
    transportation.save()

    case = Case()
    case.recipient = Recipient.objects.get(id=2)
    case.servant = Servant.objects.get(id=1)
    case.cityarea = Transportation.objects.filter(servant=Servant.objects.get(id=1)).order_by('id')[0].cityarea
    case.markup_item = ServantMarkupItemPrice.objects.filter(servant=Servant.objects.get(id=1)).order_by('id')[0]
    case.start_date = '2022-06-22'
    case.end_date = '2022-07-12'
    case.start_time = datetime.time(10,0,0)
    case.end_time = datetime.time(22,0,0)
    case.is_taken = True
    case.care_type = '????????????'
    case.save()

    case = Case()
    case.recipient = Recipient.objects.get(id=3)
    case.servant = Servant.objects.get(id=2)
    case.cityarea = Transportation.objects.filter(servant=Servant.objects.get(id=2)).order_by('id')[0].cityarea
    case.markup_item = ServantMarkupItemPrice.objects.filter(servant=Servant.objects.get(id=2)).order_by('id')[0]
    case.start_date = '2022-07-02'
    case.end_date = '2022-07-15'
    case.start_time = datetime.time(12,30,0)
    case.end_time = datetime.time(20,30,0)
    case.consult_all_servant = True
    case.care_type = '????????????'
    case.save()
    
    case = Case()
    case.recipient = Recipient.objects.get(id=5)
    case.specify_servant_1 = Servant.objects.get(id=2)
    case.specify_servant_2 = Servant.objects.get(id=3)
    case.cityarea = Transportation.objects.filter(servant=Servant.objects.get(id=3)).order_by('id')[0].cityarea
    case.markup_item = ServantMarkupItemPrice.objects.filter(servant=Servant.objects.get(id=3)).order_by('id')[0]
    case.start_date = '2022-06-25'
    case.end_date = '2022-07-25'
    case.start_time = datetime.time(9,0,0)
    case.end_time = datetime.time(17,0,0)
    case.care_type = '????????????'
    case.is_alltime_service = True
    case.save()

    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=1)
    caseitemship.service_item = ServiceItem.objects.get(id=2)
    caseitemship.save()
    
    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=1)
    caseitemship.service_item = ServiceItem.objects.get(id=3)
    caseitemship.save()
    
    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=2)
    caseitemship.service_item = ServiceItem.objects.get(id=1)
    caseitemship.save()
    
    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=2)
    caseitemship.service_item = ServiceItem.objects.get(id=5)
    caseitemship.save()
        
    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=3)
    caseitemship.service_item = ServiceItem.objects.get(id=2)
    caseitemship.save()

    caseitemship = CaseServiceItemShip()
    caseitemship.case = Case.objects.get(id=3)
    caseitemship.service_item = ServiceItem.objects.get(id=6)
    caseitemship.save()

    orderstate = OrderState()
    orderstate.name = '?????????'
    orderstate.save()

    orderstate = OrderState()
    orderstate.name = '?????????'
    orderstate.save()

    orderstate = OrderState()
    orderstate.name = '?????????'
    orderstate.save()

    order = Order()
    order.case = Case.objects.get(id=1)
    order.state = OrderState.objects.get(id=1)
    order.info = 'test'
    order.save()

    order = Order()
    order.case = Case.objects.get(id=2)
    order.state = OrderState.objects.get(id=3)
    order.info = 'test'
    order.save()

    order = Order()
    order.case = Case.objects.get(id=3)
    order.state = OrderState.objects.get(id=1)
    order.info = 'test'
    order.save()

    orderreview = OrderReview()
    orderreview.order = Order.objects.get(id=1)
    orderreview.user_score = 5
    orderreview.user_is_rated = True
    orderreview.user_content = 'Test'
    orderreview.servant_score = 5
    orderreview.servant_is_rated = True
    orderreview.servant_content = 'Test'
    orderreview.save()
    
    orderreview = OrderReview()
    orderreview.order = Order.objects.get(id=2)
    orderreview.user_score = 4
    orderreview.user_is_rated = True
    orderreview.user_content = 'Test'
    orderreview.servant_score = 5
    orderreview.servant_is_rated = True
    orderreview.servant_content = 'Test'
    orderreview.save()
    
    orderreview = OrderReview()
    orderreview.order = Order.objects.get(id=3)
    orderreview.save()


def importCityArea():
    city = City()
    city.name = '?????????'
    city.save()

    city = City()
    city.name = '?????????'
    city.save()

    city = City()
    city.name = '?????????'
    city.save()

    city = City()
    city.name = '?????????'
    city.save()

    city = City()
    city.name = '?????????'
    city.save()

    city = City()
    city.name = '?????????'
    city.save()

    city = City()
    city.name = '?????????'
    city.save()

    city = City()
    city.name = '?????????'
    city.save()

    city = City()
    city.name = '?????????'
    city.save()

    city = City()
    city.name = '?????????'
    city.save()


    cityarea = CityArea()
    cityarea.city = City.objects.get(id=1)
    cityarea.area = '??????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=2)
    cityarea.area = '??????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=2)
    cityarea.area = '?????????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=3)
    cityarea.area = '??????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=4)
    cityarea.area = '??????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=5)
    cityarea.area = '??????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=6)
    cityarea.area = '??????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=7)
    cityarea.area = '??????'
    cityarea.save()

    cityarea = CityArea()
    cityarea.city = City.objects.get(id=7)
    cityarea.area = '?????????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=7)
    cityarea.area = '?????????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=8)
    cityarea.area = '??????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=8)
    cityarea.area = '?????????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=9)
    cityarea.area = '??????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=9)
    cityarea.area = '?????????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=9)
    cityarea.area = '??????'
    cityarea.save()
    
    cityarea = CityArea()
    cityarea.city = City.objects.get(id=10)
    cityarea.area = '??????'
    cityarea.save()