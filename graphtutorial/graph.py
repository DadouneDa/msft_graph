# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <UserAuthConfigSnippet>
from configparser import SectionProxy
from uuid import UUID

# from azure.identity import DeviceCodeCredential
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.service_principals.service_principals_request_builder import ServicePrincipalsRequestBuilder
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import (
    MessagesRequestBuilder)
from msgraph.generated.models.user import User
from msgraph.generated.models.password_profile import PasswordProfile
from msgraph.generated.models.app_role_assignment import AppRoleAssignment

from graphtutorial.utils import Utils


class Graph:
    settings: SectionProxy
    # device_code_credential: DeviceCodeCredential
    client_credential: ClientSecretCredential
    user_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        # client_id = self.settings['clientId']
        # tenant_id = self.settings['tenantId']
        # client_secret = self.settings['clientSecret']
        # OVOC_app_id = self.settings['OVOC_app_id']

        config = Utils.get_config("config.cfg")
        client_id = config['azure'].get('client_id')
        tenant_id = config['azure'].get('tenant_id')
        client_secret = config['azure'].get('client_secret')
        self.ovoc_app_id = config['azure'].get('ovoc_app_id')
        # self.client_credential = ClientSecretCredential(client_id, tenant_id = tenant_id)
        self.client_credential = ClientSecretCredential(tenant_id=tenant_id,
                                                        client_id=client_id,
                                                        client_secret=client_secret)
        # self.user_client = GraphServiceClient(self.client_credential, graph_scopes)
        self.user_client = GraphServiceClient(self.client_credential)
# </UserAuthConfigSnippet>

    # <GetUserTokenSnippet>
    async def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.client_credential.get_token(graph_scopes)
        return access_token.token
    # </GetUserTokenSnippet>

    # <GetUserSnippet>
    async def get_user(self):
        # Only request specific properties using $select
        query_params = UserItemRequestBuilder.UserItemRequestBuilderGetQueryParameters(
            select=['displayName', 'mail', 'userPrincipalName']
        )

        request_config = UserItemRequestBuilder.UserItemRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        user = await self.user_client.me.get(request_configuration=request_config)
        return user
    # </GetUserSnippet>

    # <GetInboxSnippet>
    async def get_inbox(self):
        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            # Only request specific properties
            select=['from', 'isRead', 'receivedDateTime', 'subject'],
            # Get at most 25 results
            top=25,
            # Sort by received time, newest first
            orderby=['receivedDateTime DESC']
        )
        request_config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
            query_parameters= query_params
        )

        messages = await self.user_client.me.mail_folders.by_mail_folder_id('inbox').messages.get(
                request_configuration=request_config)
        return messages
    # </GetInboxSnippet>

    # <SendMailSnippet>
    async def assign_roles(self, app_role_assignment_body: AppRoleAssignment):
        print("creating user with json_body: ", app_role_assignment_body)
        result = await (self.user_client.service_principals.by_service_principal_id(self.ovoc_app_id).
                        app_role_assignments.post(app_role_assignment_body))
        return result
    # </SendMailSnippet>

    async def get_roles(self):
        result = await self.user_client.service_principals.by_service_principal_id( self.ovoc_app_id).get()
        app_role_dict = {}
        for app_role in result.app_roles:
            app_role_dict[app_role.display_name] = app_role.id
        print(app_role_dict)
        return app_role_dict
    # </SendMailSnippet>

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

    # </SendMailSnippet>


    # <MakeGraphCallSnippet>
    async def make_graph_call(self):
        # INSERT YOUR CODE HERE
        return
    # </MakeGraphCallSnippet>

    # create user:
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