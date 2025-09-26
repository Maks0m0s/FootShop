# FootShop
Welcome to my Football Collective Staff Marketplace !
Here you can search by categories items you need, and add them to your own cart. You'll have 1 week to commit your order becouse then your item will be removed from the cart automatically. To commit payments, we use 'Stripe' service.
Finally, enjoy using my web and here you have end-points :

-- Header Buttons --
-
- ' ' : Home Page
- 'categories/' : Categories List
- 'about/' : About Us

-- Product Mechanics --
-
- 'categories/<int:pk>/' : Products by Category
- 'product/<int:category_id>/<int:pk>/' : Product Details
- 'product/<int:category_id>/<int:pk>/add-to-cart/' : Add to cart the product

-- Authorisation --
-
- 'auth/login/' : Login
- 'auth/register/' : Register
- 'auth/logout/' : Logout

-- Cart Mechanics --
-
- 'cart/' : Cart page
- 'cart/<int:pk>/remove/' : Remove product from the cart

-- Checkout Mechanics --
-
- "cart/checkout/get/" : Get checkout form
- "cart/checkout/post/" : Post checkout form

-- Payment Mechanic --
-
- "stripe/webhook/" : Brings to Stripe page to execute payment

-- Orders Mechanics --
-
- 'orders/' : Orders List
- 'orders/success_payment/' : Order placement and success page
- 'orders/<int:index>/<int:pk>/' : Order Details


For now that's all :)

To test payment method use next data :
-
Email : test@example.com

Code : 4242 4242 4242 4242

CVC : 567

Date : 12/34
