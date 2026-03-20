import boto3
from datetime import datetime


def get_cost_and_usage(profile=None):
    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    client = session.client('ce', region_name='us-east-1')

    today = datetime.today()
    start = today.replace(day=1).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    # edge case — if today is the 1st, start and end are the same which errors
    if start == end:
        return [], 0.0

    response = client.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    groups = response['ResultsByTime'][0]['Groups']
    total = sum(float(g['Metrics']['UnblendedCost']['Amount']) for g in groups)

    return groups, total