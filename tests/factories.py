
import random
import string

import factory

from models  import Author


def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for x in range(length))


class AuthorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Author

    name = factory.LazyAttribute(lambda t: random_string(25))
    age = factory.LazyAttribute(lambda a: random.randrange(17,104))