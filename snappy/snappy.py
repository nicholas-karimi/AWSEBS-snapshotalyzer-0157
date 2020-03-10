import boto3
import click

session = boto3.Session(profile_name='snappy')
ec2 = session.resource('ec2')

def filter_intsances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances


#group list, stop and start commands
@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,
              help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"

    instances = filter_intsances(project)

    for instance in instances:
        tags = { t['Key']: t['Value'] for t in instance.tags or [] }
        print(','.join((
            #boto3 ec2 parameters
            instance.id,
            instance.instance_type,
            instance.placement['AvailabilityZone'],
            instance.state['Name'],
            instance.public_dns_name,
            tags.get('Project', '<no project>')
        )))
    return

#Stop instance
@instances.command('stop')
@click.option('--project', default=None,
              help="Only instances for project")
def stop_intances(project):
    "Stop EC2 instances"
    # instances = []
    # if project:
    #     filters = [{'Name':'tag:Project', 'Values':[project]}]
    #     instances = ec2.instances.filter(Filters=filters)
    # else:
    #     instances = ec2.instances.all()
    instances = filter_intsances(project)

    for i in instances:
        print('Stopping {0}...'.format(i.id))
        i.stop()
    return

#Start Instance
@instances.command('start')
@click.option('--project', default=None,
              help="Only instances for project")
def start_intances(project):
    "Start EC2 instances"

    instances = filter_intsances(project)

    for i in instances:
        print('Starting {0}...'.format(i.id))
        i.start()
    return

if __name__ == '__main__':
    instances()
