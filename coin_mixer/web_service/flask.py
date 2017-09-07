# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, flash
import math


class WebService(object):
    def __init__(self, mix_service):
        self.mix_service = mix_service

        WTF_CSRF_ENABLED = True
        self.app = Flask(__name__)

        self.app.secret_key = "wzsc3lbI7TDa0K8YnEkjBM1sZNmAjl21"

        @self.app.route('/')
        def index():
            return render_template('index.html')


        @self.app.route('/mix-request', methods=['POST'])
        def mix_request():
            input_address = request.values['input_address']
            output_addresses = request.values['output_addresses']
            deposit_value = request.values['deposit_value']

            print("HIT", "deposit_value", deposit_value)
            if (not deposit_value.isnumeric() or input_address == "" or
                    output_addresses == ""):
                if (not (deposit_value.isnumeric())):
                    flash('Invalid deposit value.')
                elif (input_address == ""):
                    flash('Input address cannot be empty.')
                elif (output_addresses == ""):
                    flash('Output address cannot be empty.')
                return redirect('/')
            else:
                output_addresses = output_addresses.split(" ")
                deposit_value = math.floor(float(deposit_value))

                client_operator = self.mix_service.client_operator
                client_operator.add_request(input_address,
                                            output_addresses,
                                            deposit_value)
                return redirect('/')


        @self.app.errorhandler(404)
        def page_not_found(event):
            flash('Sorry, that page does not exist. You have been redirected home.')
            return redirect('/', code=302)

    def run(self):
        self.app.run(debug=False, host='0.0.0.0')
