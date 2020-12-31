# Destatis Genesis REST API Python Client

## Usability Note

In my opinion the Genesis REST API is currently more suited for
expert users. I highly reccomend users that want convenient quick access
to statistical data to use [datenguide](https://datengui.de/) instead.
Datenguide predates genesis' RESTful API and fetches **all** the data from
destatis using its older SOAP API and provides it to users in the form
of a GraphQL API. For particularly easy use I recommend also the
[python](https://github.com/CorrelAid/datenguide-python)
and [R](https://github.com/CorrelAid/datenguideR) clients available for datenguide API.

The main purpouse of this client is to keep up to date with the official destatis API
development with the hope that eventually the official API will also be the one
that can be used most easily by a wide range of users.

### Disclaimer

I'm also a core developer of the datenguide python client although no commercial interests
are involved in the project.

## Destatis Genesis API documentation

Official documentation of the API in pdf form is available in [German](https://www.regionalstatistik.de/genesis/misc/GENESIS-Webservices_Einfuehrung.pdf)
and [English](https://www-genesis.destatis.de/genesis/misc/GENESIS-Webservices_Introduction.pdf). The RESTful API consists of roughly
the first 100 pages of the documenation.

There is also a technichal API description in the form of a *.wadl* [file](https://www-genesis.destatis.de/genesisWS/rest/2020/application.wadl), which
is used by this client in order to mediate a first systematic overvieww of the API. The *.wadl* file contains all available parameters for all the endpoints
including their defaults which helps to get an overview. It does not, however, contain descriptions of the parameters.

## Installation instructions

Install python requirements.

> pip install -r requirements.txt

If not already registered create a personal [regionalstatistik account](https://www.regionalstatistik.de/genesis/online?Menu=RegistrierungForm&REGKUNDENTYP=001#abreadcrumb).
In the project folder create a `.secrets.toml` file containing
```
genesis_usr = "<your_username>"
genesis_pwd = "<your_password>"
```
This setting will provide the credentials automatically to all endpoints that require them. Otherwise they can still be passed manually to the endpoints.

## Usage

To use the client instantiate an instance

```python
from client import GenesisClient

gc = GenesisClient()
```

Afterwards it currently provides three methods
- `.api_info`
- `.get_json`
- `.get_file`

For a minimal usage examples please see `example.ipynb`.

## Notebook kernel installation 

It is often very convenient to use the client from within a jupyter notebook.
This can be setup as follows.

1. Install ipykernel with `pip install ipykernel`
2. Create the kernel for instance with the name genesispy with `python -m ipykernel install --user --name genesispy`
3. Refresh the browser tab running  jupyter