# fastapi xss

import uvicorn

from fastapi import FastAPI, Request, Form
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse

# add session for login

app = FastAPI()

data = []  # data is list of tuples (users, messages)
users = [('admin', 'admin'), ('bob', 'bob_p'), ('eve', 'eve_p')]  # users (without database)

app.add_middleware( # add session
    SessionMiddleware,
    secret_key="simple"  # Using a trivial key, not secure
)


@app.get("/")
async def root(request: Request):
    html = '\n'.join([f'{a}: {b} </br>' for a, b in data])  # show all message with </br> in between

    if request.session.get('user') is None:  # if the user in not logged in yet
        html += ('<form method="post", action="/login" id="login_form">'  # login form
                 'username: <input type="text" name="username"></br>'
                 'password: <input type="password" name="password"></br>'
                 '<input type="submit" value="Login">'
                 '</form>')
    else:  # the user is logged in
        html += ('<form method="post", action="/add_comment">'  # form to add comment  
                 'text: <input type="text" name="text"> </br>'
                 '<input type="submit" value="submit">'
                 '</form></br>'
                 '<form method="get", action="/logout">'  # form to log out
                 '<input type="submit" value="Logout">'
                 '</form>')
    return HTMLResponse(html)


@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    if any(a[0] == username and a[1] == password for a in users):
        request.session["user"] = username
        return RedirectResponse(url='/', status_code=303)
    return HTMLResponse('Login Failed')


@app.post("/add_comment")
async def add_comment(request: Request, text: str = Form(...)):
    if request.session.get('user') is None:
        return RedirectResponse(url='/', status_code=303)

    data.append((request.session.get('user'), text))
    return RedirectResponse(url='/', status_code=303)


@app.get("/logout")
async def logout(request: Request):
    del request.session["user"]
    return RedirectResponse(url='/', status_code=303)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
