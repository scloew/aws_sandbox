"""
following along with tutorial beginning at
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-creating-alarms.html

terminology:

alarm: watches a single metric over period of time; performs 1+ actions based
       on value of metric relative to threshold over number of time periods
"""

import boto3


def print_alarms():
    #create CloudWatch client if one does not exist
    cloudwatch = boto3.client('cloudwatch')

    #List alarms of insufficent data through the pagination interface
    #paginator docs: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html
    paginator = cloudwatch.get_paginator('describe_alarms')
    for response in paginator.paginate(StateValue='INSUFFICIENT_DATA'):
        print(response['MetricAlarms'])


def create_alarm(alarm_name='Web_Server_CPU_Utilization'):
    """
    Note, the alarm name may change but everything else will always be the same
    alarm docs found at https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html
    """

    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=60,
        Statistic='Average',
        Threshold=70.0,
        ActionsEnabled=False,
        AlarmDescription='Alarm when server CPU exceeds 70%',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'INSTANCE_ID'
            },
        ],
        Unit='Seconds'
    )
    print_alarms()


def delete_alarm(alarm_name='Web_Server_CPU_Utilization'):
    cloudwatch = boto3.client('cloudwatch')

    cloudwatch.delete_alarms(
        AlarmNames=[alarm_name]
    )
    print_alarms()


def create_alarm_with_actions(alarm_name='Web_Server_CPU_Utilization'):
    cloudwatch = boto3.client('cloudwatch')

    # Create alarm with actions enabled
    cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Period=60,
        Statistic='Average',
        Threshold=70.0,
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:swf:us-east-1:{CUSTOMER_ACCOUNT}:action/actions/AWS_EC2.InstanceId.Reboot/1.0'
        ],
        AlarmDescription='Alarm when server CPU exceeds 70%',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': 'INSTANCE_ID'
            },
        ],
        Unit='Seconds'
    )
    print_alarms()


def disable_action(alarm_name='Web_Server_CPU_Utilization'):
    """
    this function will turn 'ActionsEnabled' field
    for <alarm_name> to False
    """
    cloudwatch = boto3.client('cloudwatch')

    #disable alarm
    cloudwatch.disable_alarm_actions(
        AlarmNames=[alarm_name]
    )
    print_alarms()


def list_metrics(args=None):
    """
    function code from: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-metrics.html
    """
    if not args:
        kargs = {'Dimensions': [{'Name': 'LogGroupName'}],
                 'MetricName': 'IncomingLogEvents',
                 'Namespace': 'AWS/Logs'}
    else:
        print(f'args are triggered {args}')
        kargs = args

    cloudwatch = boto3.client('cloudwatch')

    #list metrics through the paginator interface
    #more on paginators at: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html
    paginator = cloudwatch.get_paginator('list_metrics')

    for response in paginator.paginate(**kargs):
        print(response['Metrics'])


def publish_metric():
    cloudwatch=boto3.client('cloudwatch')

    args = {'Dimensions': [{'Name': 'UNIQUE_PAGES', 'Value': 'URLS'}],
                 'MetricName': 'PAGES_VISITED',
                 'Namespace': 'SITE/TRAFFIC'}

    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'PAGES_VISITED',
                'Dimensions': [
                    {
                        'Name': 'UNIQUE_PAGES',
                        'Value': 'URLS'
                    },
                ],
                'Unit': 'None',
                'Value': 1.0
            },
        ],
        Namespace='SITE/TRAFFIC'
    )

    list_metrics(args)



if __name__ == '__main__':
    # print('\n***\nstep 1 of tutorial')
    # print('https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-creating-alarms.html\n***\n')
    # print('\n***\ncreate\n***\n')
    # create_alarm()
    # print('\n***\ndelete\n***\n')
    # delete_alarm()
    # input('\n***\nbreak\n***\n')
    # print('\n***\ncreate foo\n***\n')
    # create_alarm('foo')
    # print('\n***\ncreate bar\n***\n')
    # create_alarm('bar')
    # print('\n***\ndelete bar\n***\n')
    # delete_alarm('bar')
    # print('\n***\ndelete foo\n***\n')
    # delete_alarm('foo')
    # print('\n***\nstep 2 of tutorial')
    # print('https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-using-alarms.html\n***\n')
    # print('\n***\ncreate alarm with action\n***\n')
    # create_alarm_with_actions()
    # print('\n***\ndisable action on alarm\n***\n')
    # disable_action()
    # print('\n***\ndelete\n***\n')
    delete_alarm()
    print('\n***\nstep 3 of tutorial')
    print('https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-metrics.html\n***\n')
    list_metrics()
    publish_metric()
    print('\n***\nstep 4 of tutorial')
    print('https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-events.html\n***\n')