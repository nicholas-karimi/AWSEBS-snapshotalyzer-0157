import boto3
import click

session = boto3.Session(profile_name='snappy')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    "List EC2 instances"
    for instance in ec2.instances.all():
        print(','.join((
            instance.id,
            instance.instance_type,
            instance.placement['AvailabilityZone'],
            instance.state['Name'],
            instance.public_dns_name
        )))
    return

if __name__ == '__main__':
    list_instances()
