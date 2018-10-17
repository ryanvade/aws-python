import json

import boto3
from Ec2Repository import Ec2Repository
from VpcRepository import VpcRepository


def get_ec2_instance_json(instance, with_vpc=False):
    instance_details = {}
    for attr in dir(instance):
        if "__" not in attr and not callable(instance.__getattribute__(attr)):
            if attr is "vpc" and with_vpc:
                instance_details[attr] = get_vpc_json(
                    instance.__getattribute__(attr))
            elif attr is not "vpc":
                instance_details[attr] = instance.__getattribute__(attr)

    return instance_details


def get_ec2_subnet_json(subnet):
    subnet_details = {}
    for attr in dir(subnet):
        if "__" not in attr and not callable(subnet.__getattribute__(attr)):
            subnet_details[attr] = subnet.__getattribute__(attr)
    return subnet_details


def get_ec2_internet_gateway_json(gateway):
    gateway_details = {}
    for attr in dir(gateway):
        if "__" not in attr and not callable(gateway.__getattribute__(attr)):
            gateway_details[attr] = gateway.__getattribute__(attr)
    return gateway_details


def get_vpc_json(vpc):
    vpc_details = {
        'id': vpc.id,
        'cird': vpc.cidr_block,
        'cidr_association': vpc.cidr_block_association_set,
        'dhcp_options': vpc.dhcp_options_id,
        'instance_tenancy': vpc.instance_tenancy,
        'ipv6_cidr_association': vpc.ipv6_cidr_block_association_set,
        'is_default': vpc.is_default,
        'state': vpc.state,
        'tags': vpc.tags,
        'vpc_id': vpc.vpc_id
    }
    instances = []
    for instance in vpc.instances.all():
        instances.append(get_ec2_instance_json(instance))
    vpc_details['instances'] = instances

    subnets = []
    for subnet in vpc.subnets.all():
        subnets.append(get_ec2_subnet_json(subnet))
    vpc_details['subnets'] = subnets

    internet_gateways = []
    for gateway in vpc.internet_gateways.all():
        internet_gateways.append(get_ec2_internet_gateway_json(gateway))
    vpc_details['internet_gateways'] = internet_gateways
    return json.dumps(vpc_details, default=str)

session = boto3.Session(region_name='us-west-2')

vpc_repo = VpcRepository(session)
vpc = vpc_repo[0]
print(get_vpc_json(vpc))
