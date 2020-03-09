import boto3

if __name__ == '__main__':
    session = boto3.Session(profile_name='snappy')
    ec2 = session.resource('ec2')

    for instance in ec2.instances.all():
        print(instance)
