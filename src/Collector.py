import json
from Ec2Repository import Ec2Repository
from VpcRepository import VpcRepository
from InternetGatewayRepository import InternetGatewayRepository
from SecurityGroupRepository import SecurityGroupRepository
from S3BucketRepository import S3BucketRepository
from UserRepository import UserRepository

class Collector(object):
    """Collects information from AWS"""

    def __init__(self, session):
        super(Collector, self).__init__()
        self.session = session
        self.vpc_repository = VpcRepository(session)
        self.ec2_repository = Ec2Repository(session)
        self.gateway_repository = InternetGatewayRepository(session)
        self.securitygroup_repository = SecurityGroupRepository(session)
        self.s3bucket_repository = S3BucketRepository(session)
        self.user_repository = UserRepository(session)

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

    def __get_internet_gateways(self, account):
        gateways = []
        for id, gateway in self.gateway_repository:
            for attach in gateway.attachments:
                if 'VpcId' in attach:
                    gateways.append({
                        'data': {
                            'id': gateway.id,
                            'label': gateway.internet_gateway_id,
                            'parent': account['data']['id']
                        },
                        'classes': 'internetgateway'
                    })
                    gateways.append({
                        'data': {
                            'id': str(gateway.id) + str(attach['VpcId']),
                            'source': gateway.id,
                            'target': attach['VpcId']
                        },
                        'classes': 'internetedge'
                    })
                    gateways.append({
                        'data': {
                            'id': str(gateway.id) + 'internet',
                            'source': gateway.id,
                            'target': 'internet'
                        }
                    })
        return gateways

    def __get_security_groups(self, account):
        groups = []
        for id, instance in self.ec2_repository:
            for group in instance.security_groups:
                # print(group)
                groups.append({
                    'data': {
                        'id': group['GroupId'],
                        'label': group['GroupName'],
                        'parent': instance.subnet_id
                    },
                    'classes': 'securitygroup'
                })
                groups.append({
                    'data': {
                        'id': str(group['GroupId']) + str(instance.id),
                        'source': group['GroupId'],
                        'target': instance.id
                    }
                })
        return groups

    def __get_s3_buckets(self, account):
        buckets = []
        for id, bucket in self.s3bucket_repository:
            buckets.append({
                'data': {
                    'id': bucket.name,
                    'label': bucket.name,
                    'parent': account['data']['id']
                },
                'classes': 's3bucket'
            })
        return buckets

    def __get_users(self, account):
        users = []
        for id, user in self.user_repository:
            users.append({
                'data': {
                    'id': user.user_name,
                    'label': user.name,
                    'parent':account['data']['id'],
                },
                'classes': 'user'
            })
            for policy in user.policies.all():
                doc = policy.policy_document
                for statement in doc["Statement"]:
                    if 'Resource' in statement:
                        res = statement['Resource'][0]
                        users.append({
                            'data': {
                                'id': str(user.user_name) + str(policy.name),
                                'source': user.user_name,
                                'target': res[13::]
                            }
                        })
        return users

    def __get_access_keys(self, account):
        keys = []
        for id, user in self.user_repository:
            for key in user.access_keys.all():
                keys.append({
                    'data': {
                        'id': key.id,
                        'label': key.access_key_id,
                        'parent': account['data']['id']
                    },
                    'classes': 'accesskey'
                })
                keys.append({
                    'data': {
                        'id': str(user.user_name) + str(key.access_key_id),
                        'source': user.user_name,
                        'target': key.id
                    }
                })
        return keys

    def collect(self):
        # Start with the Account
        account = self.__get_account()
        # Then Internet
        internet = {
            'data': {
                'id': 'internet',
                'label': 'Internet',
            },
            'classes': 'internet'
        }
        # Then VPCs
        vpcs = self.__get_vpcs(account)
        # Then Subnets
        subnets = self.__get_subnets(account)
        # Then resources in subnets
        instances = self.__get_ec2_instances(account)
        gateways = self.__get_internet_gateways(account)
        security_groups = self.__get_security_groups(account)
        buckets = self.__get_s3_buckets(account)
        users = self.__get_users(account)
        access_keys = self.__get_access_keys(account)
        return json.dumps([account] + [internet] + vpcs + subnets + instances + gateways + security_groups + buckets + users + access_keys, default=str)
