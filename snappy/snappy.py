import boto3
import botocore
import click

session = boto3.Session(profile_name='snappy')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances


@click.group()
#cli main group with volumes and instances commands
def cli():
    """Snappy manages snapshots"""

@cli.group('snapshots')
def snapshots():
    "Commands for snapshots"

@snapshots.command('list')
@click.option('--project', default=None,
              help="Only snapshots for project (tag Project:<name>)")
@click.option('--all', 'list_all', default=None, is_flag=True,
              help='List all snapshots for each volume, not only the most recnt one.' )

def list_snapshots(project, list_all):
    "List EC2 snapshots"

    instances = filter_instances(project)
    for instance in instances:
        for vol in instance.volumes.all():
            for snap in vol.snapshots.all():
                print(','.join((
                    snap.id,
                    vol.id,
                    instance.id,
                    snap.state,
                    snap.progress,
                    snap.start_time.strftime('%c')
                )))
                if snap.state == 'completed' and not list_all: break
    return


@cli.group('volumes')
def volumes():
    "Commands for volumes"

@volumes.command('list')
@click.option('--project', default=None,
              help="Only instances for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)

    for instance in instances:
        for vol in instance.volumes.all():
            print(','.join((
                #boto3 ec2 volume parameters
                vol.id,
                instance.id,
                vol.state,
                str(vol.size) + 'GiB',
                vol.encrypted and 'Encrypted' or 'Not Encrypted'
            )))
    return



#group list, stop and start commands
@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('snapshot',
                  help="Create snapshots for all volumes.")
@click.option("--project", default=None,
                  help="Only instances for project (tag Project:<name>)")

def create_snapshots(project):
    """Create snapshots for ec2 instances"""
    instances = filter_intsances(project)

    for instance in instances:
        print('Stopping {0}....'.format(instance.id))

        #stop instances before creating snapshots
        instance.stop ()
        instance.wait_until_stopped()

        for vol in instance.volumes.all():
            print("Creating snapshots for {0}".format(vol.id))
            vol.create_snapshot(Description="Created by SnnapshotAlyzer-0157")

        print('Starting {0}...'.format(instance.id))
        instance.start()
        instance.wait_until_running()

    print("Job's Done!")
    return


@instances.command('list')
@click.option('--project', default=None,
              help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

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
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Could not stop {0}..".format(i.id) + str(e))
            continue

    return

#Start Instance
@instances.command('start')
@click.option('--project', default=None,
              help="Only instances for project")
def start_intances(project):
    "Start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print('Starting {0}...'.format(i.id))

        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Could not start {0}..".format(i.id) + str(e))
            continue
    return

if __name__ == '__main__':
    cli()
