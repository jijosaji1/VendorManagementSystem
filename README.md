# README

## API Endpoints

1. **/auth/login/**: This endpoint allows only POST requests. It is used to get the token required for all other HTTP requests. The format for sending the POST request is available under auth.json.

    ```json
    {
        "username": "admin",
        "password": "admin"
    }
    ```

    Here, the username and password are the ones used to create a superuser or any other users.

2. **/api/vendors/**: This endpoint allows GET and POST requests only. It is used to view all vendors with a GET request and add a new vendor with a POST request. The format for sending the POST request is available under vendor.json.

    ```json
    {
        "name": "New Vendors",
        "contact_details": "9999999999",
        "address": "123 New Jersey, 21654",
        "vendor_code": "1"
    }
    ```

    Here, the vendor_code should be unique for all vendors.

3. **/api/vendors/{vendor_id}/**: This endpoint allows GET, PUT, and DELETE requests only. It is used to view, modify, or delete the details of a specific vendor.

4. **/api/purchase_orders/**: This endpoint allows GET and POST requests only. It is used to view all purchase orders and create a new purchase order. The format for sending the POST request is available under purchase_orders.json.

    ```json
    {
        "po_number": "PO2",
        "order_date": "2023-12-01T22:00:00Z",
        "delivery_date": "2023-12-15T12:00:00Z",
        "items": {
            "bat": 3,
            "pads": 8
        },
        "quantity": 11,
        "status": "pending",
        "issue_date": "2023-12-01T22:01:00Z",
        "vendor": 4
    }
    ```

    Here, the po_number must be unique.

5. **/api/purchase_orders/{po_id}/**: This endpoint allows GET, PUT, and DELETE requests only. It is used to view, modify, or delete the details of a specific purchase order. Use this endpoint to change the status to completed or canceled.

6. **/api/vendors/{vendor_id}/performance**: This endpoint allows GET requests only. It is used to view the performance of each vendor individually.

7. **/api/purchase_orders/{po_id}/acknowledge**: This endpoint allows POST requests only. It is used to acknowledge a purchase order by the vendor. No data needs to be passed while sending the POST request.

## Test Instructions

### 1. Installations

1. To install Django:
   ```bash
   pip install django
2. To install django rest framework:
   ```bash
   pip install djangorestframework
   ```
### 2. Running the Server

1. To run the server, first move to the VendorManagementSystem directory, and then run,
   ```bash
   python manage.py runserver	
2. To create the initial database structure run,
   ```bash
   python manage.py makemigrations
   python manage.py migrate
4. To create a superuser, run,
   ```bash
   python manage.py createsuperuser
   ```
   **Note** : The credentials are used to generate the token for sending the Http request.

### 3. Running Test Suites
 **Note**: 
 Make sure to run the server before starting to send http requests.
 Make sure to follow the steps in Section 2 and 3 before moving forward
 1. Running Test for Vendor Model
    ```bash
    python manage.py test VendorManager.tests
 2. Running Test for Purchase Orders Model
    ```bash
    python manage.py test PurchaseOrder.tests
    ```
### Note: Follow the below steps to do customized testing of API endpoints
### 4. Creating Bearer Token for Authentication
 **Note**: 
 Make sure to run the server before starting to send http requests. Make use of a software like Postman or Insomnia to send the http requests. 
 For sending http requests I have used Insomnia.
1. Send a POST request to http://127.0.0.1:8000/auth/login. The data of the POST request must be JSON and must have username and password as keys.
2. Now apply the token received under bearer token with the prefix as Token.

### 5. Sending Http requests:
 **Note**: 
 Make sure to run the server before starting to send http requests. Make use of a software like Postman or Insomnia to send the http requests. 
 For sending http requests I have used Insomnia. 
 Make sure to follow the steps in Section 2 and 3 before moving forward
 
1. Sending POST request, enter the correct uri and provide the correct information and then click on Send.
2. Sending GET request,  enter the correct uri and then click on Send.
3. Sending PUT request,  enter the correct uri and provide the correct information and then click on Send. To get the details of the vendor or purchase order that needs to be updated, first do a GET request for the specific vendor id or purchase order id. Then copy the JSON data and modify it.
4. Sending DELETE request,  enter the correct uri and then click on Send.
