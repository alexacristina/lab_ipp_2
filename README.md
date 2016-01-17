### Laboratory Work Nr. 2

Implementation of an oauth system, having 4 features.

#####Implementation of this oauth system was done in Python, using Django Oauth Toolkit, and Django Rest Framework

In this laboratory work there was needed to:

* Register
For this particular task there has been created a ViewSet such that the user will be able to create and after that be able to see other users, if being authorized. Example of how to register a user. 
```
    curl -X POST -d "grant_type=password&username=username&password=password" -u"client_id:client_secret" http://localhost:8000/authentication/users/
```
The client in this particular case is the app for which the oauth app is used.
The result for this request is the following: 
```{"message":"The user has been created successfully"}```
* Login
The login part of this laboratory is built-in in the DOT tool and it should generate an access token and give a limited time of its validation. 
```curl -X POST -d "grant_type=password&username=fatfrumos&password=ileanacosanzeana" -u"client_id:client_secret" http://localhost:8000/authentication/o/token/
```
The response to this request is the following
```
{
    "access_token": "O3ecYtazF7W5XzJ0K1h1GrDq8AM6RW",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "write groups read",
    "refresh_token": "sq9UCBF5BE3XVyjrdiS61y1g03PW5g"
}
```
    
* Get statistics. History of user's tokens requests (logins).

This feature was implemented partially as it doesn't actually give statistics as a response but the response is contained only of the last login.
The request is the following
```curl -H "Authorization: Bearer 7cSUBjPgdAkzezRbzhgKOAbPbukjII"  http://localhost:8000/authentication/users/1/last_login/```

And the response the following:
```
{
    "username":"username",
    "last_login":"2016-01-12T19:24:16.592Z"
}
* One more, change password for user.

    This feature allows the user to change password by using the generated token authorization of the oauth app.

REQUEST:
```
curl -H "Authorization: Bearer 7cSUBjPgdAkzezRbzhgKOAbPbukjII" -X POST 
    -d "username=username&old_password=old_password&new_password1=new_password&new_password2=confirm_new_password" 
    http://localhost:8000/authentication/users/1/change_password/
```
RESPONSE:
``` {
        "result":"The password has been changed successfully"
    }
```

Regarding the testing part of this application, it has been made approximately 30% of the code written by myself, though the tool that measures the coverage gives a measure of 83% percent of the app. The feature, I made the tests for, is the User Registration Feature. The others require more analysis of source code of DOT in order to test the authorization itself. 

For testing I used ```unittest``` integrated in ```django.test``` module. For test coverage analysis I used ```coverage```.

#####Conclusion

Due to the implementation of this lab I familiarized myself with how an oauth works and how it is implemented, what are the measurements of security of such an app. Besides, I got to understand how to use a package in django and how to integrate it in my project.


