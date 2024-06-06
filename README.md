# Aioaquacell

Asynchronous library to retrieve details of your Aquacell water softener device.
This API is reverse engineered from the official Android application.

## Requirements

- aiohttp
- aiobotocore
- requests_aws4auth
- pycognito
- aws_request_signer
- botocore
- botocore3

## Usage

```python
userName = "<email address>"
password = "<password>"


async def main():
    api = AquacellApi()
    await api.authenticate(userName, password)
    # Get the refresh token
    print(api.refresh_token)
    
    softeners = await api.get_all_softeners()
    for softener in softeners:
        print(softener.name)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```
### Authenticate using refresh token
```python
refresh_token = "<refresh token>"
api = AquacellApi()
await api.authenticate(refresh_token)
```