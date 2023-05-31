#!/usr/bin/env python3

__copyright__ = 'Copyright (c) 2023, Utrecht University'
__license__ = 'GPLv3, see LICENSE'

from flask import Blueprint, Response

blueprint_datacite = Blueprint('blueprint_datacite', __name__)


@blueprint_datacite.route('/', methods=['GET'])
def index():
    return Response("Yoda mock: Datacite")


@blueprint_datacite.route('/doi/<path:doi>', methods=['GET'])
def check_doi_availability(doi):
    return Response("Check DOI availability response (mocked)",
                    status=404)  # 404 means the DOI is available


@blueprint_datacite.route('/dois/<path:doi>', methods=['PUT'])
def update_doi_url(doi):
    # 200 means successful update
    return Response("Update DOI response (mocked)", status=200)


@blueprint_datacite.route('/dois', methods=['POST'])
def register_doi_url():
    # 201 means URL has been updated
    return Response("Register DOI response (mocked)", status=201)
