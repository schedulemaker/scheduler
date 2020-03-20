import boto3
import scheduler
import os


def exports():
    dynamodb = boto3.client('dynamodb')
    
    return dynamodb, scheduler