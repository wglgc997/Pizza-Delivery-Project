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
    cep = Column("cep", VARCHAR)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    # Constructor method in Python class.
    def __init__(self, name, email, password, cep, active= True, admin= False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin
        self.cep = cep



class Order(Base):
    __tablename__ = "orders"

    #List of tuples OR tuple of tuples
    # ORDERS_STATUS_CHOICES = (
    # ("PENDING", "PENDING"),
    # ("CANCELED", "CANCELED"),
    # ("FINISHED", "FINISHED")
    #
    # )

    id = Column("id", Integer, primary_key= True, autoincrement = True)
    status = Column("status", String) #Related to the tuples, just the three choices are possible
    user = Column("user", ForeignKey("users.id")) #Reference to the users table
    price = Column("price", Float)
    items = Column("items", ForeignKey("order_items.id")) #Reference to the order_items table


    def __init__(self, user, items, status="PENDING", price=0):
        self.user = user
        self.status = status
        self.price = price
        self.items = items


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key= True, autoincrement = True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String) #Could use ChoiceType
    size = Column("size", String) #Could use ChoiceType
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id")) # Reference to orders table

    def __init__(self, quantity, flavor, size, unit_price, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order

# Create of the DB

