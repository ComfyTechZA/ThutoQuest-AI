"""
Offline-Sync Delta Handler
Manages synchronization of student data in offline/low-connectivity environments.
Handles conflict resolution and delta sync for rural connectivity scenarios.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import hashlib

logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS FOR OFFLINE SYNC
# ============================================================================

class SyncOperation(Enum):
    """Types of sync operations"""
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    MERGE = "MERGE"


class ConflictResolutionStrategy(Enum):
    """Strategies for resolving sync conflicts"""
    LAST_WRITE_WINS = "LAST_WRITE_WINS"
    FIRST_WRITE_WINS = "FIRST_WRITE_WINS"
    SERVER_PRIORITY = "SERVER_PRIORITY"
    CLIENT_PRIORITY = "CLIENT_PRIORITY"


@dataclass
class SyncDelta:
    """Represents a synchronized data change"""
    entity_id: str
    entity_type: str
    operation: SyncOperation
    data: Dict
    timestamp: datetime
    version: int
    client_id: str
    checksum: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'operation': self.operation.value,
            'data': self.data,
            'timestamp': self.timestamp.isoformat(),
            'version': self.version,
            'client_id': self.client_id,
            'checksum': self.checksum,
        }


@dataclass
class SyncConflict:
    """Represents a conflict during sync"""
    entity_id: str
    local_delta: SyncDelta
    remote_delta: SyncDelta
    conflict_type: str
    resolution: Optional[str] = None


# ============================================================================
# OFFLINE DELTA SYNC HANDLER
# ============================================================================

class OfflineDeltaSyncHandler:
    """
    Manages offline-first synchronization with conflict resolution.
    Designed for low-connectivity rural environments.
    """
    
    MAX_RETRIES = 3
    SYNC_BATCH_SIZE = 100
    CONFLICT_THRESHOLD_SECONDS = 5  # Conflicts if within 5 seconds
    
    def __init__(self, persistence_layer=None):
        """
        Initialize sync handler.
        
        Args:
            persistence_layer: Optional persistence layer (file, db, memory)
        """
        self.pending_deltas: List[SyncDelta] = []
        self.synced_deltas: List[SyncDelta] = []
        self.conflicts: List[SyncConflict] = []
        self.entity_versions: Dict[str, int] = {}
        self.persistence_layer = persistence_layer
        self.last_sync_timestamp: Optional[datetime] = None
        self.sync_state = "idle"  # idle, syncing, conflict-resolution
    
    def add_local_change(
        self,
        entity_id: str,
        entity_type: str,
        operation: SyncOperation,
        data: Dict,
        client_id: str
    ) -> SyncDelta:
        """
        Record a local change to be synced.
        
        Args:
            entity_id: Unique entity identifier
            entity_type: Type of entity (e.g., 'quest', 'prediction')
            operation: Type of operation (CREATE, UPDATE, DELETE)
            data: Entity data
            client_id: Client identifier
            
        Returns:
            SyncDelta object
        """
        version = self.entity_versions.get(entity_id, 0) + 1
        self.entity_versions[entity_id] = version
        
        checksum = self._calculate_checksum(data)
        
        delta = SyncDelta(
            entity_id=entity_id,
            entity_type=entity_type,
            operation=operation,
            data=data,
            timestamp=datetime.now(),
            version=version,
            client_id=client_id,
            checksum=checksum
        )
        
        self.pending_deltas.append(delta)
        logger.info(f"Added local change: {entity_type}:{entity_id} (v{version})")
        
        return delta
    
    def get_pending_deltas(self, limit: Optional[int] = None) -> List[SyncDelta]:
        """
        Get pending deltas for sync.
        
        Args:
            limit: Maximum number of deltas to return
            
        Returns:
            List of pending SyncDelta objects
        """
        if limit is None:
            limit = self.SYNC_BATCH_SIZE
        
        return self.pending_deltas[:limit]
    
    def process_remote_deltas(
        self,
        remote_deltas: List[SyncDelta],
        resolution_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.LAST_WRITE_WINS
    ) -> Tuple[List[SyncDelta], List[SyncConflict]]:
        """
        Process incoming remote deltas and detect conflicts.
        
        Args:
            remote_deltas: Deltas received from server
            resolution_strategy: How to resolve conflicts
            
        Returns:
            Tuple of (applied_deltas, conflicts)
        """
        applied = []
        conflicts = []
        
        for remote_delta in remote_deltas:
            # Check for conflicts with pending local changes
            conflict = self._detect_conflict(remote_delta)
            
            if conflict:
                conflicts.append(conflict)
                # Apply resolution strategy
                resolved_delta = self._resolve_conflict(
                    conflict,
                    resolution_strategy
                )
                if resolved_delta:
                    applied.append(resolved_delta)
                    self._remove_conflicting_pending_delta(remote_delta.entity_id)
            else:
                applied.append(remote_delta)
                # Update local version tracking
                self.entity_versions[remote_delta.entity_id] = remote_delta.version
        
        logger.info(f"Processed {len(remote_deltas)} remote deltas: "
                   f"{len(applied)} applied, {len(conflicts)} conflicts")
        
        return applied, conflicts
    
    def apply_sync_result(
        self,
        successful_deltas: List[SyncDelta],
        failed_deltas: List[Tuple[SyncDelta, str]] = None
    ) -> Dict:
        """
        Apply results of successful sync.
        
        Args:
            successful_deltas: Deltas that were successfully synced
            failed_deltas: Deltas that failed [(delta, error_message)]
            
        Returns:
            Sync result summary
        """
        # Remove successfully synced deltas from pending
        for delta in successful_deltas:
            if delta in self.pending_deltas:
                self.pending_deltas.remove(delta)
                self.synced_deltas.append(delta)
        
        # Keep failed deltas in pending (will retry)
        failed_count = len(failed_deltas) if failed_deltas else 0
        
        self.last_sync_timestamp = datetime.now()
        
        result = {
            'timestamp': self.last_sync_timestamp.isoformat(),
            'successful': len(successful_deltas),
            'failed': failed_count,
            'pending': len(self.pending_deltas),
            'conflicts': len(self.conflicts),
        }
        
        logger.info(f"Sync result: {result}")
        return result
    
    def resolve_conflicts_manually(
        self,
        conflict: SyncConflict,
        winning_delta: SyncDelta
    ) -> bool:
        """
        Manually resolve a conflict by selecting the winning delta.
        
        Args:
            conflict: The conflict to resolve
            winning_delta: The delta that should win
            
        Returns:
            True if resolved successfully
        """
        if winning_delta not in [conflict.local_delta, conflict.remote_delta]:
            logger.error("Winning delta must be either local or remote")
            return False
        
        conflict.resolution = "MANUAL"
        self.conflicts.remove(conflict)
        
        logger.info(f"Manually resolved conflict for {conflict.entity_id}")
        return True
    
    def get_sync_status(self) -> Dict:
        """
        Get current sync status.
        
        Returns:
            Status dictionary
        """
        return {
            'state': self.sync_state,
            'pending_deltas': len(self.pending_deltas),
            'synced_deltas': len(self.synced_deltas),
            'conflicts': len(self.conflicts),
            'last_sync': self.last_sync_timestamp.isoformat() if self.last_sync_timestamp else None,
            'entity_versions': self.entity_versions,
        }
    
    # ========================================================================
    # PRIVATE HELPERS
    # ========================================================================
    
    def _calculate_checksum(self, data: Dict) -> str:
        """Calculate checksum for data integrity"""
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    def _detect_conflict(self, remote_delta: SyncDelta) -> Optional[SyncConflict]:
        """Detect if remote delta conflicts with pending local deltas"""
        for local_delta in self.pending_deltas:
            if local_delta.entity_id == remote_delta.entity_id:
                # Check if operations overlap (conflict)
                time_diff = abs(
                    (remote_delta.timestamp - local_delta.timestamp).total_seconds()
                )
                
                if time_diff < self.CONFLICT_THRESHOLD_SECONDS:
                    return SyncConflict(
                        entity_id=remote_delta.entity_id,
                        local_delta=local_delta,
                        remote_delta=remote_delta,
                        conflict_type="CONCURRENT_MODIFICATION"
                    )
        
        return None
    
    def _resolve_conflict(
        self,
        conflict: SyncConflict,
        strategy: ConflictResolutionStrategy
    ) -> Optional[SyncDelta]:
        """Resolve conflict based on strategy"""
        if strategy == ConflictResolutionStrategy.LAST_WRITE_WINS:
            winner = (conflict.remote_delta 
                     if conflict.remote_delta.timestamp > conflict.local_delta.timestamp
                     else conflict.local_delta)
        elif strategy == ConflictResolutionStrategy.FIRST_WRITE_WINS:
            winner = (conflict.local_delta 
                     if conflict.local_delta.timestamp < conflict.remote_delta.timestamp
                     else conflict.remote_delta)
        elif strategy == ConflictResolutionStrategy.SERVER_PRIORITY:
            winner = conflict.remote_delta
        elif strategy == ConflictResolutionStrategy.CLIENT_PRIORITY:
            winner = conflict.local_delta
        else:
            winner = conflict.remote_delta  # Default
        
        conflict.resolution = strategy.value
        return winner
    
    def _remove_conflicting_pending_delta(self, entity_id: str):
        """Remove pending delta for entity"""
        self.pending_deltas = [
            d for d in self.pending_deltas
            if d.entity_id != entity_id
        ]
