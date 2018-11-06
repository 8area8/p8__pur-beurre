"""Substitutes algorithm module."""


class FindSubstitutes:
    """Find substitute for a product."""

    @classmethod
    def run(cls, product):
        """Run function. Start the research."""
        categories = product.categories.all()
        categories = sorted(
            categories, key=lambda elem: elem.product_set.count())

        name = product.name
        nutriscore = product.nutriscore
        substitutes = cls._search_in_categories(name, nutriscore, categories)

        # substitutes = sorted(substitutes, key=lambda sub: ord(sub.nutriscore))
        for product in substitutes:
            product.nutriscore = f"nutriscore-{product.nutriscore}.png"
        return substitutes

    @classmethod
    def _search_in_categories(cls, name, nutriscore, categories):
        """Search in categories."""
        substitutes = []
        for category in categories:
            if substitutes and len(substitutes) == 6:
                return substitutes
            if category.product_set.count() < 1:
                continue

            products = category.product_set
            products = products.exclude(name=name)
            cls._filter_by_nutriscore(nutriscore, products, substitutes)
        return substitutes

    @classmethod
    def _filter_by_nutriscore(cls, nutriscore, products, substitutes):
        """Filter by nutriscore.

        Uses ord() python built in function to convert the letter to a number.
        """
        nutriscore = ord(nutriscore)
        products = sorted(products.all(),
                          key=lambda elem: ord(elem.nutriscore))

        for product in products:
            if substitutes and len(substitutes) == 6:
                return substitutes
            if nutriscore <= ord(product.nutriscore) != ord("a"):
                continue
            if product in substitutes:
                continue
            substitutes.append(product)


def disable_doubles(substitutes, user):
    """Add a double attribute to the substitutes."""
    u_substitutes = user.substitute_set.all()
    for substitute in substitutes:
        if u_substitutes.filter(substituted__name=substitute.name):
            substitute.double = True
        else:
            substitute.double = False
