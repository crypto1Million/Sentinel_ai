###############################################################################
# Imports
###############################################################################

from __future__ import annotations

import os
import json
import copy
import time
import logging

from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from dataclasses import (
    dataclass,
    field,
)

from enum import (
    Enum,
    IntEnum,
    auto,
)

import yaml

###############################################################################
# Constants
###############################################################################

DEFAULT_CONFIG_VERSION = "1.0.0"

DEFAULT_ENVIRONMENT = "development"

DEFAULT_GRAPH_NAME = "WalletDNA"

DEFAULT_MAX_NODES = 5_000_000

DEFAULT_MAX_EDGES = 50_000_000

DEFAULT_CACHE_SIZE = 50000

DEFAULT_THREAD_COUNT = 8

DEFAULT_MAX_TRAVERSAL_DEPTH = 50

DEFAULT_SNAPSHOT_INTERVAL = 300

DEFAULT_HEALTH_CHECK_INTERVAL = 30

DEFAULT_EXPORT_FORMAT = "json"

CONFIG_DIRECTORY = "config"

CONFIG_FILE_NAME = "wallet_dna_graph.json"

BACKUP_DIRECTORY = "config/backups"

SUPPORTED_FORMATS = {

    "json",

    "yaml",

    "yml",

}

###############################################################################
# Enums
###############################################################################

class Environment(Enum):
    """
    Runtime environment.
    """

    DEVELOPMENT = "development"

    TESTING = "testing"

    STAGING = "staging"

    PRODUCTION = "production"


###############################################################################


class GraphMode(Enum):
    """
    Graph execution mode.
    """

    STANDARD = auto()

    PERFORMANCE = auto()

    MEMORY_OPTIMIZED = auto()

    DEBUG = auto()


###############################################################################


class CacheMode(Enum):
    """
    Cache strategy.
    """

    NONE = auto()

    MEMORY = auto()

    REDIS = auto()

    HYBRID = auto()


###############################################################################


class StorageMode(Enum):
    """
    Storage backend.
    """

    MEMORY = auto()

    SQLITE = auto()

    POSTGRES = auto()

    NEO4J = auto()


###############################################################################


class TraversalMode(Enum):
    """
    Traversal algorithm preference.
    """

    BFS = auto()

    DFS = auto()

    AUTO = auto()

###############################################################################
# GraphConfig
###############################################################################

class GraphConfig:
    """
    Central configuration manager for the Wallet DNA Graph Engine.

    Responsible for:

    • Loading configuration
    • Environment handling
    • Runtime settings
    • Cache settings
    • Storage settings
    • Validation
    • Import / Export
    • Feature flags
    """


###############################################################################
# Configuration Models
###############################################################################

@dataclass(slots=True)
class GraphSettings:
    """
    Core graph configuration.
    """

    graph_name: str = DEFAULT_GRAPH_NAME

    graph_version: str = DEFAULT_CONFIG_VERSION

    graph_mode: GraphMode = GraphMode.STANDARD

    max_nodes: int = DEFAULT_MAX_NODES

    max_edges: int = DEFAULT_MAX_EDGES

    directed_graph: bool = True

    weighted_graph: bool = True

    multigraph: bool = False

    auto_cleanup: bool = True

    cleanup_interval: int = 600


###############################################################################


@dataclass(slots=True)
class TraversalSettings:
    """
    Graph traversal configuration.
    """

    traversal_mode: TraversalMode = TraversalMode.AUTO

    max_depth: int = DEFAULT_MAX_TRAVERSAL_DEPTH

    max_queue_size: int = 100000

    max_path_length: int = 100

    allow_cycles: bool = False

    timeout_seconds: int = 30

    parallel_traversal: bool = True

    batch_size: int = 1000


###############################################################################


@dataclass(slots=True)
class StorageSettings:
    """
    Graph storage configuration.
    """

    storage_mode: StorageMode = StorageMode.MEMORY

    database_url: Optional[str] = None

    auto_persist: bool = True

    persist_interval: int = 300

    compression: bool = True

    backup_enabled: bool = True

    backup_interval: int = 3600

    backup_directory: str = BACKUP_DIRECTORY


###############################################################################


@dataclass(slots=True)
class CacheSettings:
    """
    Cache configuration.
    """

    cache_mode: CacheMode = CacheMode.MEMORY

    cache_size: int = DEFAULT_CACHE_SIZE

    cache_ttl: int = 3600

    preload_cache: bool = True

    cache_statistics: bool = True

    eviction_policy: str = "LRU"

    redis_url: Optional[str] = None


###############################################################################


@dataclass(slots=True)
class RuntimeSettings:
    """
    Runtime configuration.
    """

    worker_threads: int = DEFAULT_THREAD_COUNT

    snapshot_interval: int = DEFAULT_SNAPSHOT_INTERVAL

    health_check_interval: int = DEFAULT_HEALTH_CHECK_INTERVAL

    auto_snapshot: bool = True

    monitoring_enabled: bool = True

    diagnostics_enabled: bool = True

    graceful_shutdown: bool = True

    shutdown_timeout: int = 30


###############################################################################


@dataclass(slots=True)
class StatisticsSettings:
    """
    Statistics configuration.
    """

    collect_statistics: bool = True

    collect_centrality: bool = True

    collect_clusters: bool = True

    collect_performance: bool = True

    collect_runtime: bool = True

    export_format: str = DEFAULT_EXPORT_FORMAT

    auto_export: bool = False


###############################################################################


@dataclass(slots=True)
class SecuritySettings:
    """
    Security configuration.
    """

    validate_wallet_addresses: bool = True

    validate_token_addresses: bool = True

    validate_edges: bool = True

    enable_checksums: bool = True

    enable_audit_logs: bool = True

    encryption_enabled: bool = False

    api_key_required: bool = False


###############################################################################


@dataclass(slots=True)
class FeatureFlags:
    """
    Enable / Disable Wallet DNA modules.
    """

    wallet_dna: bool = True

    funding_graph: bool = True

    deployer_graph: bool = True

    statistics: bool = True

    runtime_monitor: bool = True

    snapshots: bool = True

    diagnostics: bool = True

    cache: bool = True

    storage: bool = True

    replay: bool = True


###############################################################################


@dataclass(slots=True)
class GraphConfiguration:
    """
    Master Wallet DNA configuration.
    """

    graph: GraphSettings = field(
        default_factory=GraphSettings
    )

    traversal: TraversalSettings = field(
        default_factory=TraversalSettings
    )

    storage: StorageSettings = field(
        default_factory=StorageSettings
    )

    cache: CacheSettings = field(
        default_factory=CacheSettings
    )

    runtime: RuntimeSettings = field(
        default_factory=RuntimeSettings
    )

    statistics: StatisticsSettings = field(
        default_factory=StatisticsSettings
    )

    security: SecuritySettings = field(
        default_factory=SecuritySettings
    )

    features: FeatureFlags = field(
        default_factory=FeatureFlags
    )

###############################################################################
# Initialization
###############################################################################

def __init__(
    self,
    config_file: Optional[Union[str, Path]] = None,
    environment: Optional[Union[str, Environment]] = None,
    logger: Optional[logging.Logger] = None,
):
    """
    Initialize Graph Configuration Manager.

    Parameters
    ----------
    config_file : str | Path, optional
        External configuration file.

    environment : str | Environment, optional
        Runtime environment.

    logger : logging.Logger, optional
        Logger instance.
    """

    ###########################################################################
    # Core
    ###########################################################################

    self.logger = logger or logging.getLogger(__name__)

    self.config_file = (

        Path(config_file)

        if config_file

        else None

    )

    self.environment = (

        Environment(environment)

        if isinstance(environment, str)

        else environment

    )

    ###########################################################################
    # Configuration Object
    ###########################################################################

    self.config = GraphConfiguration()

    ###########################################################################
    # Initialization
    ###########################################################################

    self._load_defaults()

    self._load_environment()

    self._load_config_file()

    self._validate_configuration()


###############################################################################


def _load_defaults(self) -> None:
    """
    Load default Wallet DNA configuration.
    """

    self.config = GraphConfiguration()

    self.logger.info(
        "Loaded default graph configuration."
    )


###############################################################################


def _load_environment(self) -> None:
    """
    Load configuration from runtime environment.
    """

    ###########################################################################
    # Environment
    ###########################################################################

    if self.environment is None:

        env = os.getenv(

            "GRAPH_ENV",

            DEFAULT_ENVIRONMENT,

        )

        self.environment = Environment(env)

    ###########################################################################
    # Environment Overrides
    ###########################################################################

    self.config.runtime.worker_threads = int(

        os.getenv(

            "GRAPH_THREADS",

            self.config.runtime.worker_threads,

        )

    )

    self.config.cache.cache_size = int(

        os.getenv(

            "GRAPH_CACHE_SIZE",

            self.config.cache.cache_size,

        )

    )

    self.config.storage.database_url = os.getenv(

        "GRAPH_DATABASE_URL",

        self.config.storage.database_url,

    )

    self.logger.info(

        "Environment configuration loaded (%s).",

        self.environment.value,

    )


###############################################################################


def _load_config_file(self) -> None:
    """
    Load configuration from JSON or YAML.
    """

    if self.config_file is None:

        return

    if not self.config_file.exists():

        self.logger.warning(

            "Configuration file not found: %s",

            self.config_file,

        )

        return

    ###########################################################################
    # JSON
    ###########################################################################

    if self.config_file.suffix.lower() == ".json":

        with open(

            self.config_file,

            "r",

            encoding="utf-8",

        ) as file:

            data = json.load(file)

    ###########################################################################
    # YAML
    ###########################################################################

    elif self.config_file.suffix.lower() in {

        ".yaml",

        ".yml",

    }:

        with open(

            self.config_file,

            "r",

            encoding="utf-8",

        ) as file:

            data = yaml.safe_load(file)

    else:

        raise ValueError(

            "Unsupported configuration format."

        )

    ###########################################################################
    # Merge
    ###########################################################################

    self.update(data)

    self.logger.info(

        "Configuration loaded from %s",

        self.config_file,

    )


###############################################################################


def _validate_configuration(self) -> None:
    """
    Validate configuration values.
    """

    ###########################################################################
    # Nodes
    ###########################################################################

    if self.config.graph.max_nodes <= 0:

        raise ValueError(

            "max_nodes must be > 0"

        )

    ###########################################################################
    # Edges
    ###########################################################################

    if self.config.graph.max_edges <= 0:

        raise ValueError(

            "max_edges must be > 0"

        )

    ###########################################################################
    # Cache
    ###########################################################################

    if self.config.cache.cache_size < 0:

        raise ValueError(

            "cache_size cannot be negative"

        )

    ###########################################################################
    # Threads
    ###########################################################################

    if self.config.runtime.worker_threads <= 0:

        raise ValueError(

            "worker_threads must be > 0"

        )

    ###########################################################################
    # Traversal
    ###########################################################################

    if self.config.traversal.max_depth <= 0:

        raise ValueError(

            "Traversal depth must be > 0"

        )

    ###########################################################################
    # Snapshot
    ###########################################################################

    if self.config.runtime.snapshot_interval <= 0:

        raise ValueError(

            "Snapshot interval must be > 0"

        )

    self.logger.info(

        "Graph configuration validated successfully."

    )

###############################################################################
# Graph Configuration
###############################################################################

def graph_settings(self) -> GraphSettings:
    """
    Return graph configuration.

    Returns
    -------
    GraphSettings
    """

    return self.config.graph


###############################################################################


def traversal_settings(self) -> TraversalSettings:
    """
    Return traversal configuration.

    Returns
    -------
    TraversalSettings
    """

    return self.config.traversal


###############################################################################


def storage_settings(self) -> StorageSettings:
    """
    Return storage configuration.

    Returns
    -------
    StorageSettings
    """

    return self.config.storage


###############################################################################


def cache_settings(self) -> CacheSettings:
    """
    Return cache configuration.

    Returns
    -------
    CacheSettings
    """

    return self.config.cache


###############################################################################


def runtime_settings(self) -> RuntimeSettings:
    """
    Return runtime configuration.

    Returns
    -------
    RuntimeSettings
    """

    return self.config.runtime


###############################################################################


def statistics_settings(self) -> StatisticsSettings:
    """
    Return statistics configuration.

    Returns
    -------
    StatisticsSettings
    """

    return self.config.statistics


###############################################################################


def security_settings(self) -> SecuritySettings:
    """
    Return security configuration.

    Returns
    -------
    SecuritySettings
    """

    return self.config.security

###############################################################################
# Performance Configuration
###############################################################################

def memory_limits(self) -> Dict[str, Any]:
    """
    Return memory-related limits.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "max_nodes":
            self.config.graph.max_nodes,

        "max_edges":
            self.config.graph.max_edges,

        "cache_size":
            self.config.cache.cache_size,

        "compression":
            self.config.storage.compression,

        "auto_cleanup":
            self.config.graph.auto_cleanup,

        "cleanup_interval":
            self.config.graph.cleanup_interval,

    }


###############################################################################


def cpu_limits(self) -> Dict[str, Any]:
    """
    Return CPU-related configuration.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "worker_threads":
            self.config.runtime.worker_threads,

        "parallel_traversal":
            self.config.traversal.parallel_traversal,

        "monitoring":
            self.config.runtime.monitoring_enabled,

        "diagnostics":
            self.config.runtime.diagnostics_enabled,

    }


###############################################################################


def thread_limits(self) -> Dict[str, Any]:
    """
    Return thread limits.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "worker_threads":
            self.config.runtime.worker_threads,

        "health_check_interval":
            self.config.runtime.health_check_interval,

        "shutdown_timeout":
            self.config.runtime.shutdown_timeout,

    }


###############################################################################


def queue_limits(self) -> Dict[str, Any]:
    """
    Return queue limits.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "max_queue_size":
            self.config.traversal.max_queue_size,

        "batch_size":
            self.config.traversal.batch_size,

        "max_depth":
            self.config.traversal.max_depth,

        "max_path_length":
            self.config.traversal.max_path_length,

    }


###############################################################################


def optimization_settings(self) -> Dict[str, Any]:
    """
    Return optimization settings.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "graph_mode":
            self.config.graph.graph_mode.name,

        "cache_mode":
            self.config.cache.cache_mode.name,

        "storage_mode":
            self.config.storage.storage_mode.name,

        "parallel_traversal":
            self.config.traversal.parallel_traversal,

        "compression":
            self.config.storage.compression,

        "preload_cache":
            self.config.cache.preload_cache,

        "collect_statistics":
            self.config.statistics.collect_statistics,

        "runtime_monitor":
            self.config.features.runtime_monitor,

        "diagnostics":
            self.config.runtime.diagnostics_enabled,

    }

###############################################################################
# Feature Flags
###############################################################################

def enable_wallet_dna(self) -> bool:
    """
    Wallet DNA feature flag.
    """

    return self.config.features.wallet_dna


###############################################################################


def enable_funding_graph(self) -> bool:
    """
    Funding Graph feature flag.
    """

    return self.config.features.funding_graph


###############################################################################


def enable_deployer_graph(self) -> bool:
    """
    Deployer Graph feature flag.
    """

    return self.config.features.deployer_graph


###############################################################################


def enable_statistics(self) -> bool:
    """
    Statistics Engine feature flag.
    """

    return self.config.features.statistics


###############################################################################


def enable_runtime_monitor(self) -> bool:
    """
    Runtime Monitor feature flag.
    """

    return self.config.features.runtime_monitor


###############################################################################


def enable_snapshots(self) -> bool:
    """
    Snapshot System feature flag.
    """

    return self.config.features.snapshots


###############################################################################


def enable_diagnostics(self) -> bool:
    """
    Diagnostics feature flag.
    """

    return self.config.features.diagnostics


###############################################################################
# Configuration Management
###############################################################################

def get(
    self,
    key: str,
    default: Any = None,
) -> Any:
    """
    Retrieve a configuration value using dot notation.

    Example
    -------
    graph.max_nodes
    runtime.worker_threads
    cache.cache_size
    """

    try:

        obj = self.config

        for part in key.split("."):

            if hasattr(obj, part):

                obj = getattr(obj, part)

            elif isinstance(obj, dict):

                obj = obj.get(part)

            else:

                return default

        return obj

    except Exception:

        return default


###############################################################################


def set(
    self,
    key: str,
    value: Any,
) -> bool:
    """
    Set a configuration value using dot notation.
    """

    try:

        parts = key.split(".")

        obj = self.config

        for part in parts[:-1]:

            obj = getattr(obj, part)

        setattr(
            obj,
            parts[-1],
            value,
        )

        return True

    except Exception as exc:

        self.logger.exception(
            "Failed setting configuration '%s': %s",
            key,
            exc,
        )

        return False


###############################################################################


def update(
    self,
    data: Dict[str, Any],
) -> bool:
    """
    Update configuration recursively.
    """

    try:

        def recursive_update(
            obj,
            values,
        ):

            for key, value in values.items():

                if hasattr(obj, key):

                    attr = getattr(obj, key)

                    if hasattr(attr, "__dict__") and isinstance(value, dict):

                        recursive_update(
                            attr,
                            value,
                        )

                    else:

                        setattr(
                            obj,
                            key,
                            value,
                        )

        recursive_update(
            self.config,
            data,
        )

        return True

    except Exception as exc:

        self.logger.exception(
            "Configuration update failed: %s",
            exc,
        )

        return False


###############################################################################


def delete(
    self,
    key: str,
) -> bool:
    """
    Reset a configuration value to None.
    """

    try:

        parts = key.split(".")

        obj = self.config

        for part in parts[:-1]:

            obj = getattr(obj, part)

        setattr(
            obj,
            parts[-1],
            None,
        )

        return True

    except Exception as exc:

        self.logger.exception(
            "Delete configuration failed: %s",
            exc,
        )

        return False


###############################################################################


def exists(
    self,
    key: str,
) -> bool:
    """
    Check whether a configuration key exists.
    """

    try:

        obj = self.config

        for part in key.split("."):

            if hasattr(obj, part):

                obj = getattr(obj, part)

            else:

                return False

        return True

    except Exception:

        return False


###############################################################################


def reset_defaults(self) -> None:
    """
    Restore the complete default configuration.
    """

    self.config = GraphConfiguration()

    self.logger.info(
        "Graph configuration restored to defaults."
    )

###############################################################################
# File Operations
###############################################################################

def load_json(
    self,
    file_path: Union[str, Path],
) -> Dict[str, Any]:
    """
    Load configuration from JSON.
    """

    file_path = Path(file_path)

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


###############################################################################


def save_json(
    self,
    file_path: Union[str, Path],
) -> Path:
    """
    Save configuration as JSON.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with file_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(

            asdict(self.config),

            file,

            indent=4,

            default=str,

        )

    self.logger.info(
        "Configuration saved to %s",
        file_path,
    )

    return file_path


###############################################################################


def load_yaml(
    self,
    file_path: Union[str, Path],
) -> Dict[str, Any]:
    """
    Load configuration from YAML.
    """

    file_path = Path(file_path)

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return yaml.safe_load(file)


###############################################################################


def save_yaml(
    self,
    file_path: Union[str, Path],
) -> Path:
    """
    Save configuration as YAML.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with file_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        yaml.safe_dump(

            asdict(self.config),

            file,

            sort_keys=False,

        )

    self.logger.info(
        "Configuration saved to %s",
        file_path,
    )

    return file_path


###############################################################################


def import_config(
    self,
    file_path: Union[str, Path],
) -> bool:
    """
    Import configuration from JSON or YAML.
    """

    try:

        file_path = Path(file_path)

        suffix = file_path.suffix.lower()

        if suffix == ".json":

            data = self.load_json(file_path)

        elif suffix in {".yaml", ".yml"}:

            data = self.load_yaml(file_path)

        else:

            raise ValueError(
                f"Unsupported configuration format: {suffix}"
            )

        self.update(data)

        self._validate_configuration()

        self.logger.info(
            "Configuration imported from %s",
            file_path,
        )

        return True

    except Exception as exc:

        self.logger.exception(
            "Configuration import failed: %s",
            exc,
        )

        return False


###############################################################################


def export_config(
    self,
    file_path: Union[str, Path],
    export_format: str = "json",
) -> Path:
    """
    Export configuration.

    Parameters
    ----------
    file_path
        Output file.

    export_format
        json | yaml

    Returns
    -------
    Path
    """

    export_format = export_format.lower()

    if export_format == "json":

        return self.save_json(file_path)

    if export_format in {

        "yaml",

        "yml",

    }:

        return self.save_yaml(file_path)

    raise ValueError(
        f"Unsupported export format: {export_format}"
    )

###############################################################################
# Validation
###############################################################################

def validate(self) -> bool:
    """
    Validate the complete Wallet DNA configuration.

    Returns
    -------
    bool
    """

    return (

        self.validate_graph()

        and self.validate_runtime()

        and self.validate_cache()

        and self.validate_storage()

    )


###############################################################################


def validate_graph(self) -> bool:
    """
    Validate graph configuration.
    """

    graph = self.config.graph

    try:

        if graph.max_nodes <= 0:

            return False

        if graph.max_edges <= 0:

            return False

        if graph.cleanup_interval <= 0:

            return False

        return True

    except Exception:

        return False


###############################################################################


def validate_runtime(self) -> bool:
    """
    Validate runtime configuration.
    """

    runtime = self.config.runtime

    try:

        if runtime.worker_threads <= 0:

            return False

        if runtime.snapshot_interval <= 0:

            return False

        if runtime.health_check_interval <= 0:

            return False

        if runtime.shutdown_timeout <= 0:

            return False

        return True

    except Exception:

        return False


###############################################################################


def validate_cache(self) -> bool:
    """
    Validate cache configuration.
    """

    cache = self.config.cache

    try:

        if cache.cache_size < 0:

            return False

        if cache.cache_ttl < 0:

            return False

        if cache.eviction_policy not in {

            "LRU",

            "LFU",

            "FIFO",

        }:

            return False

        return True

    except Exception:

        return False


###############################################################################


def validate_storage(self) -> bool:
    """
    Validate storage configuration.
    """

    storage = self.config.storage

    try:

        if storage.persist_interval <= 0:

            return False

        if storage.backup_interval <= 0:

            return False

        if storage.backup_directory is None:

            return False

        return True

    except Exception:

        return False


###############################################################################


def validation_report(self) -> Dict[str, Any]:
    """
    Generate validation report.

    Returns
    -------
    Dict[str, Any]
    """

    graph_valid = self.validate_graph()

    runtime_valid = self.validate_runtime()

    cache_valid = self.validate_cache()

    storage_valid = self.validate_storage()

    overall = (

        graph_valid

        and runtime_valid

        and cache_valid

        and storage_valid

    )

    return {

        "overall_valid": overall,

        "graph": graph_valid,

        "runtime": runtime_valid,

        "cache": cache_valid,

        "storage": storage_valid,

        "environment": self.environment.value,

        "configuration_version": self.config.graph.graph_version,

        "generated_at": time.time(),

    }

###############################################################################
# Environment
###############################################################################

def development(self) -> None:
    """
    Switch configuration to Development.
    """

    self.environment = Environment.DEVELOPMENT

    self.config.runtime.monitoring_enabled = True

    self.config.runtime.diagnostics_enabled = True

    self.config.runtime.auto_snapshot = True

    self.config.cache.cache_statistics = True

    self.config.features.diagnostics = True

    self.config.features.runtime_monitor = True

    self.logger.info(
        "Environment switched to DEVELOPMENT."
    )


###############################################################################


def testing(self) -> None:
    """
    Switch configuration to Testing.
    """

    self.environment = Environment.TESTING

    self.config.runtime.monitoring_enabled = False

    self.config.runtime.auto_snapshot = False

    self.config.runtime.diagnostics_enabled = True

    self.config.cache.cache_statistics = False

    self.config.features.snapshots = False

    self.logger.info(
        "Environment switched to TESTING."
    )


###############################################################################


def staging(self) -> None:
    """
    Switch configuration to Staging.
    """

    self.environment = Environment.STAGING

    self.config.runtime.monitoring_enabled = True

    self.config.runtime.auto_snapshot = True

    self.config.runtime.diagnostics_enabled = True

    self.config.cache.cache_statistics = True

    self.config.features.runtime_monitor = True

    self.logger.info(
        "Environment switched to STAGING."
    )


###############################################################################


def production(self) -> None:
    """
    Switch configuration to Production.
    """

    self.environment = Environment.PRODUCTION

    self.config.runtime.monitoring_enabled = True

    self.config.runtime.auto_snapshot = False

    self.config.runtime.diagnostics_enabled = False

    self.config.cache.cache_statistics = False

    self.config.features.diagnostics = False

    self.config.features.runtime_monitor = True

    self.logger.info(
        "Environment switched to PRODUCTION."
    )


###############################################################################


def current_environment(self) -> Dict[str, Any]:
    """
    Return current runtime environment.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "environment":
            self.environment.value,

        "monitoring":
            self.config.runtime.monitoring_enabled,

        "diagnostics":
            self.config.runtime.diagnostics_enabled,

        "auto_snapshot":
            self.config.runtime.auto_snapshot,

        "cache_statistics":
            self.config.cache.cache_statistics,

        "runtime_monitor":
            self.config.features.runtime_monitor,

        "snapshots":
            self.config.features.snapshots,

    }

###############################################################################
# Utilities
###############################################################################

def summary(self) -> Dict[str, Any]:
    """
    Return a concise configuration summary.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "graph_name":
            self.config.graph.graph_name,

        "graph_version":
            self.config.graph.graph_version,

        "environment":
            self.environment.value,

        "graph_mode":
            self.config.graph.graph_mode.name,

        "storage":
            self.config.storage.storage_mode.name,

        "cache":
            self.config.cache.cache_mode.name,

        "worker_threads":
            self.config.runtime.worker_threads,

        "max_nodes":
            self.config.graph.max_nodes,

        "max_edges":
            self.config.graph.max_edges,

        "statistics":
            self.config.features.statistics,

    }


###############################################################################


def pretty_print(self) -> str:
    """
    Pretty-print current configuration.

    Returns
    -------
    str
    """

    summary = self.summary()

    lines = []

    lines.append("=" * 80)

    lines.append("             WALLET DNA GRAPH CONFIGURATION")

    lines.append("=" * 80)

    for key, value in summary.items():

        lines.append(

            f"{key:<25}: {value}"

        )

    lines.append("=" * 80)

    return "\n".join(lines)


###############################################################################


def diagnostics(self) -> Dict[str, Any]:
    """
    Generate configuration diagnostics.

    Returns
    -------
    Dict[str, Any]
    """

    validation = self.validation_report()

    diagnostics = {

        "configuration_valid":

            validation["overall_valid"],

        "environment":

            self.environment.value,

        "graph":

            validation["graph"],

        "runtime":

            validation["runtime"],

        "cache":

            validation["cache"],

        "storage":

            validation["storage"],

        "features":

            asdict(

                self.config.features

            ),

        "runtime_settings":

            asdict(

                self.config.runtime

            ),

        "cache_settings":

            asdict(

                self.config.cache

            ),

    }

    return diagnostics


###############################################################################


def snapshot(self) -> Dict[str, Any]:
    """
    Create a configuration snapshot.

    Returns
    -------
    Dict[str, Any]
    """

    return {

        "timestamp":

            time.time(),

        "environment":

            self.environment.value,

        "configuration":

            copy.deepcopy(

                asdict(self.config)

            ),

    }                    
