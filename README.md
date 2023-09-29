# Aioaquacell

Asynchronous library to retrieve details of your Aquacell water softener device

## Requirements

- aiohttp
- aioboto3
- requests_aws4auth
- pycognito
- aws_request_signer

## Usage

```python
userName = "<email address>"
password = "<password>"


async def main():
    api = AquacellApi()
    authenticated = await api.authenticate(userName, password)
    print(authenticated)
    # Get the refresh token
    print(api.refresh_token)
    if authenticated:
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
authenticated = await api.authenticate(refresh_token)
```