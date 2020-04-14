import asyncio
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, Separator, View
import snapcast.control
import sys
from wtforms import Form
from wtforms.fields import HiddenField, SelectField, SubmitField, TextField, BooleanField
from wtforms.fields.html5 import IntegerRangeField


class volumeSliderForm(Form):
    hf = HiddenField()
    name = TextField(label='name')
    slider = IntegerRangeField(label='volume')


class streamSelectForm(Form):
    hf = HiddenField()
    name = TextField(label='name')
    clients = TextField(label='clients')
    select = SelectField(label='streams')


class assignForm(Form):
    hf = HiddenField()
    name = TextField(label='name')
    select = SelectField(label='groups')


class Snapcastr:
    def __init__(self, host, port, sc_host, debug):
        self.debug = debug
        self.host = host
        self.port = port
        self.sc_host = sc_host
        self.loop = asyncio.get_event_loop()
        self.app = self.create_app()


    def run(self):
        self.app.run(host=self.host, port=self.port, use_reloader=False, debug=self.debug)


    def create_snapserver(self):
        try:
            snapserver = self.loop.run_until_complete(snapcast.control.create_server(self.loop,
                    self.sc_host, reconnect=True))
        except Exception as ex:
            print(f"Exception get_actors, type: {type(ex).__name__}, args:{ex.args}")
            sys.exit(1)

        return snapserver


    def create_app(self):
        topbar = Navbar('snapcastr',
                View('Home', 'base'),
                View('Clients', 'basep', page='clients'),
                View('Groups', 'basep', page='groups'),
                View('Streams', 'basep', page='streams'),
                View('Zones', 'basep', page='zones'),
                )

        nav = Nav()
        nav.register_element('top', topbar)

        # create app
        app = Flask(__name__)
        nav.init_app(app)
        Bootstrap(app)

        @app.route('/')
        def base():
            return redirect('/page/base')

        @app.route('/page/<string:page>', methods=['GET', 'POST'])
        def basep(page):
            snapserver = self.create_snapserver()
            # process POST data
            if ( request.method == 'POST'):
                data = request.form.to_dict(flat=False)
                if ( page == 'clients' ):
                    for hf, slider in zip(data['hf'], data['slider']):
                        gg = snapserver.client(hf).set_volume(int(slider))
                        self.loop.run_until_complete(gg)
                if ( page == 'groups' ):
                    data = request.form.to_dict(flat=False)
                    for gid, sid in zip(data['hf'], data['select']):
                        grp = snapserver.group(gid)
                        gg = None
                        if sid=='0':
                            gg = grp.set_muted(True)
                        else:
                            if grp.muted:
                                gg = grp.set_muted(False)
                                self.loop.run_until_complete(gg)
                            gg = grp.set_stream(sid)
                        self.loop.run_until_complete(gg)
                if ( page == 'zones' ):
                    data = request.form.to_dict(flat=False)
                    for cid, gid in zip(data['hf'], data['select']):
                        gg = snapserver.group(gid).add_client(cid)
                        self.loop.run_until_complete(gg)

            # generate content
            if ( page == 'clients' ):
                forms = []
                for client in snapserver.clients:
                    form = volumeSliderForm(csrf_enabled=False)
                    form.slider.default = client.volume
                    form.process()
                    if client.friendly_name:
                        form.name.data = client.friendly_name
                    else:
                        form.name.data = client.identifier
                    form.hf.data = client.identifier
                    form.connected = client.connected
                    forms.append(form)
                return render_template('clients.html', page=page, forms=forms)
            elif ( page == 'groups' ):
                forms = []
                clients = {client.identifier: client for client in snapserver.clients}
                for group in snapserver.groups:
                    form = streamSelectForm(csrf_enabled=False)
                    form.select.choices = [
                            (
                                stream.identifier,
                                (stream.friendly_name if stream.friendly_name else stream.identifier) + " : " + stream.status
                                )
                            for stream in snapserver.streams
                            ]
                    form.select.choices.append(("0","Mute"))
                    form.select.default = "0" if group.muted else group.stream
                    form.process()
                    if ( group.friendly_name ):
                        form.name.data = group.friendly_name
                    else:
                        form.name.data = group.identifier
                    form.clients   = [
                            ( client.friendly_name if client.friendly_name else client.identifier,
                              client.connected )
                            for client in [clients[gclient] for gclient in group.clients]
                            ]
                    form.hf.data   = group.identifier
                    forms.append(form)
                return render_template('groups.html', page=page, forms=forms)
            elif ( page == 'streams' ):
                return render_template('streams.html', page=page, streams=snapserver.streams)
            elif ( page == 'zones' ):
                forms = []
                for client in snapserver.clients:
                    form = assignForm(csrf_enabled=False)
                    form.select.choices = [
                            (
                                group.identifier,
                                group.friendly_name if group.friendly_name else group.identifier
                                )
                            for group in snapserver.groups
                            ]
                    form.select.default = client.group.identifier
                    form.process()
                    form.hf.data = client.identifier
                    if client.friendly_name:
                        form.name.data = client.friendly_name
                    else:
                        form.name.data = client.identifier
                    form.connected = client.connected
                    forms.append(form)
                return render_template('zones.html', page=page, forms=forms)
            else:
                version = snapserver.version
                num_clients = len(snapserver.clients)
                num_groups = len(snapserver.groups)
                num_streams = len(snapserver.streams)
                return render_template('base.html', version=version,num_clients=num_clients,
                        num_groups=num_groups, num_streams=num_streams)

        return app
