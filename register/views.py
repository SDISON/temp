from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404
import boto3
from ast import literal_eval
from mylogger import mylogger

logger = mylogger('register-views').createLogger()

def index(request):
    if request.method=='POST':
        logger.debug('Post-call')
        data = request.POST
        if data['flag'] == '1':
            logger.debug('Sign-in')
            email = data['email']
            password = str(data['password'])
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
            table = dynamodb.Table('mytable')
            response = table.get_item(Key={'email':email})
            if 'Item' not in response:
                logger.warning('No user found')
                return HttpResponse('No user found')
            elif decrypt(response['Item']['password']) == password:
                logger.debug('success-signin')
                return HttpResponse('Success')
            else:
                logger.debug('fail-signin')
                return HttpResponse('Fail')
        else:
            logger.debug('Sign-up')
            try:
                username = data['username']
                password = encrypt(data['password'])
                email = data['email']
                dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
                table = dynamodb.Table('mytable')
                try:
                    response = table.put_item(Item={'email':email, 'username':username, 'password':password}, ConditionExpression = 'attribute_not_exists(username) and attribute_not_exists(password)')
                    logger.debug('success-put-signup')
                    return HttpResponse('Saved')
                except Exception as e:
                    logger.warning('already-exists-signup')
                    return HttpResponse('Already exists')
            except:
                logger.error('error-signup')
                return HttpResponse('Error in signup')
    logger.debug('get-call')
    return render(request,'register/index.html',{})

def encrypt(msg):
    logger.debug('encrypt-call')
    try:
        client = boto3.client('kms', region_name='us-east-1')
        response = client.encrypt(KeyId='703190f2-4f7b-4a9b-bf33-b9eff211fc24', Plaintext= msg, GrantTokens=['string',])
        logger.debug('success-encrypt')
        return repr(response['CiphertextBlob'])
    except:
        logger.error('error-encrypt')
        return HttpResponse('Error during encryption')

def decrypt(msg):
    logger.debug('decrypt-call')
    try:
        msg = literal_eval(msg.decode())
        client = boto3.client('kms', region_name='us-east-1')
        response = client.decrypt(KeyId = '703190f2-4f7b-4a9b-bf33-b9eff211fc24', CiphertextBlob= msg, GrantTokens=['string',])
        logger.debug('success-decrypt')
        return str(response['Plaintext'])
    except:
        logger.error('error-decrypt')
        return HttpResponse('Error during execution')
