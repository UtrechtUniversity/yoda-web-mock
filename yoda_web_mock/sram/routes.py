#!/usr/bin/env python3

__copyright__ = 'Copyright (c) 2023-2026, Utrecht University'
__license__ = 'GPLv3, see LICENSE'

import email.utils
import smtplib
import uuid
from email.mime.text import MIMEText
from typing import Any, Dict, List

from flask import Blueprint, jsonify, make_response, request, Response

from yoda_web_mock.sram.database import JSONStorage

blueprint_sram = Blueprint('blueprint_sram', __name__)
storage = JSONStorage()


def _collaboration_to_dict(collaboration: Dict[str, Any],
                           members: List[Dict[str, Any]],
                           invitations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert collaboration data to response format."""
    return {
        "identifier": collaboration['identifier'],
        "name": collaboration['name'],
        "short_name": collaboration['short_name'],
        "collaboration_memberships_count": str(len(members)),
        "invitations_count": str(len(invitations)),
        "collaboration_memberships": [
            {"user": {"uid": m['user_id'], "email": m['user_email']}}
            for m in members
        ]
    }


@blueprint_sram.route('/', methods=['GET'])
def index() -> Response:
    return Response("Yoda mock: sram")


@blueprint_sram.route('/api/collaborations/v1', methods=['POST'])
def create_collaboration() -> Response:
    data = request.json or {}
    collaboration = {
        'identifier': str(uuid.uuid4()).lower(),
        'name': data.get('name', 'Yoda research group'),
        'short_name': data.get('short_name', 'yodagrp')
    }

    collaboration = storage.create_collaboration(collaboration)

    for administrator in data.get('administrators', []):
        storage.add_or_update_member(collaboration['identifier'], str(uuid.uuid4()), administrator)

    # 201 means collaboration has been created
    return make_response(jsonify(_collaboration_to_dict(collaboration, [], [])), 201)


@blueprint_sram.route('/api/collaborations/v1/<path:co_identifier>', methods=['GET'])
def get_collaboration(co_identifier: str) -> Response:
    collaboration = storage.get_collaboration_by_identifier(co_identifier)

    if not collaboration:
        return make_response(jsonify({"message": "Not found"}), 404)

    members = storage.get_members_by_collaboration_id(collaboration['identifier'])
    invitations = storage.get_invitations_by_collaboration_id(collaboration['identifier'])

    # 200 means collaboration exists
    return make_response(jsonify(_collaboration_to_dict(collaboration, members, invitations)), 200)


@blueprint_sram.route('/api/collaborations/v1/<path:co_identifier>/members', methods=['PUT'])
def update_collaboration_membership(co_identifier: str) -> Response:
    data = request.json or {}
    members = data.get('members', [])

    collaboration = storage.get_collaboration_by_identifier(co_identifier)

    if not collaboration:
        return make_response(jsonify({"message": "Not found"}), 404)

    members = request.json.get('members', []) if request.json else []

    try:
        for member in members:
            storage.add_or_update_member(collaboration['identifier'], member['uid'], member['email'])
    except KeyError as e:
        return make_response(jsonify({"error": str(e)}), 400)

    # 201 means successful update of a collaboration membership
    return Response("Update collaboration membership (mocked)", status=201)


@blueprint_sram.route('/api/collaborations/v1/<path:co_identifier>/members/<path:user_uuid>', methods=['DELETE'])
def delete_collaboration_membership(co_identifier: str, user_uuid: str) -> Response:
    collaboration = storage.get_collaboration_by_identifier(co_identifier)

    if not collaboration:
        return make_response(jsonify({"message": "Not found"}), 404)

    if not storage.delete_member(collaboration['identifier'], user_uuid):
        return make_response(jsonify({"message": "Not found"}), 404)

    # 204 means successful deletion of a collaboration membership
    return Response("Delete collaboration membership", status=204)


@blueprint_sram.route('/api/collaborations/v1/<path:co_identifier>', methods=['DELETE'])
def delete_collaboration(co_identifier: str) -> Response:
    if not storage.delete_collaboration(co_identifier):
        return make_response(jsonify({"message": "Not found"}), 404)

    # 204 means successful deletion of a collaboration
    return Response("Delete collaboration (mocked)", status=204)


@blueprint_sram.route('/api/invitations/v1/invitations/<path:co_identifier>', methods=['GET'])
def get_collaboration_invitations(co_identifier: str) -> Response:
    collaboration = storage.get_collaboration_by_identifier(co_identifier)

    if not collaboration:
        return make_response(jsonify({"message": "Not found"}), 404)

    invitations = storage.get_invitations_by_collaboration_id(collaboration['identifier'])
    response = [
        {"status": "open", "invitation": {"identifier": i['invitation_id'], "email": i['email']}}
        for i in invitations
     ]

    # 200 means successful get of open collaboration invitations
    return make_response(jsonify(response), 200)


@blueprint_sram.route('/api/invitations/v1/collaboration_invites', methods=['PUT'])
def put_new_collaboration_invitation() -> Response:
    invitation = request.json or {}

    if 'collaboration_identifier' not in invitation:
        return make_response(jsonify({"message": "Not found"}), 404)

    invitees = invitation.get('invites', [])
    if not invitees:
        return make_response(jsonify({"message": "At least one invitee email is required"}), 400)

    collaboration = storage.get_collaboration_by_identifier(invitation['collaboration_identifier'])
    if not collaboration:
        return make_response(jsonify({"message": "Not found"}), 404)

    invitation_id = str(uuid.uuid4()).lower()
    storage.create_invitation(collaboration['identifier'], invitation_id, invitees[0])

    # Send emails
    message = invitation.get('message', 'You are invited to join a collaboration')
    with smtplib.SMTP("localhost", 25) as smtp:
        msg = MIMEText(str(invitation), 'plain', 'UTF-8')
        msg['Date'] = email.utils.formatdate()
        msg['From'] = "sram-mock@yoda.test"
        msg['To'] = invitees[0]
        msg['Subject'] = message
        smtp.sendmail("sram-mock@yoda.test", invitees, msg.as_string())

    # 201 means successful put of collaboration invitation
    return Response("Put new collaboration invitation (mocked)", status=201)


@blueprint_sram.route('/api/collaborations_services/v1/connect_collaboration_service', methods=['PUT'])
def connect_service_collaboration() -> Response:
    # 201 means successful connection of a service to an existing collaboration
    return Response("Connect a service to an existing collaboration (mocked)", status=201)
