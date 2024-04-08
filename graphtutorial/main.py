# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <ProgramSnippet>
import asyncio
import configparser
import pprint
from uuid import UUID

from msgraph.generated.models.app_role_assignment import AppRoleAssignment
from msgraph.generated.models.o_data_errors.o_data_error import ODataError

from graph import Graph
from graphtutorial.utils import PermissionType, permissions_mapping, Utils


async def main():
    print('Create AAD Users for Ovoc\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    # await greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Create Users')
        print('2. Assign_roles')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            if choice == 0:
                print('Goodbye...')
            elif choice == 1:
                await create_azure_users(graph)
            elif choice == 2:
                await assign_roles(graph)
            # elif choice == 3:
            #     await send_mail(graph)
            # elif choice == 4:
            #     await make_graph_call(graph)
            # elif choice == 5:
            #     await create_user(graph)
            else:
                print('Invalid choice!\n')
        except ODataError as odata_error:
            print('Error:')
            if odata_error.error:
                print(odata_error.error.code, odata_error.error.message)
# </ProgramSnippet>


# <AssignRoles>
async def assign_roles(graph: Graph):
    config = Utils.get_config("config.cfg")
    ovoc_app_id = config['azure'].get('ovoc_app_id')

    # getting roles dictionary
    get_roles_dict = await graph.get_roles()

    # get the users to apply the roles to
    users_dict = await graph.get_cdx_users()

    # Create role assignments body
    for user_key, user_value_id in users_dict.items():
        print(user_key, user_value_id)
        for role_key, role_value_id in get_roles_dict.items():
            print(role_key, role_value_id)
            if role_key.split('OVOC')[-1].lower() == user_key.split('_')[-1].lower().split('@')[0]:
                role_assignments_body = AppRoleAssignment(
                    principal_id=UUID(str(user_value_id)),
                    resource_id=UUID(str(ovoc_app_id)),
                    app_role_id=UUID(str(role_value_id)),
                )
                print(role_assignments_body)
                assign_role = await graph.assign_roles(app_role_assignment_body=role_assignments_body)
    return
# </AssignRoles>


# <CreateUsers>
async def create_azure_users(graph: Graph):
    sub_choice = -1
    while sub_choice != 0:
        print('Sub-menu for Create Users:')
        print('0. Return to main menu')
        print('1. Create System users')
        print('2. Create SP users')
        print('3. Create Channel users')
        print('4. Create Customer users')
        # Add more sub-options if needed

        try:
            sub_choice = int(input())
        except ValueError:
            sub_choice = -1

        if sub_choice == 0:
            print('Returning to main menu...')
        elif sub_choice == 1:
            await create_users_loop(graph, PermissionType.SYSTEM)
        elif sub_choice == 2:
            await create_users_loop(graph, PermissionType.SP)
        elif sub_choice == 3:
            await create_users_loop(graph, PermissionType.Channel)
        elif sub_choice == 4:
            await create_users_loop(graph, PermissionType.Customer)
        else:
            print('Invalid sub-choice!\n')

# </CreateUsers>


# <MakeGraphCallSnippet>
async def create_users_loop(graph: Graph, permission_ty):
    user_types = permissions_mapping[permission_ty]
    for user_type in user_types:
        print(user_type.value)
        display_name = f'cdx_{permission_ty.value}_{user_type.value}'
        user_json = {"user_principal_name": f'{display_name}@{graph.settings.get('msft_tenant_name')}',
                     "display_name": display_name}
        await graph.create_user(json_body=user_json)
# </MakeGraphCallSnippet>


# Run main
asyncio.run(main())

# </DisplayAccessTokenSnippet>