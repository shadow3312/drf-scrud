## DRF SCRUD Viewset

DRF SCRUD (emphasizes on the S, you'll discover why) Viewset is a lightweight Django package built on top of django-rest-framework. It delivers a highly abstracted global viewset thats provides common CRUD operations methods including advanced search and pagination.

### Features

- Create, Read, Update and Delete ready-to-go methods for viewsets
- FileUploadParser enabled for create and edit methods to allow uploading files and images
- Powerful search feature (all its greatness described [bellow](#the-search-action) )
- Toggle status of instances (if ```is_active``` field on model)
- Paginated responses

### Install

```bash 
pip install drf-scrud
```
    

### Quick Start

1. Add ```scrud``` to your ```INSTALLED_APPS``` like this:
    ```python
    INSTALLED_APPS = [
        ...
        'scrud',  
    ] ```

2. Use in ```views.py```:
    ```python
    
    from scrud import ScrudViewset
    from . import models, serializers
    
    class BookViewset(ScrudViewset)
        # Override the default permissions by action if needed. Default is AllowAny for all actions.
        
        permission_classes_by_action = {
            'create': [IsAuthenticated],
            'list': [IsAuthenticated],
            'get': [IsAuthenticated],
            'edit': [IsAuthenticated],
            'delete': [IsAdminUser],
            'active': [IsAdminUser],
            'desactive': [IsAdminUser],
            'inactives': [IsAdminUser],
            'search': [IsAuthenticated]
        }
        def __init__(self):
            super().__init__(models.Book, serializers.BookSerializer, self.permission_classes_by_action)
    ```
> When defining your Viewset this way, BookViewset inherit these methods: ```list```, ```create```, ```get```, ```edit```, ```delete```, ```activate```, ```deactivate```, ```search```

3. Then, in ```urls.py``` you can set:
```python
    path('book/', include([
        path('', views.BookViewset.as_view({'get': 'list', 'post': 'create'})),
        path('<int:pk>/', views.BookViewset.as_view({'get': 'get'})),
        path('<int:pk>/edit/', views.BookViewset.as_view({'put': 'edit'})),
        path('<int:pk>/delete/', views.BookViewset.as_view({'delete': 'delete'})),
        path('search/', views.BookViewset.as_view({'get': 'search'})),
    ])),
        
```

4. DRF Settings

The returned json of all the endpoints are page number paginated, so you may need to set a default ```PAGE_SIZE``` in ```settings.py```

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

5. You are done ! All the endpoints should be working fine by now.

### Especialy for the 'inactives()' action

This action make use of a customized manager that binds ```active_rows()``` and ```inactive_rows()``` to model.objects, like ```Book.objects.inactive_rows()```

So if you intend to use this action, consider adding the manager in your models.py like this:

```python
from scrud.managers import TemporalQuerySet

class BookModel(models.Model):
    ...
    objects = TemporalQuerySet()
```


### The Search Action
This action implements advanced query filtering throught model instances to help you improve your API.
```http
https://YOUR_API_ENDPOINT/search/?field_name=value
```
The ```field_name``` can be any of the model field. 
    
Considering a model represented by this json
```json
{
    "id": 1,
    "title": "The journey to Elixir",
    "description": "Elixir is going to rule the world. You better watch out !",
    "price": 250,
    "currency": "USD",
    "release_date": "2022-10-10",
    "author": {
        "id": 1,
        "firstName": "John",
        "lastName": "Doe",
        "city": {
            "id": 5,
            "name": "Sydney",
            "country": {
                "id": 2,
                "name": "Australia"
            }
        }
    } 
}

```
You can filter by ```title```, ```description``` and/or any other 
```/search/?title="stuff"```
or
```/search/?title="elix"&description="world"&price=150&{and_so_on_to_infinity}```


> String fields are double-quoted

- #### Even better
    You can lookup throughout related models

    ```/search/?author__city__country_name="Aus" ```
        
        Double underscore __ to reach related model name, and single _ to reach a field

    > String field lookups are case insensitive and perform a like %% sql query

### Overriding a method
You can override any of the pre-built method.

- e.g adding decorator

```python
@extend_schema(
        parameters=[
            OpenApiParameter(
            name='title',
            required=False,
            location=OpenApiParameter.QUERY,
            ),
        ]
    )
    def search(self, request):
        return super().search(request)
```

- If you want to override the entire function, just write your function as usual
```python
def search(self, request):
    # New code goes here
```

Feel free to open issues or to pull request. Contributors are welcome.

&copy; Shuruzer.