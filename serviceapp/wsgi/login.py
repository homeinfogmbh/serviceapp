"""User login."""

from functools import partial
from typing import Union
from uuid import UUID

from authlib.integrations.flask_oauth2 import AuthorizationServer
from flask import request, Flask, Response

from wsgilib import JSON, JSONMessage

from serviceapp.exceptions import InvalidPassword, NonceUsed, UserLocked
from serviceapp.oauth2 import FRAMEWORK
from serviceapp.orm import AuthorizationNonce, User
from serviceapp.pin import decode_pin
from serviceapp.pwgen import genpw


__all__ = ["init_oauth_endpoints"]


INVALID_PIN = JSONMessage("Invalid PIN.")


def init_oauth_endpoints(application: Flask) -> None:
    """Adds OAuth endpoints to the respective application."""

    server = FRAMEWORK.authorization_server(application)
    application.route("/client", methods=["POST"])(register_client)
    application.route("/authorize", methods=["POST"], endpoint="authorize_client")(
        partial(authorize_client, server)
    )
    application.route("/oauth/token", methods=["POST"])(server.create_token_response)
    application.route("/oauth/revoke", methods=["POST"])(server.revoke_token)
    application.route("/oauth/introspect", methods=["POST"])(server.introspect_token)


def authorize_client(server: AuthorizationServer) -> Union[Response, JSONMessage]:
    """Login is required since we need to know the current resource owner.
    It can be done with a redirection to the login page, or a login
    form on this authorization page.
    """

    if (nonce := request.form.get("nonce")) is None:
        return JSONMessage("Missing nonce.", status=400)

    try:
        uuid = UUID(nonce)
    except ValueError:
        return JSONMessage("Invalid UUID.", status=400)

    try:
        user = AuthorizationNonce.use(uuid).user
    except NonceUsed:
        return JSONMessage("Invalid nonce.", status=400)

    return server.create_authorization_response(grant_user=user)


def register_client() -> Union[JSON, JSONMessage]:
    """Registers a client."""

    if (pin := request.headers.get("pin")) is None:
        raise JSONMessage("No PIN provided.")

    try:
        ident, passwd = decode_pin(pin)
    except ValueError:
        return INVALID_PIN

    try:
        user = User[ident]
    except User.DoesNotExist:
        return INVALID_PIN

    try:
        user.login(passwd)
    except UserLocked:
        return JSONMessage("This user is locked.", status=401)
    except InvalidPassword:
        return INVALID_PIN

    transaction = FRAMEWORK.models.client.add(user, secret := genpw())
    transaction.commit()
    json = transaction.primary.to_json()
    json["clientSecret"] = secret
    json["authorizationNonce"] = AuthorizationNonce.add(user).uuid.hex
    return JSON(json)
