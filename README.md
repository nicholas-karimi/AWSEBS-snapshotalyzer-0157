# AWSEBS-snapshotalyzer-0157
Project to manage AWS EC2 instances snapshots.

##  About
This project is an illustration of how to use boto3 to
manage AWS EC2 instance snapshots.

## Configuration

snappy uses the configuration file created by AWS cli . eg.

`aws configure --profile snappy`

## Running

`pipenv run snappy/snappy.py <command> <subcommand>
<--project=PROJECT>`

*command* is list, start, stop
*command* is volume, instances, or snapshop
*subcommand* depends on command 
*project* is optional
