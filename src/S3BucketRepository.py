from Repository import Repository


class S3BucketRepository(Repository):
    """Class for retrieving S3 Buckets"""
    def __init__(self, session):
        super(S3BucketRepository, self).__init__()
        self.resource = session.resource("s3")

    def __iter__(self):
        return enumerate(self.resource.buckets.all())

    def __getitem__(self, key):
        return [instance for instance in self.resource.buckets.limit(key + 1)][-1]
