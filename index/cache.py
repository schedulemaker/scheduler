def exports():
    local = locals()
    globa = globals()

    if 'boto3' not in local and 'boto3' not in globa:
        import boto3
    if 'schedule' not in local and 'schedule' not in globa:
        import scheduler as schedule
    if 'os' not in local and 'os' not in globa:
        import os
    if 'json' not in local and 'json' not in globa:
        import json
    if 'asyncio' not in local and 'asyncio' not in globa:
        import asyncio
    if 'deque' not in local and 'deque' not in globa:
        from collections import deque
    if 'deserializer' not in local and 'deserializer' not in globa:
        from boto3.dynamodb.types import TypeDeserializer as deserializer

    dynamodb = boto3.client('dynamodb')
    scheduler = schedule.Scheduler(deque)
    

    return dynamodb, scheduler, os, json, asyncio, deserializer