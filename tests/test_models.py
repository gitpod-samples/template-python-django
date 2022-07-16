from django.test import TestCase
from todo_app.models import ToDoItem, ToDoList
from django.utils import timezone
from dateutil import tz

# Create your tests here.

class TestModels(TestCase):

    def test_model_str(self):
        israel_tz = tz.gettz('Asia / Jerusalem')  
        td_list = ToDoList.objects.create(title="Baraks TODO list")
        td_item = ToDoItem.objects.create(title = "Pick up the kids", todo_list = td_list, due_date=timezone.datetime(year=2022,month=7,day=17,hour=16,tzinfo=israel_tz))
        td_item2 = ToDoItem.objects.create(title = "Make dinner", todo_list = td_list)
        self.assertNotEqual(str(td_item), str(td_item2))
        

        
