# techstables

## Table of contents
* [Database](#database)
    -   [Database Schema](#database-schema)
    -   [User Model](#user-model)
    -   [Profile Model](#profile-model)
* [Technologies](#technologies)

## Database

* ### Database schema
![Database schema](assets/images/db_diagram.svg)

*   ### User Model 
| name | type | key | others |
|------|------|-----|--------|
| id | BigAuto | Primary Key|| 
| username | CharField |||
| password | Charfield ||| 

*   ### Profile Model
| name | type | key | others |
|------|------|-----|--------|
| id | BigAuto | Primary Key ||
| owner | OneToOneField | Foreign Key | User, on_delete= models.CASCADE |
| created_at | DateTimeField || auto_now_add=True |
| updated_at | DateTimeField || auto_now=True |
| name | CharField || max_length=100, null=True, blacnk=True |
| image | ImageField || upload_to='images/', default='media/images default_profile_xdfle7' |


## Technologies
-   Python
-   Django
-   [Cloudinary](https://cloudinary.com) -> for images storage
-   [DBDiagram](https://dbdiagram.io) -> create db diagram