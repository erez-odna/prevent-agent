import json
from flask import Blueprint, Response, request

from validation.validation import validate_schema

# create blueprint for post
post_blueprint = Blueprint("post", __name__)


@post_blueprint.route("/api/patient", methods=["POST"])
@validate_schema("post")
def change_me_handler():
    """Change me

        .. :quickref: Add and item; Add an item to the list

        **Summary:** |br|
        Add an item to the list.

        :reqjson item_name: (Optional) Item name. Maximum length 256.

        :status 200: Success, Item added
        :status 400: BadRequest, missing or invalid request body or body parts
        :status 500: InternalServerError, error happened while doing the activity

        **Example Request:**

        .. sourcecode:: http

            HTTP/1.1 200 OK

            {
                "item_name": "my-name"
            }

        **Example Response:**

        .. sourcecode:: http

            HTTP/1.1 200 OK

            {
                "sys_id": "123456"
            }
    """
    # parse arguments
    req_data = request.get_json()
    cohort = req_data.get("item-name")

    # add code here

    response_json = {"sys_id": patient_id}
    response = json.dumps(response_json, indent=4)
    print(f"added patient with id: {patient_id}")
    return Response(response, status=200, mimetype="application/json")
