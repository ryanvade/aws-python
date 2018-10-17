import boto3
from flask import Flask, render_template

from helpers import (get_ec2_instance_json, get_ec2_internet_gateway_json,
                     get_ec2_subnet_json, get_vpc_json)

from Collector import Collector

app = Flask(__name__)

@app.route("/data")
def data():
    session = boto3.Session(region_name='us-west-2')
    collector = Collector(session)
    headers = {'Content-Type' : 'application/json'}
    return (collector.collect(), 200, headers)

@app.route("/")
def index():
    return render_template("index.html")
