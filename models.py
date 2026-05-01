from sqlalchemy import create_engine, Integer, Boolean, String, Column,Float,ForeignKey, VARCHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType


# DB connection created
db = create_engine("sqlite:///banco.db") #inside the () is the name of DB

# Base of DB created
Base = declarative_base()

# Create the classes/DB tables
class User(Base):
    __tablename__ = "users" #Table name

    #Columns configs
    id = Column("id", Integer, primary_key=True, autoincrement = True)
    name = Column("name", String)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    # Constructor method in Python class.
    def __init__(self, name, email, password, active= True, admin= False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin



class Order(Base):
    __tablename__ = "order"

    id = Column("id", Integer, primary_key= True, autoincrement = True)
    status = Column("status", String) #Related to the tuples, just the three choices are possible
    user = Column("user", ForeignKey("users.id")) #Reference to the users table > each order belongs to an ID
    price = Column("price", Float)
    #items = Column("items", ForeignKey("order_items.id")) #Reference to the orders_items table > 1:N > each user could have many orders


    def __init__(self, user, status="PENDING", price=0):
        self.user = user
        self.status = status
        self.price = price
        #self.items = items


class OrdersItem(Base):
    __tablename__ = "order_item"

    id = Column("id", Integer, primary_key= True, autoincrement = True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String) #Could use ChoiceType
    size = Column("size", String) #Could use ChoiceType
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("order.id")) # Reference to orders table

    def __init__(self, quantity, flavor, size, unit_price, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order

# Create of the DB

