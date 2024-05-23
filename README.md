Framework: Django Rest Framework
Database: sqlite3(default)



Following are performed successfully.


1.Create and edit users (Admin)
    http://127.0.0.1:8000/admin/login/

2.Login and Logout(Any User)
    http://127.0.0.1:8000/api-auth/login/?next=/

3.List of users ang Groups
    "userlist": "http://127.0.0.1:8000/userlist/",
    "grouplist": "http://127.0.0.1:8000/grouplist/",
    
4.Create Group(Any User)
    "groupcreate": "http://127.0.0.1:8000/groupcreate/"
  
5.Delete Group(Any User)
    http://127.0.0.1:8000/group/<int>/

6.Add Group Members(Any User)
     http://127.0.0.1:8000/group/<int>/member/

7.Post Message in Group(Any User)
    http://127.0.0.1:8000/group/<int>/messages/

8.Like Messages(Any User)
    http://127.0.0.1:8000/group/<int>/messages/<int>


Here we are using default Django User Model


API test results are attached in attachment"test.png"