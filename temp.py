import boto3
from ast import literal_eval

client = boto3.client('kms', region_name='us-east-1')

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('mytable')

#response = table.put_item(Item={'email':'ssinstein123@gmail.com', 'username':'3rx2', 'password':'Qwerty@321'}, ConditionExpression = 'attribute_not_exists(username) and attribute_not_exists(password)')
#use try catch in put for conditional

response = table.get_item(Key={'email':'123@gmail.com'})
x = ''
if 'Item' in response:
    x = literal_eval(response['Item']['password'].decode())
    print(x)
else:
    print('not')

response = client.encrypt(KeyId='703190f2-4f7b-4a9b-bf33-b9eff211fc24', Plaintext= "Qwerty@321", GrantTokens=['string',])
y = (response['CiphertextBlob'])
print(type(y))
print(y)
#response = table.put_item(Item={'email':'123@gmail.com', 'username':'3rx2', 'password':x}, ConditionExpression = 'attribute_not_exists(username) and attribute_not_exists(password)')
#print(response)
print(type(x))
response = client.decrypt(CiphertextBlob=x, GrantTokens= ['string', ], KeyId= '703190f2-4f7b-4a9b-bf33-b9eff211fc24')
print(response['Plaintext'])

