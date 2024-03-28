from decimal import Decimal
from django.utils import timezone
from rest_framework.fields import Field


class ClassPricePlanSerializer(Field):
    def calculate_taxed_amount(self, price, tax_rate):
        if not isinstance(price, Decimal) or not isinstance(tax_rate, Decimal):
            return None
        return str(round(price + (price * (tax_rate / Decimal("100.00")))))

    def get_price(self, prices, tax_rate):
        filtered_prices = []
        now = int(timezone.now().timestamp())
        for price in prices:
            if now < int(price.start_date.timestamp()):
                continue
            if price.end_date and now > int(price.end_date.timestamp()):
                continue
            filtered_prices.append(price)
        filtered_prices.sort(reverse=True, key=lambda x: x.start_date)
        if len(filtered_prices) > 0:
            p = filtered_prices[0]
            return {
                "name": p.name,
                "display_name": p.display_name,
                "pretax_price": str(p.price),
                "posttax_price": self.calculate_taxed_amount(p.price, tax_rate),
                "is_sale": p.is_limited_sale,
                "before_sale_pretax_price": (
                    str(p.before_sale_price)
                    if p.before_sale_price
                    else p.before_sale_price
                ),
                "before_sale_posttax_price": self.calculate_taxed_amount(
                    p.before_sale_price, tax_rate
                ),
                "start_date": p.start_date,
                "end_date": p.end_date,
            }
        return {}

    def to_representation(self, value):
        cs = value.class_service
        return {
            "id": value.id,
            "slug": value.slug,
            "title": value.title,
            "display_title": value.display_title,
            "length": cs.length,
            "length_unit": cs.get_length_unit_display(),
            "quantity": cs.quantity,
            "quantity_unit": cs.get_quantity_unit_display(),
            "max_num": cs.max_num,
            "is_native": cs.is_native,
            "is_online": cs.is_online,
            "is_inperson": cs.is_inperson,
            "has_onlinenotes": cs.has_onlinenotes,
            "bookable_online": cs.bookable_online,
            "price_info": self.get_price(cs.prices.all(), cs.tax_rate.rate),
        }
