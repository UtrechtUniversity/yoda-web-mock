#!/usr/bin/env python3

__copyright__ = 'Copyright (c) 2023, Utrecht University'
__license__ = 'GPLv3, see LICENSE'

from flask import Blueprint, Response

blueprint_datacite = Blueprint('blueprint_datacite', __name__)


@blueprint_datacite.route('/', methods=['GET'])
def index():
    return Response("Yoda mock: Datacite")


@blueprint_datacite.route('/doi/<doi>', methods=['GET'])
def check_doi_availability(doi):
    return Response("Check DOI availability response (mocked)",
                    status=404)  # 404 means the DOI is available


@blueprint_datacite.route('/metadata/<doi>', methods=['PUT'])
def register_doi_metadata(doi):
    return Response("Register DOI metadata response (mocked)",
                    status=201)  # 201 means metadata has been updated


@blueprint_datacite.route('/metadata/<doi>', methods=['DELETE'])
def delete_doi_metadata(doi):
    # 200 means metadata has been removed
    return Response("Delete metadata (mocked)", status=200)


@blueprint_datacite.route('/doi/<doi>', methods=['PUT'])
def register_doi_url(doi):
    # 201 means URL has been updated
    return Response("Register DOI response (mocked)", status=201)
