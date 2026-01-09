"""
Audit Log Module

This module provides cryptographic audit logging for Foliorank operations.
All portfolio planning and simulation results are logged with SHA256 hashes
to enable future verification and reproducibility proof.
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List


class AuditLog:
    """
    Cryptographic audit log for Foliorank operations.

    This class maintains tamper-evident logs of all portfolio operations,
    enabling future verification that results were produced according to
    the defined rules and constraints.
    """

    def __init__(self):
        self.entries: List[Dict[str, Any]] = []
        self.agent_id = "controlled_agent_v0"
        self.mcp_version = "v0.1"
        self.schema_version = "portfolio_v1"

    def log(self, description: str, portfolio: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and store an audit entry for a complete operation cycle.

        Args:
            description: Original user input description
            portfolio: Generated portfolio specification
            result: Simulation results

        Returns:
            Complete audit entry dictionary with hash
        """
        # Create the payload for hashing (excludes timestamp and agent_id)
        hash_payload = {
            "input_description": description,
            "portfolio": portfolio,
            "simulation_result": result,
            "mcp_version": self.mcp_version,
            "schema_version": self.schema_version
        }

        # Compute SHA256 hash of canonical JSON
        hash_value = self._compute_hash(hash_payload)

        # Create complete audit entry
        audit_entry = {
            "timestamp": self._get_current_timestamp(),
            "agent_id": self.agent_id,
            "input_description": description,
            "portfolio": portfolio,
            "simulation_result": result,
            "mcp_version": self.mcp_version,
            "schema_version": self.schema_version,
            "hash": hash_value
        }

        # Store the entry
        self.entries.append(audit_entry)

        return audit_entry

    def _compute_hash(self, payload: Dict[str, Any]) -> str:
        """
        Compute SHA256 hash of the canonical JSON representation.

        Args:
            payload: Dictionary to hash (must be JSON-serializable)

        Returns:
            Hexadecimal SHA256 hash string
        """
        # Create canonical JSON with sorted keys for deterministic hashing
        canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    def _get_current_timestamp(self) -> str:
        """
        Get current timestamp in ISO 8601 format with timezone.

        Returns:
            Timestamp string in format: 2026-01-10T12:34:56Z
        """
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    def get_entries(self) -> List[Dict[str, Any]]:
        """
        Retrieve all audit entries.

        Returns:
            List of audit entry dictionaries
        """
        return self.entries.copy()

    def get_entry_by_hash(self, hash_value: str) -> Dict[str, Any]:
        """
        Retrieve audit entry by its hash.

        Args:
            hash_value: SHA256 hash to search for

        Returns:
            Audit entry dictionary if found

        Raises:
            ValueError: If no entry found with the given hash
        """
        for entry in self.entries:
            if entry["hash"] == hash_value:
                return entry
        raise ValueError(f"No audit entry found for hash: {hash_value}")

    def verify_hash(self, entry: Dict[str, Any]) -> bool:
        """
        Verify that an audit entry's hash matches its content.

        Args:
            entry: Audit entry dictionary to verify

        Returns:
            True if hash is valid, False otherwise
        """
        # Recreate the hash payload from the entry
        hash_payload = {
            "input_description": entry["input_description"],
            "portfolio": entry["portfolio"],
            "simulation_result": entry["simulation_result"],
            "mcp_version": entry["mcp_version"],
            "schema_version": entry["schema_version"]
        }

        # Compute expected hash
        expected_hash = self._compute_hash(hash_payload)

        # Compare with stored hash
        return expected_hash == entry["hash"]