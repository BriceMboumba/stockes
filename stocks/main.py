import psycopg2 as pg
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# python Auth libraries
from fastapi import Depends, status, Response, HTTPException  # Assuming you have the FastAPI class for routing
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from fastapi_login import LoginManager  # Login manager Class
from fastapi_login.exceptions import InvalidCredentialsException  # Exception class
import path
import os

# get dataframe from schema
from stocks.schema import df, sender, getter, count_id, hasher, connection
from stocks.processing import description
from stocks.model import linear_regression

# {% for i in range((data|length)) %}
app = FastAPI()
try:
    app.mount("/static", StaticFiles(directory="stocks"), name="static")
except RuntimeError:
    pass
templates = Jinja2Templates(directory="stocks/templates")

# get description function
data = description

# Auth script
SECRET = "secret-key"
# To obtain a suitable secret key you can run | import os; print(os.urandom(24).hex())
manager = LoginManager(SECRET, token_url="/", use_cookie=True)
manager.cookie_name = "access-token"


# define app routes
@manager.user_loader()
def load_user(password: str):
    for i in range(1, count_id() + 1):
        password_hashed = hasher(str(i), password)
        sql_request = f"SELECT id, user_name, password from users where password='{password_hashed}'"
        if getter(sql_request):
            return getter(sql_request)


@app.get("/unauthorized", response_class=HTMLResponse)
async def unauth(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("/unauth.html", context)


# 1) A SECURISER !!!
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    context = {"request": request, 'data': data}
    return templates.TemplateResponse("/admin.html", context)


@app.post("/admin", response_class=HTMLResponse)
async def predict_admin(
        request: Request,
        open: float = Form(...),
        high: float = Form(...),
        low: float = Form(...),
        volume: float = Form(...), ):
    # here we can call the machine learning model
    ml = linear_regression(df, open, high, low, volume)
    context = {'request': request, 'data': data, 'ml': ml}
    return templates.TemplateResponse('/admin.html', context)


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    if login():
        context = {"request": request}
        return templates.TemplateResponse("/home.html", context)


@app.post("/home", response_class=HTMLResponse)
async def predict_home(
        request: Request,
        open: float = Form(...),
        high: float = Form(...),
        low: float = Form(...),
        volume: float = Form(...)):
    # here we can call the machine learning model
    ml = linear_regression(df, open, high, low, volume)
    context = {'request': request, 'ml': ml}
    return templates.TemplateResponse('/home.html', context)


@app.get("/", response_class=HTMLResponse)
async def sign_in(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("/sign_in.html", context)


@app.post("/")
def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = load_user(password)
    # [(2, 'laterreestronde1234@', '88067f6cd2d44c9a51b01d08d671e963')]
    if not user:
        return RedirectResponse(url="/login_error", status_code=status.HTTP_302_FOUND)
    for user_info in user:
        if not user_info:
            return RedirectResponse(url="/login_error", status_code=status.HTTP_302_FOUND)
        # elif not hasher(str(user_info[0]), password) == user_info[2]:
        #     return RedirectResponse(url="/login_error", status_code=status.HTTP_302_FOUND)
        elif hasher(str(user_info[0]), password) == hasher('2', '1234@1234@') and username == 'laterreestronde1234@':
            access_token = manager.create_access_token(
                data={"sub": username}
            )
            resp = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
            manager.set_cookie(resp, access_token)
            return resp
        elif hasher(str(user_info[0]), password) == hasher('2', '1234@1234@') and username != 'laterreestronde1234@':
            return RedirectResponse(url="/login_error", status_code=status.HTTP_302_FOUND)
        else:
            access_token = manager.create_access_token(
                data={"sub": username}
            )
            context = {"request": request, 'username': username}
            resp = templates.TemplateResponse("/home.html", context)
            manager.set_cookie(resp, access_token)
            return resp


@app.get("/sign_up", response_class=HTMLResponse)
async def sign_up(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("/sign_up.html", context)


@app.post("/sign_up", response_class=HTMLResponse)
async def register(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    access_token = manager.create_access_token(
        data={"sub": username}
    )
    context = {"request": request, 'username': username}
    resp = templates.TemplateResponse("/home.html", context)
    manager.set_cookie(resp, access_token)

    id = str(count_id() + 1)
    password_hased = hasher(id, password)
    sender((id, username, password_hased), connection)

    return resp


@app.get("/login_error", response_class=HTMLResponse)
async def auth_wrong(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("/auth_wrong.html", context)


# 2) A SECURISER !!!
@app.get("/users", response_class=HTMLResponse)
async def users(request: Request):
    # get users to the database by the request and send it through the context
    context = {"request": request}
    return templates.TemplateResponse("/users.html", context)


# 3) A SECURISER !!!
# change password
@app.get("/change_password", response_class=HTMLResponse)
async def change_password(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("/change_password.html", context)


@app.post("/change_password", response_class=HTMLResponse)
async def change_password(request: Request,
                          last_password: str = Form(...),
                          new_password: str = Form(...), ):
    # send data to the database code (update request) !
    context = {"request": request}

    if "'" in last_password:
        return templates.TemplateResponse("/change_password.html", context)

    elif "'" in new_password:
        return templates.TemplateResponse("/change_password.html", context)

    elif last_password == new_password:
        message = 'Passwords must be different'
        return templates.TemplateResponse("/change_password.html", {"request": request, 'message': message})
    else:
        # call hasher and sender function
        templates.TemplateResponse("/sign_in.html", context)


# Forgot your password
@app.get("/forgot_password", response_class=HTMLResponse)
async def forgot_password(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("/forgot_password.html", context)


@app.post("/forgot_password", response_class=HTMLResponse)
async def change_password(request: Request,
                          username: str = Form(...),
                          first_password: str = Form(...),
                          duplicate_password: str = Form(...),):

    cursor = None
    context = {"request": request}
    message = "Passwords are not the same"
    # send data to the database code (insert request) !
    sql_request = f"SELECT id, user_name, password from users where user_name='{username}'"

    if "'" in first_password:
        return templates.TemplateResponse("/forgot_password.html", context)

    elif "'" in duplicate_password:
        return templates.TemplateResponse("/forgot_password.html", context)
    elif first_password != duplicate_password:
        return templates.TemplateResponse("/forgot_password.html", {"request": request, 'message': message})

    if getter(sql_request):
        id = getter(sql_request)
        password_hased = hasher(id, duplicate_password)

        try:
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Print PostgreSQL details
            print("PostgreSQL server information")
            print(connection.get_dsn_parameters(), "\n")
            # Executing a SQL query
            postgres_insert_query = f"UPDATE users SET {id}='%s', {username}='%s', {password_hased}='%s' where id={id}"
            values = login
            cursor.execute(postgres_insert_query, values)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")

        except (Exception, pg.Error) as error:
            print("Failed to insert record into mobile table", error)
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()

            return templates.TemplateResponse("/sign_in.html", context)


# start server
def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run("stocks.main:app", host="localhost", port=3000, reload=True)
