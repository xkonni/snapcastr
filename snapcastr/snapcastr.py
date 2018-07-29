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
server_addr='innocence'

# create navigation bar
topbar = Navbar('snapcastr',
    View('Home', 'base'),
    View('Clients', 'basep', page='clients'),
    View('Groups', 'basep', page='groups'),
    View('Streams', 'basep', page='streams'),
    View('Zones', 'basep', page='zones'),
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
  return (yield from snapcast.control.create_server(loop, server_addr, reconnect=True))

def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    snapserver = loop.run_until_complete(run_test(loop))
    return [loop, snapserver]

class volumeSliderForm(Form):
    hf = HiddenField()
    slider = IntegerRangeField(label='volume')

class streamSelectForm(Form):
  hf = HiddenField()
  name = TextField(label='name')
  clients = TextField(label='clients')
  select = SelectField(label='streams')

class assignForm(Form):
  hf = HiddenField()
  select = SelectField(label='streams')

@app.route('/')
def base():
    return redirect('/page/base')

@app.route('/page/<string:page>', methods=['GET', 'POST'])
def basep(page):
    loop, snapserver = start_server()

    # process POST data
    if ( request.method == 'POST'):
        if ( page == 'clients' ):
            data = request.form.to_dict(flat=False)
            for i in range(0, len(data['hf'])):
                # print('client: %s, volume: %d' % (data['hf'][i], int(data['slider'][i])))
                gg = snapserver.client(data['hf'][i]).set_volume(int(data['slider'][i]))
                loop.run_until_complete(gg)
        if ( page == 'groups' ):
            data = request.form.to_dict(flat=False)
            for i in range(0, len(data['hf'])):
                # print('group: %s, stream: %s' % (data['hf'][i], data['select'][i]))
                grp = snapserver.group(data['hf'][i])
                gg = None
                if data['select'][i]=='0':
                    gg = grp.set_muted(True)
                else:
                    if grp.muted:
                        gg = grp.set_muted(False)
                        loop.run_until_complete(gg)
                    gg = grp.set_stream(data['select'][i])
                loop.run_until_complete(gg)
        if ( page == 'zones' ):
            data = request.form.to_dict(flat=False)
            for i in range(0, len(data['hf'])):
                # print('group: %s, stream: %s' % (data['hf'][i], data['select'][i]))
                gg = snapserver.group(data['select'][i]).add_client(data['hf'][i])
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
            form.select.choices.append(("0","Mute"))
            form.select.default = "0" if group.muted else group.stream
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
    elif ( page == 'zones' ):
        forms = []
        for client in snapserver.clients:
            form = assignForm(csrf_enabled=False)
            form.select.choices = [(group.identifier, group.friendly_name + " : " + group.identifier)
                    for group in snapserver.groups]
            form.select.default = client.group.identifier
            form.process()
            form.hf.data = client.identifier
            forms.append(form)
        return render_template('zones.html', page=page, forms=forms)
    else:
        loop, snapserver = start_server()
        version = snapserver.version
        num_clients = len(snapserver.clients)
        num_groups = len(snapserver.groups)
        num_streams = len(snapserver.streams)
        return render_template('base.html', version=version,num_clients=num_clients,
                num_groups=num_groups, num_streams=num_streams)
