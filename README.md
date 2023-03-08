# webstore
E-commerce app made in django and django rest framework with bootstrap frontend.

![image](https://user-images.githubusercontent.com/66256669/222742736-ba3179c6-b803-4b60-b948-ce88d62fc78f.png)

## Live website

[LINK](https://webstore-deploy-production.up.railway.app/)

## How to run

Enter directory in which `docker-file.yml` is located and type in command `docker compose up`. Website will run on port 8000.

## API endpoints

### /api/token/
#### POST
Returns refresh and access token.

Success code: ```200```

Error code: 


``401`` - unauthorized

Example request:

```
{
   "username":"admin",
   "password":"admin"
}
```

Example response:

```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjIwMjY3NCwiaWF0IjoxNjczNjEwNjc0LCJqdGkiOiJkMjg4MmVmODA5Yzk0NGRkYmUxNTQwOWEwYzhjYTE0NSIsInVzZXJfaWQiOjJ9.yyGHVqFi1EJDEfcL4VyaF7uhfVdHX4xf7jglsGZ3YIA",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjczNjEwOTc0LCJpYXQiOjE2NzM2MTA2NzQsImp0aSI6IjUwZWFlYmYwZTVlYjQ3ZGU4ZTZhYjE3ZGFjMmVkMWYxIiwidXNlcl9pZCI6Mn0.PpngohnD7247WFIHAeKMjbq593YAvqSQRc26QyDHlQQ"
}
```

### /api/token/refresh/
#### POST
Refreshes user token

Success code: ```200```

Error code: 

``401`` - unauthorized

Example input:

```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjIwMzE5NiwiaWF0IjoxNjczNjExMTk2LCJqdGkiOiI1OWIzM2NmNjc4MzA0MTgzYTgyNjg0YjQzZDc5ZTBmOSIsInVzZXJfaWQiOjJ9.Zrl09OfHO_ipqgIrrmcb5D7L8VT4YZUmPQBMrX-0Y0E"
}
```

Example return:

```
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjczNjExNDk2LCJpYXQiOjE2NzM2MTExMzMsImp0aSI6IjQ0YjZiMzQzMTk5ZTQ4MmZhOGZiOGU3YmYzMGYyN2MzIiwidXNlcl9pZCI6Mn0.Ooi-CjNAG193w2LEaGHkNwYi1AoEpqV2MBze4Z_hFYA",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjIwMzE5NiwiaWF0IjoxNjczNjExMTk2LCJqdGkiOiI1OWIzM2NmNjc4MzA0MTgzYTgyNjg0YjQzZDc5ZTBmOSIsInVzZXJfaWQiOjJ9.Zrl09OfHO_ipqgIrrmcb5D7L8VT4YZUmPQBMrX-0Y0E"
}
```

### /api/register/

Create user

#### post

example request:

```
{
    "username": "username",
    "password": "password"
}
```

example response:

```
{
    "username": "username"
}
```

Success code: ```201```

Error code: 

``400`` - bad request


### /api/customer/

View and edit account.

#### get

Returns account information

example response:

```
{
    "user": "igor",
    "firstname": "Igor",
    "lastname": "Niebylski",
    "phone_number": "+48000000000"
}
```

success response code: `200`

error response:

`403 - not authenticated`
`404 - account not found`

#### patch

Changes user personal information

example request:

```
{
    "firstname": "Igor",
    "lastname": "New last name",
    "phone_number": "+48000000000"
}
```

example response:

```
{
    "user": "igor",
    "firstname": "Igor",
    "lastname": "New last name",
    "phone_number": "+48000000000"
}
```

success response code: `200`

error response:

`400 - bad request`
`403 - not authenticated`
`404 - account not found`

#### delete

Deletes user account

success response code: `200`

error response:

`403 - not authenticated`
`404 - account not found`

### /api/customer-address/

Customer shipping address

#### get

Returns customer address

example response:

```
{
    "customer": "test",
    "firstname": "Igor",
    "lastname": "N",
    "city": "Gliwice",
    "postcode": "44-100",
    "street": "some street",
    "house_number": "11"
}
```

success response code: `200`

error response:

`403 - not authenticated`
`404 - address not found`

#### patch

Change user shipping address

example request:

```
{
    "firstname": "Igor",
    "lastname": "N",
    "city": "Gliwice",
    "postcode": "44-100",
    "street": "some street",
    "house_number": "11"
}
```

success response code: `200`

error response:

`400 - bad request`
`403 - not authenticated`
`404 - not found`


### /api/product-list/

List of all products 

#### get

Returns list of all products

example response:

```
[
    {
        "url": "serveraddress/api/product/brand-no1-lorem-ipsum-category-no1/",
        "name": "Lorem Ipsum",
        "slug": "brand-no1-lorem-ipsum-category-no1",
        "category": "category no.1",
        "brand": "Brand no1",
        "image": "http://127.0.0.1:8000/static/media/static/media/Brand%20no1/brand-no1-lorem-ipsum-category-no1/file.webp",
        "current_price": "100.00",
        "base_price": "100.00",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's",
        "no_of_items_in_stock": 20
    },
    ...
]
```

Responses can be sorted by attaching `order_by` parameter to url. 

allowed `order_by` values:

```
price_a - price ascending
price_d - price descending
bestselers - most popular
```

Example: `/api/product-list/?order_by=price_a`


success response code: `200`

error response:

`400 - wrong GET parameter`

### /api/category-product-list/{category}/

List of all products from given category

#### get

Returns list of all products from given category

example response:

```
[
    {
        "url": "serveraddress/api/product/brand-no1-lorem-ipsum-category-no1/",
        "name": "Lorem Ipsum",
        "slug": "brand-no1-lorem-ipsum-category-no1",
        "category": "category no.1",
        "brand": "Brand no1",
        "image": "http://127.0.0.1:8000/static/media/static/media/Brand%20no1/brand-no1-lorem-ipsum-category-no1/file.webp",
        "current_price": "100.00",
        "base_price": "100.00",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's",
        "no_of_items_in_stock": 20
    },
    ...
]
```

Responses can be sorted by attaching `order_by` parameter to url. 

allowed `order_by` values:

```
price_a - price ascending
price_d - price descending
bestselers - most popular
```

Example: `/api/category-product-list/{category}/?order_by=price_a`


success response code: `200`

error response:

`400 - wrong GET parameter`
`404 - category not found`

### /api/brand-product-list/{category}/

List of all products from given brand

#### get

Returns list of all products from given brand

example response:

```
[
    {
        "url": "serveraddress/api/product/brand-no1-lorem-ipsum-category-no1/",
        "name": "Lorem Ipsum",
        "slug": "brand-no1-lorem-ipsum-category-no1",
        "category": "category no.1",
        "brand": "Brand no1",
        "image": "http://127.0.0.1:8000/static/media/static/media/Brand%20no1/brand-no1-lorem-ipsum-category-no1/file.webp",
        "current_price": "100.00",
        "base_price": "100.00",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's",
        "no_of_items_in_stock": 20
    },
    ...
]
```

Responses can be sorted by attaching `order_by` parameter to url. 

allowed `order_by` values:

```
price_a - price ascending
price_d - price descending
bestselers - most popular
```

Example: `/api/brand-product-list/{category}/?order_by=price_a`


success response code: `200`

error response:

`400 - wrong GET parameter`
`404 - brand not found`

### /api/search-product/{search-query}/

List of all products that name, brand or category contains search query

#### get

Returns search results

example response:

```
[
    {
        "url": "serveraddress/api/product/brand-no1-lorem-ipsum-category-no1/",
        "name": "Lorem Ipsum",
        "slug": "brand-no1-lorem-ipsum-category-no1",
        "category": "category no.1",
        "brand": "Brand no1",
        "image": "http://127.0.0.1:8000/static/media/static/media/Brand%20no1/brand-no1-lorem-ipsum-category-no1/file.webp",
        "current_price": "100.00",
        "base_price": "100.00",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's",
        "no_of_items_in_stock": 20
    },
    ...
]
```

Responses can be sorted by attaching `order_by` parameter to url. 

allowed `order_by` values:

```
price_a - price ascending
price_d - price descending
bestselers - most popular
```

Example: `/api/search-product/{search-query}/?order_by=price_a`


success response code: `200`

error response:

`400 - wrong GET parameter`
`404 - brand not found`

### /api/cart-list/

List of all products added to cart

#### get

Returns products added to cart

example response:

```
[
    {
        "item": {
            "url": "http://127.0.0.1:8000/api/product/brand-no1-lorem-ipsum-category-no1/",
            "name": "Lorem Ipsum",
            "slug": "brand-no1-lorem-ipsum-category-no1",
            "category": "category no.1",
            "brand": "Brand no1",
            "image": "http://127.0.0.1:8000/static/media/static/media/Brand%20no1/brand-no1-lorem-ipsum-category-no1/28_ThinkpadDoubleSidedPosterc_NyD8S8G.webp",
            "current_price": "100.00",
            "base_price": "100.00",
            "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries",
            "no_of_items_in_stock": 20
        },
        "quantity": 20,
        "total": 2000.0
    },
    ...
]
```

success response code: `200`

error response:

`404 - brand not found`

#### post

Adding item with given slug to cart

example request:

```
{
    "item":"brand-no1-first-product-category-no1",
    "quantity": 1
}
```

example response:

```
{
    "item": {
        "url": "http://127.0.0.1:8000/api/product/brand-no1-first-product-category-no1/",
        "name": "first product",
        "slug": "brand-no1-first-product-category-no1",
        "category": "category no.1",
        "brand": "Brand no1",
        "image": "http://127.0.0.1:8000/static/media/static/media/Brand%20no1/brand-no1-first-product-category-no1/test.jpg",
        "current_price": "110.00",
        "base_price": "120.00",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries",
        "no_of_items_in_stock": 20
    },
    "quantity": 1,
    "total": 110.0
}
```

success response code: `200`

error response:

`400 - wrong quantity parameter`
`404 - product not found`

### /api/cart-details/{product-slug}/
Single cart for item with given slug
#### get
Returns single cart for item with given slug

example response:

```
{
    "item": {
        "url": "http://127.0.0.1:8000/api/product/brand-no1-lorem-ipsum-category-no1/",
        "name": "Lorem Ipsum",
        "slug": "brand-no1-lorem-ipsum-category-no1",
        "category": "category no.1",
        "brand": "Brand no1",
        "image": "http://127.0.0.1:8000/static/media/static/media/Brand%20no1/brand-no1-lorem-ipsum-category-no1/test.webp",
        "current_price": "100.00",
        "base_price": "100.00",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'",
        "no_of_items_in_stock": 20
        },
    "quantity": 20,
    "total": 2000.0
}
```

success response code: `200`

error response:

`404 - cart with given product slug not found`

#### patch

Adding item with given slug to cart

example request:

```
{
    "quantity": 1
}
```

example response:

```
{
    "item": {
        "url": "http://127.0.0.1:8000/api/product/brand-no1-first-product-category-no1/",
        "name": "first product",
        "slug": "brand-no1-first-product-category-no1",
        "category": "category no.1",
        "brand": "Brand no1",
        "image": "http://127.0.0.1:8000/static/media/static/media/Brand%20no1/brand-no1-first-product-category-no1/test.jpg",
        "current_price": "110.00",
        "base_price": "120.00",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'",
        "no_of_items_in_stock": 20
    },
    "quantity": 1,
    "total": 110.0
}
```

success response code: `200`

error response:

`400 - bad request`
`404 - cart with given product slug not found`

#### delete

Deletes cart with given product slug

success response code: `200`

error response:

`404 - cart with given product slug not found`


### /api/checkout/
Checkout view
#### get
Returns total amount to pay from all carts.

example response:

```
{
    "total": 440.0
}
```

success response code: `200`

error response:

`404 - there is no carts`

#### post
Creates order, with or without discount code.

example request (if you want to apply discount, otherwise send empty request):
```
{
    "discount_code":"minus-10"
}
```

success response code: `201`

error response: 
`404 - discount code not found`

### /api/discount/discount_code/

Discount code info

#### get
Returns discount code name, amount and total amount to pay after applying discount

example response:
```
{
    "discount_code": "minus-50",
    "amount": "50",
    "total": 1500
}
```

success response code: `200`

error response: `404`

