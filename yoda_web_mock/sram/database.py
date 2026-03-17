#!/usr/bin/env python3

__copyright__ = 'Copyright (c) 2026, Utrecht University'
__license__ = 'GPLv3, see LICENSE'

import json
import threading
from typing import Any, Dict, List, Optional

_lock = threading.Lock()

DATABASE = "/var/www/webmock/sram/sram_mock.json"


class JSONStorage:
    """Simple JSON-based storage for SRAM mock data."""
    def _read(self) -> Dict[str, Any]:
        """Read the entire JSON file."""
        try:
            with open(DATABASE, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to read storage file: {str(e)}")

    def _write(self, data: Dict[str, Any]) -> None:
        """Write the entire JSON file."""
        try:
            with open(DATABASE, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to write storage file: {str(e)}")

    def create_collaboration(self, collaboration: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new collaboration."""
        with _lock:
            data = self._read()
            data['collaborations'].append(collaboration)
            self._write(data)
        return collaboration

    def get_collaboration_by_identifier(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get collaboration by identifier."""
        with _lock:
            data = self._read()
            return next((c for c in data['collaborations'] if c['identifier'] == identifier), None)

    def delete_collaboration(self, identifier: str) -> bool:
        """Delete collaboration and its associated data."""
        with _lock:
            data = self._read()
            if not any(c['identifier'] == identifier for c in data['collaborations']):
                return False

            data['collaborations'] = [c for c in data['collaborations'] if c['identifier'] != identifier]
            data['members'] = [m for m in data['members'] if m['collaboration_id'] != identifier]
            data['invitations'] = [i for i in data['invitations'] if i['collaboration_id'] != identifier]
            self._write(data)
        return True

    def add_or_update_member(self, collaboration_id: str, user_id: str, user_email: str) -> Dict[str, Any]:
        """Add or update a collaboration member."""
        with _lock:
            data = self._read()
            member = next(
                (m for m in data['members']
                 if m['collaboration_id'] == collaboration_id and m['user_id'] == user_id),
                None
            )

            if member:
                member['user_email'] = user_email
            else:
                member = {'collaboration_id': collaboration_id, 'user_id': user_id, 'user_email': user_email}
                data['members'].append(member)

            self._write(data)
        return member

    def get_members_by_collaboration_id(self, collaboration_id: str) -> List[Dict[str, Any]]:
        """Get all members of a collaboration."""
        with _lock:
            data = self._read()
            return [m for m in data['members'] if m['collaboration_id'] == collaboration_id]

    def delete_member(self, collaboration_id: str, user_id: str) -> bool:
        """Delete a collaboration member."""
        with _lock:
            data = self._read()
            if not any(m['collaboration_id'] == collaboration_id and m['user_id'] == user_id for m in data['members']):
                return False

            data['members'] = [
                m for m in data['members']
                if not (m['collaboration_id'] == collaboration_id and m['user_id'] == user_id)
            ]
            self._write(data)
        return True

    def create_invitation(self, collaboration_id: str, invitation_id: str, email: str) -> Dict[str, Any]:
        """Create a new invitation."""
        invitation = {'collaboration_id': collaboration_id, 'invitation_id': invitation_id, 'email': email}
        with _lock:
            data = self._read()
            data['invitations'].append(invitation)
            self._write(data)
        return invitation

    def get_invitation_by_id(self, invitation_id: str) -> Optional[Dict[str, Any]]:
        """Get invitation by invitation ID."""
        with _lock:
            data = self._read()
            for inv in data['invitations']:
                if inv['invitation_id'] == invitation_id:
                    return inv
        return None

    def get_invitations_by_collaboration_id(self, collaboration_id: str) -> List[Dict[str, Any]]:
        """Get all invitations of a collaboration."""
        with _lock:
            data = self._read()
            return [i for i in data['invitations'] if i['collaboration_id'] == collaboration_id]

    def delete_invitation(self, invitation_id: str) -> bool:
        """Delete an invitation."""
        with _lock:
            data = self._read()
            if not any(i['invitation_id'] == invitation_id for i in data['invitations']):
                return False

            data['invitations'] = [i for i in data['invitations'] if i['invitation_id'] != invitation_id]
            self._write(data)
        return True
