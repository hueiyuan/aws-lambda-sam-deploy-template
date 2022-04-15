import boto3

def get_ssm_value(region, ssm_name, is_decryption=True):
    client = boto3.client(service_name='ssm', region_name=region)
    response = client.get_parameter(
        Name=ssm_name,
        WithDecryption=is_decryption
    )

    corresponding_value = response['Parameter']['Value']

    return corresponding_value.replace('\"','')
  
