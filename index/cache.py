import boto3
import scheduler as schedule
import os


def exports():
    dynamodb = boto3.client('dynamodb')
    scheduler = schedule.Scheduler()
    return dynamodb, scheduler