from Repository import Repository


class SecurityGroupRepository(Repository):
    """Class for retrieving Security Groups"""
    def __init__(self, session):
        super(SecurityGroupRepository, self).__init__()
        self.resource = session.resource("ec2")

    def __iter__(self):
        return enumerate(self.resource.security_groups.all())

    def __getitem__(self, key):
        return [instance for instance in self.resource.security_groups.limit(key + 1)][-1]
