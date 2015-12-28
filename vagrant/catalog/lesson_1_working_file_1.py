from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('postgresql:///restaurantmenu')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


# myFirstRestaurant = Restaurant(name = "Pizza Palace")
# session.add(myFirstRestaurant)
# session.commit()
# session.query(Restaurant).all()
#
# cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella",
#                        course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
# session.add(cheesepizza)
# session.commit()
#
# allResults = session.query(MenuItem).all()
# print(allResults)
#
# firstResult = session.query(Restaurant).first()
# print(firstResult.name)


#query used to find the veggie burger that is at Urban Burger
# veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
# for veggieBurger in veggieBurgers:
#     print(veggieBurger.id)
#     print(veggieBurger.price)
#     print(veggieBurger.restaurant.name)
#     print("\n")
#
# #found that Urban Burger's id is 1 based on prior query
# UrbanVeggieBurger = session.query(MenuItem).filter_by(id=1).one()
# print(UrbanVeggieBurger.price)
#
# #change Urban Burger's veggie burger's price to $2.99.
# UrbanVeggieBurger.price = "$2.99"
# session.add(UrbanVeggieBurger)
# session.commit()
# print(UrbanVeggieBurger.price)
#
# #change the price of all veggie burgers in the database
# for veggieBurger in veggieBurgers:
#     if veggieBurger.price != "$2.99":
#         veggieBurger.price = "$2.99"
#         session.add(veggieBurger)
#         session.commit()
#
# for veggieBurger in veggieBurgers:
#     print(veggieBurger.id)
#     print(veggieBurger.price)
#     print(veggieBurger.restaurant.name)
#     print("\n")


# desserts = session.query(MenuItem).filter_by(course = 'Dessert')
# for each in desserts:
#     print(each.id)
#     print(each.name)
#     print(each.restaurant.name)
#     print("\n")
#
# spinach = session.query(MenuItem).filter_by(id=43).one()
# print(spinach.restaurant.name)
# session.delete(spinach)
# session.commit()
# print(spinach)
