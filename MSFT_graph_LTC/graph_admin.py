# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <UserAuthConfigSnippet>
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import (
    MessagesRequestBuilder)
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import (
    SendMailPostRequestBody)
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from configparser import SectionProxy
from uuid import UUID

# from azure.identity import DeviceCodeCredential
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.app_role import AppRole
from msgraph.generated.models.application import Application
from msgraph.generated.service_principals.service_principals_request_builder import ServicePrincipalsRequestBuilder
from msgraph.generated.models.o_auth2_permission_grant import OAuth2PermissionGrant

from msgraph.generated.models.user import User
from msgraph.generated.models.password_profile import PasswordProfile
from msgraph.generated.models.app_role_assignment import AppRoleAssignment
from utils import Utils


class GraphAdmin:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        # tenant_id = self.settings['tenantId']
        self.ovoc_app_id = self.settings['ovoc_app_id']

        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id=client_id, tenant_id="")
        self.user_client = GraphServiceClient(self.device_code_credential, graph_scopes)

    async def assign_roles(self, app_role_assignment_body: AppRoleAssignment):
        print("creating user with json_body: ", app_role_assignment_body)
        result = await (self.user_client.service_principals.by_service_principal_id(self.ovoc_app_id).
                        app_role_assignments.post(app_role_assignment_body))
        return result

    async def get_roles(self):
        result = await self.user_client.service_principals.by_service_principal_id(self.ovoc_app_id).get()
        app_role_dict = {}
        for app_role in result.app_roles:
            app_role_dict[app_role.display_name] = app_role.id
        print(app_role_dict)
        return app_role_dict

    async def get_cdx_users(self):
        cdx_users_dict = {}
        result = await self.get_users()
        for user in result.value:
            if 'cdx' in user.user_principal_name:
                cdx_users_dict[user.user_principal_name] = user.id
        print(cdx_users_dict)
        return cdx_users_dict

    async def get_users(self):
        result = await self.user_client.users.get()
        return result

    async def make_graph_call(self):
        # INSERT YOUR CODE HERE
        return

    async def create_user(self, json_body: dict):
        print("creating user with json_body: ", json_body)

        request_body = User(
            account_enabled=True,
            display_name=json_body.get("display_name"),
            mail_nickname=json_body.get("display_name"),
            user_principal_name=json_body.get("user_principal_name"),
            password_profile=PasswordProfile(
                force_change_password_next_sign_in=False,
                password="0qrY3t90DP",
            ),
        )

        result = await self.user_client.users.post(request_body)
        return result

    async def create_app(self):
        request_body = Application(
            display_name="msgraph_python",
        )
        result = await self.user_client.applications.post(request_body)
        print(result.id)

        request_body = OAuth2PermissionGrant(
            client_id=result.id,
            consent_type="AllPrincipals",
            resource_id=result.id,
            scope="DelegatedPermissionGrant.ReadWrite.All",
        )

        result = await self.user_client.oauth2_permission_grants.post(request_body)
        print('ok')

    async def add_permissions_to_app(self):
        # app_id = input("Enter the app id: ")
        # request_body = OAuth2PermissionGrant(
        #     client_id="7c2f9ea0-60a6-4b1d-9177-0fcd46ce2907",
        #     consent_type="AllPrincipals",
        #     resource_id="b7890da9-130d-41bb-bcec-770348c49745",
        #     scope="openid",
        # )

        result = await self.user_client.oauth2_permission_grants.get()
        print(result)