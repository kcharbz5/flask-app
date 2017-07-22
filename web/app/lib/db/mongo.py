"""
"""
from werkzeug import generate_password_hash, check_password_hash
from pymongo import MongoClient
from geopy.geocoders import GoogleV3
from geopy.location import Location
from geopy.point import Point

class UserDatabase:
    
    def __init__(self):
        client = MongoClient('mongodb://mongo:27017')
        self.__db = client.database
        self.__locator = GoogleV3()
    
    def _is_user(self, username):
        cur = self.__db.users.find({'username' : username})

        if cur.count() >= 1:
            return True
        else:
            return False

    def add_user(self, username, password, **kwargs):
        
        if not self._is_user(username):
            street = kwargs.get('street', None)
            if street:
                loc = self.__locator.geocode(street)
            else:
                street = ''
                loc = Location(
                    point=Point(latitude=0, longitude=0), 
                    raw={'address_components': [{}, {}, {}, {}, {}, {}, {}, {'short_name':''}]}
                    )

            self.__db.users.insert_one(
                {
                    'username' : username,
                    'password' : generate_password_hash(password),
                    'email_address' : kwargs.get('email', ''),
                    'informations' : {
                        'first_name' : kwargs.get('first_name', ''),
                        'last_name' : kwargs.get('last_name', ''),
                        'address' : {
                            'street' : street,
                            'zip_code' : loc.raw['address_components'][7]['short_name'],
                            'coords' : [loc.latitude, loc.longitude]
                        }
                    }
                }
            )
        else:
            raise ValueError('The username \"' + username + '\" already exist')

    def check_user(self, username, password):
        if self._is_user(username):
            cur = self.__db.users.find({'username' : username})
            
            if check_password_hash(cur[0]['password'], password):
                return True
            else:
                raise ValueError('Invalid password')
                return False
        else:
            raise ValueError('The username \"' + username + '\" does not exist')    

    def remove_user(self, username):
        if self._is_user(username):
            self.__db.users.delete_one({'username' : username})
        else:
            raise ValueError('The username \"' + username + '\" does not exist')