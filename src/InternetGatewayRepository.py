from Repository import Repository


class InternetGatewayRepository(Repository):
    """Class for retrieving Internet Gateways"""
    def __init__(self, session):
        super(InternetGatewayRepository, self).__init__()
        self.resource = session.resource("ec2")

    def __iter__(self):
        return enumerate(self.resource.internet_gateways.all())

    def __getitem__(self, key):
        return [instance for instance in self.resource.internet_gateways.limit(key + 1)][-1]
