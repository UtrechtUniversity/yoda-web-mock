#!/usr/bin/env python3

__copyright__ = 'Copyright (c) 2023, Utrecht University'
__license__ = 'GPLv3, see LICENSE'

import time
import uuid

from flask import Blueprint, jsonify, make_response, Response

blueprint_sram = Blueprint('blueprint_sram', __name__)


@blueprint_sram.route('/', methods=['GET'])
def index() -> Response:
    return Response("Yoda mock: sram")


@blueprint_sram.route('/api/collaborations/v1', methods=['POST'])
def create_collaboration() -> Response:
    co_identifier = str(uuid.uuid4()).lower()
    created_at = int(time.time())

    response = {
      "id": 999,
      "identifier": co_identifier,
      "name": "Yoda research group",
      "short_name": "yodagrp",
      "description": "Yoda SRAM research group.",
      "global_urn": "yoda:yodagrp",
      "status": "active",
      "organisation_id": 666,
      "uuid4": co_identifier,
      "website_url": "https://portal.yoda.test",
      "disable_join_requests": False,
      "disclose_member_information": True,
      "disclose_email_information": True,
      "expiry_date": created_at,
      "created_at": created_at,
      "collaboration_memberships_count": "0",
      "invitations_count": "1",
      "last_activity_date": created_at,
      "groups": [],
      "tags": []
    }

    # 201 means collaboration has been created
    return make_response(jsonify(response), 201)


@blueprint_sram.route('/api/collaborations/v1/<path:co_identifier>', methods=['GET'])
def get_collaboration(co_identifier):
    created_at = int(time.time())
    response = {
      "id": 999,
      "identifier": co_identifier,
      "name": "Yoda research group",
      "short_name": "yodagrp",
      "description": "Yoda SRAM research group.",
      "global_urn": "yoda:yodagrp",
      "status": "active",
      "organisation_id": 666,
      "uuid4": co_identifier,
      "website_url": "https://portal.yoda.test",
      "disable_join_requests": False,
      "disclose_member_information": True,
      "disclose_email_information": True,
      "expiry_date": created_at,
      "created_at": created_at,
      "collaboration_memberships_count": "0",
      "invitations_count": "1",
      "last_activity_date": created_at,
      "collaboration_memberships": [
        {
          "user": {
            "uid": "urn:researcher",
            "email": "researcher@yoda.test"
          }
        },
        {
          "user": {
            "uid": "urn:datamanager",
            "email": "datamanager@yoda.test"
          }
        },
        {
          "user": {
            "uid": "urn:functionaladminpriv",
            "email": "functionaladminpriv@yoda.test"
          }
        },
        {
          "user": {
            "uid": "urn:viewer",
            "email": "viewer@yoda.test"
          }
        }
      ]
    }

    # 200 means collaboration exists
    return make_response(jsonify(response), 200)


@blueprint_sram.route('/api/collaborations/v1/<path:co_identifier>/members', methods=['PUT'])
def update_collaboration_membership(co_identifier):
    # 201 means successful update of a collaboration membership
    return Response("Update collaboration membership (mocked)", status=201)


@blueprint_sram.route('/api/collaborations/v1/<path:co_identifier>/members/<path:user_uuid>', methods=['DELETE'])
def delete_collaboration_membership(co_identifier, user_uuid):
    # 204 means successful deletion of a collaboration membership
    return Response("Delete collaboration membership (mocked)", status=204)


@blueprint_sram.route('/api/collaborations/v1/<path:co_identifier>', methods=['DELETE'])
def delete_collaboration(co_identifier):
    # 204 means successful deletion of a collaboration
    return Response("Delete collaboration (mocked)", status=204)
