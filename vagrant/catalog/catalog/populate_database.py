"""Populate the item catalog database some inital content.

This application stores animals of various categories. Six categories are
created and some animals are created in each category.

This script should only be run on an empty database.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

def populate_database():
    """Populate the item catalog database some inital content."""
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    engine = create_engine('sqlite:///itemcatalog.db')
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()

    # Create the six categories animals fall in to.
    category1 = Category(name="Mammals")
    session.add(category1)
    session.commit()

    category2 = Category(name="Birds")
    session.add(category2)
    session.commit()

    category3 = Category(name="Fish")
    session.add(category3)
    session.commit()

    category4 = Category(name="Reptiles")
    session.add(category4)
    session.commit()

    category5 = Category(name="Amphibians")
    session.add(category5)
    session.commit()

    category6 = Category(name="Arthropods")
    session.add(category6)
    session.commit()

    # Create a dummy user for these intial items
    user1 = User(name="Bob Fossil", email="b.fossil@zooniverse.com")
    session.add(user1)
    session.commit()

    # Create some mammals
    item1 = Item(
        user=user1,
        category=category1,
        name="Polar Bear",
        description=(
            "The polar bear is a carnivorous bear whose native range lies "
            "largely within the Arctic Circle, encompassing the Arctic Ocean, "
            "its surrounding seas and surrounding land masses. It is a large "
            "bear, approximately the same size as the omnivorous Kodiak bear."
        )
    )
    session.add(item1)
    session.commit()

    item2 = Item(
        user=user1,
        category=category1,
        name="Elephant",
        description=(
            "Elephants are large mammals of the family Elephantidae and the "
            "order Proboscidea. Two species are traditionally recognised, the "
            "African elephant and the Asian elephant, although some evidence "
            "suggests that African bush elephants and African forest elephants "
            "are separate species."
        )
    )
    session.add(item2)
    session.commit()

    # Create some Birds
    item3 = Item(
        user=user1,
        category=category2,
        name="Kingfisher",
        description=(
            "Kingfishers are a group of small to medium-sized brightly colored "
            "birds in the order Coraciiformes. There are roughly 90 species of "
            "kingfisher. All have large heads, long, sharp, pointed bills, "
            "short legs, and stubby tails. Most species have bright plumage "
            "with little differences between the sexes."
        )
    )
    session.add(item3)
    session.commit()

    item4 = Item(
        user=user1,
        category=category2,
        name="Blue Tit",
        description=(
            "The Eurasian blue tit is a small passerine bird in the tit family "
            "Paridae. The bird is easily recognisable by its blue and yellow "
            "plumage, but various authorities dispute their scientific "
            "classification."
        )
    )
    session.add(item4)
    session.commit()

    # Create some fish
    item5 = Item(
        user=user1,
        category=category3,
        name="Swordfish",
        description=(
            "Swordfish, also known as broadbills in some countries, are large, "
            "highly migratory, predatory fish characterized by a long, flat "
            "bill. They are a popular sport fish of the billfish category, "
            "though elusive. Swordfish are elongated, round-bodied, and lose "
            "all teeth and scales by adulthood."
        )
    )
    session.add(item5)
    session.commit()

    item6 = Item(
        user=user1,
        category=category3,
        name="Whale Shark",
        description=(
            "The whale shark is a slow-moving filter feeding shark and the "
            "largest known extant fish species. The largest confirmed "
            "individual had a length of 12.65 m (41.50 ft) and a weight of "
            "about 21.5 metric tons (47,000 lb), and unconfirmed reports of "
            "considerably larger whale sharks exist. Claims of individuals "
            "over 14 m (46 ft) long and weighing at least 30 metric tons "
            "(66,000 lb) are not uncommon."
        )
    )
    session.add(item6)
    session.commit()

    # Create some reptiles
    item7 = Item(
        user=user1,
        category=category4,
        name="Saltwater Crocodile",
        description=(
            "The saltwater crocodile  is the largest of all living reptiles, "
            "as well as the largest terrestrial and riparian predator in the "
            "world. The males of this species can reach sizes up to 6.3 m "
            "(20.7 ft) and weigh up to 1,360 kg (3,000 lb). However, an adult "
            "male saltwater crocodile is generally between 4.3 and 5.2 m (14 "
            "and 17 ft) in length and weighs 400 to 1,000 kg (880-2,200 lb), "
            "rarely growing larger."
        )
    )
    session.add(item7)
    session.commit()

    item8 = Item(
        user=user1,
        category=category4,
        name="Burmese Python",
        description=(
            "The Burmese python is one of the five largest species of snakes "
            "in the world (about the third-largest as measured either by "
            "length or weight). It is native to a large variation of tropic "
            "and subtropic areas of South and Southeast Asia. Until 2009, it "
            "was considered a subspecies of Python molurus, but now is "
            "recognized as belonging to a distinct species."
        )
    )
    session.add(item8)
    session.commit()

    # Create some amphibians
    item9 = Item(
        user=user1,
        category=category5,
        name="Golden Poison Frog",
        description=(
            "The golden poison frog, also known as the golden frog, golden "
            "poison arrow frog, or golden dart frog, is a poison dart frog "
            "endemic to the Pacific coast of Colombia. Its optimal habitat is "
            "the rainforest with high rain rates (5 m or more per year), "
            "altitudes between 100 and 200 m, temperatures of at least 26C, "
            "and relative humidity of 80-90%."
        )
    )
    session.add(item9)
    session.commit()

    item10 = Item(
        user=user1,
        category=category5,
        name="Glass Frog",
        description=(
            "The glass frogs (or glassfrogs) are frogs of the amphibian family "
            "Centrolenidae (order Anura). While the general background "
            "coloration of most glass frogs is primarily lime green, the "
            "abdominal skin of some members of this family is translucent. The "
            "internal viscera, including the heart, liver, and "
            "gastrointestinal tract, are visible through the skin, hence the "
            "common name."
        )
    )
    session.add(item10)
    session.commit()

    # Create some arthropods
    item11 = Item(
        user=user1,
        category=category6,
        name="Fire Ant",
        description=(
            "Fire ant is the common name for several species of ants in the "
            "genus Solenopsis. They are however only a minority in the genus, "
            "which includes over 200 species of Solenopsis worldwide."
        )
    )
    session.add(item11)
    session.commit()

    item12 = Item(
        user=user1,
        category=category6,
        name="Swallowtail Butterfly",
        description=(
            "Swallowtail butterflies are large, colorful butterflies in the "
            "family Papilionidae, and include over 550 species. Though the "
            "majority are tropical, members of the family inhabit every "
            "continent except Antarctica."
        )
    )
    session.add(item12)
    session.commit()

    session.close()

    print "Populated database with some animals..."


if __name__ == '__main__':
    populate_database()
