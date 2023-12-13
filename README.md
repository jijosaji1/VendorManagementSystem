README

API Endpoints

1./auth/login/ : This endpoint allows only POST requests. This endpoint is used to get the token required to send all other http requests. The format for sending the POST request is available under auth.json. i.e.,
{
	"username": "admin",
	"password": "admin"
}
Here the username and password is the one used to create a super user or any other users.

2./api/vendors/ : This endpoint allows GET and POST requests only. This endpoint is used to view all vendors with a GET request and add a new vendor with a POST request. The format for sending the POST request is available under vendor.json. i.e.,
{
    "name": "New Vendors",
    "contact_details": "9999999999",
    "address": "123 New Jersey, 21654",
    "vendor_code": "1"
}
Here the vendor_code should be unique for all vendors

3./api/vendors/{vendor_id}/ : This endpoint allows GET, PUT and DELETE requests only. This endpoint is used to view and modify the details of a specific vendor or even delete it.

4./api/purchase_orders/ : This endpoint allows GET and POST requests only. This endpoint is used to view all purchase orders and create new purchase order. The format for sending the POST request is available under purchase_orders.json. i.e.,
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
Here the po_number must be unique.
5. /api/purchase_orders/{po_id}/ : This endpoint allows GET, PUT and DELETE requests only. This endpoint is used to view and modify the details of a specific purchase order or even delete it. Use this endpoint to change the status to completed or cancelled.

6. /api/vendors/{vendor_id}/performance : This endpoint allows GET requests only. This endpoint is used to view the performance of each vendor individually.

7. /api/purchase_orders/{po_id}/acknowledge : This endpoint allows POST requests only. This endpoint is used to acknowledge a purchase order by  the vendor. No data needs to be passed while sending the POST request.

