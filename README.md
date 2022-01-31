# rest_test
not implemented: migrations & tests
#### running the project
```console
docker-compose up --build
```
#### example workflow
```console
foo@bar:~$ http POST :5000/login username=usr1 password=123
HTTP/1.0 200 OK
Content-Length: 293
Content-Type: application/json
...
{
   "access_token": "access_token"
}

foo@bar:~$ export JWT="access_token"
foo@bar:~$ http [POST, PUT, DELETE] :5000/<route> Authorization:"Bearer $JWT"
```
