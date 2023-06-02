#!/usr/bin/env python3

__copyright__ = 'Copyright (c) 2023, Utrecht University'
__license__ = 'GPLv3, see LICENSE'

import time
import uuid

from flask import Blueprint, Response, jsonify, make_response

blueprint_sram = Blueprint('blueprint_sram', __name__)


@blueprint_sram.route('/', methods=['GET'])
def index() -> Response:
    return Response("Yoda mock: sram")


@blueprint_sram.route('/api/collaborations/v1', methods=['POST'])
def create_collaboration() -> Response:
    identifier = str(uuid.uuid4()).upper()
    created_at = int(time.time())

    response = {
      "id": 999,
      "identifier": identifier,
      "name": "Yoda research group",
      "short_name": "yodagrp",
      "description": "Yoda SRAM research group.",
      "global_urn": "yoda:yodagrp",
      "status": "active",
      "organisation_id": 666,
      "uuid4": identifier,
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
