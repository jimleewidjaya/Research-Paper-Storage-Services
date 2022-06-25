# Research-Paper-Storage-Services

is a service where students can add / save paper on the service provided. There are 2 types of users, students and teachers.

Note: Teacher account inputted manually by admin (not register user)

## Requests

1. Login
2. Logout
3. Upload Paper
4. View All Uploaded Paper (by Uploader)
   - if role == dosen (teacher) --> can view all file
5. Download Paper
6. User Register

### Request #1: Login

![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/login**</span>

```json
{
  "email": "janedoe@gmail.com",
  "password": "QchpCEKOIsVhOXVj"
}
```

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Login Success!"
}
```

#### Not found

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Your Email and Password are Not Defined"
}
```

<br>

### Request #2: Logout

![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/logout**</span>

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Logged out successfully!"
}
```

<br>

### Request #3: Upload Paper

![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/upload**</span>

Form-Data

1. type = text --> key = title
2. type = text --> key = abstract
3. type = file --> key = file

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Paper uploaded successfully!"
}
```

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

<br>

### Request #4: View All Uploaded Paper (by uploader)

![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/file**</span>

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "paper": [
    {
      "id_paper": 1,
      "filename": "168656837599997.pdf",
      "title": "Simple Cloud Storage",
      "abstract": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
    },
    {
      "id_paper": 2,
      "filename": "-934988497.pdf",
      "title": "Cloud Storage Simple",
      "abstract": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."
    }
  ]
}
```

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

#### There are still no uploaded paper

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "There are still no paper"
}
```

<br>

### Request #5: Download Paper

![GET](https://badgen.net/badge/Method/GET/green)<span style="padding:10px">**/download/`<int:id_paper>`**</span>

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

#### Not Logged In

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log In First!"
}
```

#### `<int:id_paper>` not matching any ID || You are not the owner of paper with that ID

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Paper not found"
}
```

<br>

### Request #6: User register

![POST](https://badgen.net/badge/Method/POST/yellow)<span style="padding:10px">**/login**</span>

```json
{
  "nrp": "c141234567",
  "nama": "jane Doe",
  "email": "janedoe@gmail.com",
  "password": "QchpCEKOIsVhOXVj"
}
```

#### Responses:

#### Success

![OK](https://badgen.net/badge/OK/200/green)

```json
{
  "status": "success",
  "message": "Register Success!"
}
```

#### Still not logged out

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Log Out First!"
}
```

#### Email already registered

![Not Found](https://badgen.net/badge/Not%20Found/404/red)

```json
{
  "status": "error",
  "message": "Your email is already registered!"
}
```
