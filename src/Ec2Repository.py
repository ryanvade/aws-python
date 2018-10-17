from Repository import Repository


class Ec2Repository(Repository):
    """Class for retrieving EC2 Instances"""
    def __init__(self, session):
        super(Ec2Repository, self).__init__()
        self.resource = session.resource("ec2")

    def __iter__(self):
        return enumerate(self.resource.instances.all())

    def __getitem__(self, key):
        return [instance for instance in self.resource.instances.limit(key + 1)][-1]
