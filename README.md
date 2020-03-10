# AWSEBS-snapshotalyzer-0157
Project to manage AWS EC2 instances snapshots.

##  About
This project is an illustration of how to use boto3 to
manage AWS EC2 instance snapshots.

## Configuration

snappy uses the configuration file created by AWS cli . eg.

`aws configure --profile snappy`

## Running

`pipenv run snappy/snappy.py <command>
<--project=PROJECT>`

*command* is list, start, stop
*project* is optional
