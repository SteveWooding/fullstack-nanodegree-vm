"""Populate the item catalog database some initial content.

This application stores animals of various categories. Six categories are
created and some animals are created in each category.

This script should only be run on an empty database.
"""
from catalog.database_setup import User, Category, Item
from catalog.connect_to_database import connect_to_database

def populate_database():
    """Populate the item catalog database some initial content."""
    session = connect_to_database()

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

    # Create a dummy user for these initial items
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
        ),
        quantity=3,
        image_url="https://upload.wikimedia.org/wikipedia/commons/6/66/Polar_Bear_-_Alaska_(cropped).jpg"
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
        ),
        quantity=4,
        image_url="http://res.freestockphotos.biz/pictures/10/10004-an-elephant-in-the-wild-pv.jpg"

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
        ),
        quantity=2,
        image_url="https://upload.wikimedia.org/wikipedia/commons/d/de/Common_Kingfisher_(Alcedo_atthis_taprobana)_-_Male_-_Flickr_-_Lip_Kee.jpg"
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
        ),
        quantity=7,
        image_url="https://upload.wikimedia.org/wikipedia/commons/6/65/Blue_Tit_-_flickr.jpg"
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
        ),
        quantity=4,
        image_url="https://upload.wikimedia.org/wikipedia/commons/f/f6/Xiphias_gladius2.jpg"
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
        ),
        quantity=1,
        image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Male_whale_shark_at_Georgia_Aquarium_crop.jpg/1024px-Male_whale_shark_at_Georgia_Aquarium_crop.jpg"
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
        ),
        quantity=2,
        image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Saltwater_crocodile.jpg/640px-Saltwater_crocodile.jpg"
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
        ),
        quantity=2,
        image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Burmese_Python_02.jpg/640px-Burmese_Python_02.jpg"
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
        ),
        quantity=2,
        image_url="https://upload.wikimedia.org/wikipedia/commons/9/9a/Phyllobates_terribilis_climbing_on_leaves.png"
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
        ),
        quantity=4,
        image_url="https://c1.staticflickr.com/7/6143/5991036083_b2a7f8d894_b.jpg"
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
        ),
        quantity=200,
        image_url="https://c2.staticflickr.com/4/3614/3469703353_9020c24f36.jpg"
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
        ),
        quantity=5,
        image_url="https://upload.wikimedia.org/wikipedia/commons/f/fe/Swallowtail_Butterfly_(Papilio_machaon)_-_geograph.org.uk_-_854088.jpg"
    )
    session.add(item12)
    session.commit()

    session.close()

    print "Populated database with some animals..."


if __name__ == '__main__':
    populate_database()
