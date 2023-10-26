from decimal import Decimal

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from .models import ProductService, ProductServicePrice


def update_price_summary(id):
    """Function to update the related Product Service price summary field after
    a change to the Product Service Price model
    - For products and classes there should only be one current price
    - For experiences there is a range of prices available depending on various conditions
    """
    product_service = ProductService.objects.get(pk=id)
    prices_query = product_service.prices.all()
    now = timezone.now()
    valid_prices = []
    for p in prices_query:
        # Check to see that price falls within valid date range
        if p.start_date <= now and not p.end_date:
            valid_prices.append(p)
        elif p.start_date <= now and p.end_date > now:
            valid_prices.append(p)
    # If no valid prices create warning string
    if not valid_prices:
        product_service.price_summary = "** WARNING: No valid price **"
        product_service.save()
        return

    # check ProductService is an experience - which can have a range of various prices
    if product_service.ptype == "experience":
        if len(valid_prices) == 1:
            product_service.price_summary = f"{str(valid_prices[0].price)}"
        else:
            mi = min(valid_prices, key=lambda x: x.price)
            mx = max(valid_prices, key=lambda x: x.price)
            product_service.price_summary = f"{str(mi.price)} ~ {str(mx.price)}"
        product_service.save()
        return
    else:
        # Product_service is not experience so should only have one current price or indicate
        # Current price with sale price
        if len(valid_prices) == 1:
            product_service.price_summary = f"{str(valid_prices[0].price)}"
        else:
            product_service.price_summary = "Still in dev"
            open_ended = []
            sale_close_ended = []
            sorted_valid_prices = sorted(
                valid_prices, reverse=True, key=lambda p: p.start_date
            )
            for priceline in sorted_valid_prices:
                # Split prices into open ended and on sale close ended (and sale without end date excluded)
                if priceline.is_limited_sale and priceline.end_date:
                    sale_close_ended.append(priceline)
                else:
                    open_ended.append(priceline)

            if len(sale_close_ended) and len(open_ended):
                s = f"SALE: ({open_ended[0].price}) -> {sale_close_ended[0].price}"
                product_service.price_summary = s
                # Check it sales price exists along with open standart price, if so build string with current price

            elif len(open_ended) and not len(sale_close_ended):
                s = f"{open_ended[0].price}"
                product_service.price_summary = s

            elif len(sale_close_ended) and not len(open_ended):
                # This is an error state, someone forgot to keep the long term price
                s = f"** WARNING: No base price, please add one"
                product_service.price_summary = s

            else:
                # SHould not be here so warn users
                s = f"** WARNING: Error with pricing"
                product_service.price_summary = s

        product_service.save()


@receiver(post_save, sender=ProductServicePrice)
def update_price_summary_on_save(sender, instance, *args, **kwargs):
    update_price_summary(instance.product_service.id)


@receiver(post_delete, sender=ProductServicePrice)
def update_price_summary_on_delete(sender, instance, *args, **kwargs):
    update_price_summary(instance.product_service.id)
