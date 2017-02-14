# techblog
A tech blog based on Flask and python

### Getting Started
I suggest you use virtualenv to create isolated Python environments. About how to install virtualenv, please refer to [virtualenv](https://virtualenv.pypa.io/en/stable/installation/). 

After you install virtualenv, create a new isolated python environment and activate it:
```
virtualenv venv
source ./venv/bin/activate
```

Install all the requirements:
```
pip install -r requirements.txt
```

Create the database you are going to use, for example *blog*,  and set the database connection url to the system environment variable **DEV_DATABASE_URL**. If you decide to use mysql on linux, you can set the url as follow:
```
export DEV_DATABASE_URL=mysql://root:123@localhost/blog
```

And then create all the necessary tables:
```
python manage.py db init
python manage.py db migrate
pytohn manage.py db upgrade
```

Initialize tags and users:
```
python manage.py shell
from app.models import Tag, User
from app import db
Tag.init_tags()
user = User(username=${username}, email=${password}, password=${password})
db.session.add(user)
db.session.commit()
```
