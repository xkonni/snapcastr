# import the Flask class from the flask module
# flask
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, Separator, View
# wtforms
from wtforms import Form
from wtforms.fields import HiddenField, SelectField, SubmitField, TextField, BooleanField
from wtforms.fields.html5 import IntegerRangeField
# snapcast
import snapcast.control
import asyncio

# parameters

# create navigation bar
topbar = Navbar('snapcastr',
    View('Home', 'base'),
    View('Clients', 'basep', page='clients'),
    View('Groups', 'basep', page='groups'),
    View('Streams', 'basep', page='streams'),
    # Subgroup('Foo',
    #     View('Foo.Bar', 'bar', arg='val'),
    #     Separator(),
    #     View('Foo.Bar', 'bar', arg='val'),
    # )
)
nav = Nav()
nav.register_element('top', topbar)

# create app
app = Flask(__name__)
nav.init_app(app)
Bootstrap(app)

# snapcast
def run_test(loop):
  return (yield from snapcast.control.create_server(loop, start_server.addr, reconnect=True))

def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    snapserver = loop.run_until_complete(run_test(loop))
    return [loop, snapserver]
start_server.addr='localhost'

class volumeSliderForm(Form):
    hf = HiddenField()
    slider = IntegerRangeField(label='volume')

class streamSelectForm(Form):
  hf = HiddenField()
  name = TextField(label='name')
  clients = TextField(label='clients')
  select = SelectField(label='streams')

@app.route('/')
def base():
    return redirect('/page/base')

@app.route('/page/<string:page>', methods=['GET', 'POST'])
def basep(page):
    loop, snapserver = start_server()

    # process POST data
    if ( request.method == 'POST'):
        data = request.form.to_dict(flat=False)
        if ( page == 'clients' ):
            for hf, slider in zip(data['hf'], data['slider']):
                # print('client: %s, volume: %d' % (hf, int(slider)))
                gg = snapserver.client(hf).set_volume(int(slider))
                loop.run_until_complete(gg)
        if ( page == 'groups' ):
            for hf, select in zip(data['hf'], data['select']):
                # print('group: %s, stream: %s' % (hf, select))
                gg = snapserver.group(hf).set_stream(select)
                loop.run_until_complete(gg)
    # generate content
    if ( page == 'clients' ):
        forms = []
        for client in snapserver.clients:
            form = volumeSliderForm(csrf_enabled=False)
            form.slider.default = client.volume
            form.process()
            form.hf.data = client.identifier
            forms.append(form)
        return render_template('clients.html', page=page, forms=forms)
    elif ( page == 'groups' ):
        forms = []
        for group in snapserver.groups:
            form = streamSelectForm(csrf_enabled=False)
            form.select.choices = [(stream.identifier, stream.identifier + " : " + stream.status)
                    for stream in snapserver.streams]
            form.select.default = group.stream
            form.process()
            if ( group.friendly_name ):
                form.name.data = group.friendly_name
            else:
                form.name.data = group.identifier
            form.clients   = group.clients
            form.hf.data   = group.identifier
            forms.append(form)
        return render_template('groups.html', page=page, forms=forms)
    elif ( page == 'streams' ):
        return render_template('streams.html', page=page, streams=snapserver.streams)
    else:
        loop, snapserver = start_server()
        version = snapserver.version
        num_clients = len(snapserver.clients)
        num_groups = len(snapserver.groups)
        num_streams = len(snapserver.streams)
        return render_template('base.html', version=version,num_clients=num_clients,
                num_groups=num_groups, num_streams=num_streams)
