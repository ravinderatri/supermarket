from django.shortcuts import render
from django.views import View
from .models import Product
from collections import Counter

class CheckoutView(View):
    def get(self, request):
        return render(request, 'form.html')

    def post(self, request):
        items = request.POST.get('items', '').upper()
        item_counts = Counter(items)
        total = 0
        errors = []
        processed_items = []

        if not items:
            return render(request, 'total.html', {
                'total': total,
                'items': items,
                'errors': ['No items provided. Please enter product letters like AAABBD.']
            })

        for item, count in item_counts.items():
            try:
                product = Product.objects.get(name=item)
                dq = product.discount_quantity
                dp = product.discount_price
                up = product.unit_price

                if dq and dp and count >= dq:
                    num_discounts = count // dq
                    remaining = count % dq
                    total += num_discounts * dp + remaining * up
                else:
                    total += count * up

                processed_items.append(f"{item} x {count}")
            except Product.DoesNotExist:
                errors.append(f"Item '{item}' is not recognized.")

        return render(request, 'total.html', {
            'total': total,
            'items': ', '.join(processed_items),
            'errors': errors
        })
