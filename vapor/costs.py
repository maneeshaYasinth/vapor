import boto3
from datetime import datetime, timedelta


def get_session(profile=None):
    return boto3.Session(profile_name=profile) if profile else boto3.Session()


def get_cost_and_usage(profile=None):
    client = get_session(profile).client('ce', region_name='us-east-1')

    today = datetime.today()
    start = today.replace(day=1).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

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


def get_daily_costs(profile=None, days=7):
    client = get_session(profile).client('ce', region_name='us-east-1')

    end = datetime.today()
    start = end - timedelta(days=days)

    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start.strftime('%Y-%m-%d'),
            'End': end.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
    )

    return response['ResultsByTime']


def get_forecast(profile=None):
    client = get_session(profile).client('ce', region_name='us-east-1')

    today = datetime.today()
    start = today.strftime('%Y-%m-%d')

    if today.month == 12:
        end = today.replace(day=31).strftime('%Y-%m-%d')
    else:
        end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        end = end.strftime('%Y-%m-%d')

    if start == end:
        return None

    try:
        response = client.get_cost_forecast(
            TimePeriod={'Start': start, 'End': end},
            Metric='UNBLENDED_COST',
            Granularity='MONTHLY'
        )
        return float(response['Total']['Amount'])
    except Exception:
        return None