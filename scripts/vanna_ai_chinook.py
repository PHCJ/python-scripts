pip install vanna

import vanna
from vanna.remote import VannaDefault

api_key = vanna.get_api_key('email@gmail.com')

vanna_model_name = 'chinook'
vn = VannaDefault(model=vanna_model_name,api_key = api_key)

vn.connect_to_sqlite('https://vanna.ai/Chinook.sqlite')

vn.ask("Quais são os artistas mais relevantes?")

from vanna.flask import VannaFlaskApp
app = VannaFlaskApp(vn)
app.run()