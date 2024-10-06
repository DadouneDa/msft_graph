permissions_dict =\
    {
        {
          "id": "c79f8feb-a9db-4090-85f9-90d820caa0eb",
          "type": "Scope"
        },
        {
          "id": "bdfbf15f-ee85-4955-8675-146e8e5296b5",
          "type": "Scope"
        },
        {
          "id": "06da0dbc-49e2-44d2-8312-53f166ab848a",
          "type": "Scope"
        },
        {
          "id": "c5366453-9fb0-48a5-a156-24f0c49a4b84",
          "type": "Scope"
        },
        {
          "id": "ea5c4ab0-5a73-4f35-8272-5d5337884e5d",
          "type": "Scope"
        },
        {
          "id": "570282fd-fa5c-430d-a7fd-fc8dc98a9dca",
          "type": "Scope"
        },
        {
          "id": "e383f46e-2787-4529-855e-0e479a3ffac0",
          "type": "Scope"
        },
        {
          "id": "7427e0e9-2fba-42fe-b0c0-848c9e6a8182",
          "type": "Scope"
        },
        {
          "id": "37f7f235-527c-4136-accd-4a02d197296e",
          "type": "Scope"
        },
        {
          "id": "14dad69e-099b-42c9-810b-d002981feec1",
          "type": "Scope"
        },
        {
          "id": "9f9ce928-e038-4e3b-8faf-7b59049a8ddc",
          "type": "Scope"
        },
        {
          "id": "e1fe6dd8-ba31-4d61-89e7-88639da4683d",
          "type": "Scope"
        },
        {
          "id": "204e0828-b5ca-4ad8-b9f3-f32a958e7cc4",
          "type": "Scope"
        },
        {
          "id": "9a5d68dd-52b0-4cc2-bd40-abcf44ac3a30",
          "type": "Role"
        },
        {
          "id": "1bfefb4e-e0b5-418b-a88f-73c46d2cc8e9",
          "type": "Role"
        },
        {
          "id": "7ab1d382-f21e-4acd-a863-ba3e13f7da61",
          "type": "Role"
        },
        {
          "id": "19dbc75e-c2e2-444c-a770-ec69d8559fc7",
          "type": "Role"
        },
        {
          "id": "607c7344-0eed-41e5-823a-9695ebe1b7b0",
          "type": "Role"
        },
        {
          "id": "5256681e-b7f6-40c0-8447-2d9db68797a0",
          "type": "Role"
        },
        {
          "id": "741f803b-c850-494e-b5df-cde7c675a1ca",
          "type": "Role"
        }
}


def run():
    for permission in permissions_dict:
        print(permission['id'])
    pass


if __name__ == '__main__':
    run()