# <app_name> API spec
Tags: <app_name>

Specification describes behaviour of <app_name> API.


## Unathorized API
Tags: real-auth0, mock-auth0

Unauthorized user is not able to see anything

* User is anonymous
* Request "/<app_name>/"
* Response code is "403"

## Failing flow for API
Tags: mock-auth0

Replace with scenario

* User has scope "<replace with scopes>"
* User tries to <do something bad>
* Response code is "400"


## Normal flow for API
Tags: mock-auth0

Replace with scenario

* User is authenticated
* User tries to <do something>
* Response code is "201"
* User has scope "<replace with scopes>"
* Good result