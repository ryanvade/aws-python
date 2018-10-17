import json
from Ec2Repository import Ec2Repository
from VpcRepository import VpcRepository

class Collector(object):
    """Collects information from AWS"""
    def __init__(self, session):
        super(Collector, self).__init__()
        self.session = session
        self.vpc_repository = VpcRepository(session)
        self.ec2_repository = Ec2Repository(session)

    def __get_account(self):
        return {
            'data': {
                'id': self.session.client('sts').get_caller_identity().get('Account'),
                'label': self.session.profile_name,
                  "position": {
                    "x": 122.50374073928583,
                    "y": 367.98329788349827
                    },
            },
            'classes': 'account'
        }

    def __get_vpcs(self, account):
        vpcs = []
        for id, vpc in self.vpc_repository:
            vpcs.append({
                'data': {
                    'id': vpc.id,
                    'label': vpc.vpc_id,
                    'parent': account['data']['id'],
                },
                'classes': 'vpc'
            })
        return vpcs

    def __get_subnets(self, account):
        subnets = []
        for id, vpc in self.vpc_repository:
            for subnet in vpc.subnets.all():
                subnets.append({
                    'data': {
                        'id': subnet.id,
                        'label': subnet.subnet_id,
                        'parent': vpc.id
                    },
                    'classes': 'subnet'
                })
        return subnets

    def __get_ec2_instances(self, account):
        instances = []
        for id, instance in self.ec2_repository:
            instances.append({
                'data': {
                    'id': instance.id,
                    'label': instance.instance_id,
                    'parent': instance.subnet_id
                },
                'classes': 'ec2instance'
            })
        return instances

    def collect(self):
        # Start with the Account
        account = self.__get_account()
        # Then VPCs
        vpcs = self.__get_vpcs(account)
        # Then Subnets
        subnets = self.__get_subnets(account)
        # Then resources in subnets
        instances = self.__get_ec2_instances(account)
        return json.dumps([account] + vpcs + subnets + instances, default=str)
