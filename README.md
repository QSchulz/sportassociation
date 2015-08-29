#Website with content management for sport associations

##Requirements

- python 3.x (tested with 3.4)
- virtualenv

##Features
- You can create activities which can be attended. Each activity can have several categories of choices.
- You can write and send mails to your users.
- You can write and publish articles.
- You can write and publish important information on the front page.
- You can create elections so members can vote for the associations' staff.
- You can manage your equipment and the associated lendings.
- You can create different types of memberships.
- You can retrieve the membership history of users.
- You can protect the access to files and images by using Public/Protected/Admin File/Image.
- You can create different sports with their associated sessions, location and matches. You can also cancel sessions.
- Fees or subventions can be added to activities to follow their financial balance.
- Cash registers are used to help treasury. Every financial transaction (membership, participation to an activity, adding or taking petty cash) is archived so you can have an easy feedback on what happened recently and see when there is too much or few money in a cash register.
- You have additionnal fields for the user but it is still compatible with other modules (e.g.: forum)

##Warning
**NEVER** communicate or commit your localsettings.py, your database files nor uploaded contents. (Use this .gitignore)

**NEVER** use DEBUG set to True in production!

##Installation

```
mkdir python-workspace
virtualenv -p /usr/bin/python3 test
cd python-workspace
git clone https://github.com/QSchulz/sportassociation.git
source bin/activate
pip install -r sportassociation/requirements.txt
python sportassociation/manage.py migrate
python sportassociation/manage.py createsuperuser
```

Before running the server, you need to create and **fill** in the variables in your localsettings.

```
cp sportassociation/sportassociation/localsettings.template sportassociation/sportassociation/localsettings.py
```

You can test the application with:

```
python sportassociation/manage.py runserver
```

If you want to print member cards, you have to edit the function *print_cards* in users/admin,py and add a PNG template in static/static/member_card.png

####Author:
Quentin SCHULZ (quentin.schulz@utbm.fr)

#####Changelog

**v0.0a - 2015-08-23**
First alpha. Models and Django admin only.
