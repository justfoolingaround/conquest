# Python TLS Client

This project is "forked" from [here](https://github.com/FlorianREGAZ/Python-Tls-Client).

## Read before usage

- This project is not stable, it has known issues with **memory leaks**.
- This project is not suitable for replacing the HTTP clients that you currently may use, even though the syntax has been made similar to [`python-requests`](https://github.com/psf/requests).
- This project **does not** support streaming responses. 
    - This project is a wraps [bogdanfinn/tls-client](https://github.com/bogdanfinn/tls-client) **is all**.
    - This also implies that you **cannot** track progress of your downloads.
- Multipart-form is supported.

    ```py
    import tls_client

    from tls_client.utils import MultipartEncoder, TLSClients

    session = tls_client.Session(settings=tls_client.TLSSettings(client_identifier=TLSClients.Firefox_110))

    encoder = MultipartEncoder({
            'field': ('file_name', b'{"a": "b"}', 'application/json',
                      {'X-My-Header': 'my-value'})
    ])

    response = session.post("https://abc.xyz/", data=encoder.to_string(), headers={'Content-Type': encoder.content_type}))
    ```

## So, just when to use this project?

- This project is a **sure-fire** bypass to Cloudflare IUAM if your browser does not encounter it.
- This project makes it difficult for site owners to filter out automated requests, given that your request headers and content don't give anything away.

## What this "fork" means

This "fork" could potentially escalate into a fully Pythonic TLS client in the near future and the main purpose of this fork is to track issues and solve existing issues.

## Usage

```py
>>> import tls_client
...
>>> from tls_client.utils import TLSClients
...
>>> settings = tls_client.TLSSettings(client_identifier=TLSClients.Firefox_110)
...
>>> session = tls_client.Session(settings=settings)
...
>>> session.get("https://www.crunchyroll.com/")
<Response [HTTP/2.0 / 200]>
```


## Similar projects, for reference

- [tlsfuzzer/tlslite-ng](https://github.com/tlsfuzzer/tlslite-ng)
- [nealyip/tls_client_handshake_pure_python](https://github.com/nealyip/tls_client_handshake_pure_python)