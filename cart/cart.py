# class Cart:
    # این تابع بررسی میکنه که ایا توی سشن سبد خرید هست یا نه اگه نیست درست کن
    # def init(self, request):
    #     self.session = request.session
    #     cart = self.session.get('cart')
    #     if not cart:
    #         cart = self.session['cart'] = {}
    #     self.cart = cart

    # این تابع یه ایتم یا یک محصول به سبدخرید اضافه میکنه
    # def add(self, product, quantity):
    #     product_id = str(product.id)
    #     if product_id not in self.cart:
    #         self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
    #     else:
    #         # if self.cart[product_id]['quantity'] < product.inventory:
    #         self.cart[product_id]['quantity'] += quantity
    #     self.save()
    #
    # # این تابع هروقت کاربر یه محصول یا همون ایتم از سبد خریدش کم کرد صدا زده میشه
    # def decrease(self, product):
    #     product_id = str(product.id)
    #     if self.cart[product_id]['quantity'] > 1:
    #         self.cart[product_id]['quantity'] -= 1
    #     self.save()
    #
    # # این تابع هروقت صدا زده بشه یه ایتم یا همون محصول از سبد خرید حذف میکنه
    # def remove(self, product):
    #     product_id = str(product.id)
    #     if product_id in self.cart:
    #         del self.cart[product_id]
    #     self.save()
    #
    # # این تابع کلا سبد خریدی که داخل سشن ایجاد شده پاک میکنه
    # def clear(self):
    #     del self.session['cart']
    #     self.save()
    #
    # def get_post_price(self):
    #     weight = sum(item['weight'] * item['quantity'] for item in self.cart.values())
    #     if weight < 1000:
    #         return 20000
    #     elif 1000 <= weight <= 2000:
    #         return 30000
    #     else:
    #         return 50000
    #
    # # این تابع جمع قیمت هر محصول یا ایتم در تعدادش ضرب میکنه
    # def get_total_price(self):
    #     price = sum(item['price'] * item['quantity'] for item in self.cart.values())
    #     return price
    #
    # # این تابع قیمت نهایی محصول با هزینه ارسالش باهم جمع میکنه
    # def get_final_price(self):
    #     return self.get_total_price() + self.get_post_price()
    #
    # # این تابع جمع تعداد هر ایتم در دیکشنری سبدخرید برمیداره و ریترن میکنه
    # def len(self):
    #     return sum(item['quantity'] for item in self.cart.values())
    #
    # # این تابع اول ایدی محصول برمیداره و از تمام محصولات اونیکه ایدیش این بوده برمیداره و اضافش میکنه به دیکشنری یا
    # # همون سبدخرید
    # def iter(self):
    #     product_ids = self.cart.keys()
    #     products = Product.objects.filter(id__in=product_ids)
    #     cart_dict = self.cart.copy()
    #     for product in products:
    #         cart_dict[str(product.id)]['product'] = product
    #     for item in cart_dict.values():
    #         item['total'] = item['price'] * item['quantity']
    #         yield item
    #
    # # این متد یعنی هروقت یک ابجکت ساخته شد و متد سیو صدا زده شد اون ابجکت سیو کن و اون تغییرات داخل سشن سیو کن
    # def save(self):
    #     self.session.modified = True