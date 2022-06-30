# careDjango
(linux  mac)  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
python3 app/manage.py makemigrations  
python3 app/manage.py migrate  
python3 app/manage.py initadmin  
python app/manage.py shell  
from modelCore.fakeData import fakeData  
fakeData()  
exit()  
python3 app/manage.py runserver  

  
(windows)  
python -m venv venv  
.\venv\Scripts\activate  
pip install -r requirements.txt  
python app/manage.py makemigrations  
python app/manage.py migrate  
python app/manage.py initadmin  
python app/manage.py shell  
from modelCore.fakeData import fakeData  
fakeData()  
exit()  
python app/manage.py runserver  
