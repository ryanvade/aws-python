from Repository import Repository


class VpcRepository(Repository):
    """Class for retrieving VPC Instances"""
    def __init__(self, session):
        super(VpcRepository, self).__init__()
        self.resource = session.resource("ec2")

    def __iter__(self):
        return enumerate(self.resource.vpcs.all())

    def __getitem__(self, key):
        return [instance for instance in self.resource.vpcs.limit(key + 1)][-1]
