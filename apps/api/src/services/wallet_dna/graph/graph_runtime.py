###############################################################################
# GraphRuntime
###############################################################################

class GraphRuntime:
    """
    Runtime manager for the Wallet DNA graph engine.

    Responsibilities
    ----------------
    • Runtime lifecycle
    • Timers
    • Performance monitoring
    • Counters
    • Events
    • Health monitoring
    • Snapshots
    """

    ###########################################################################
    # Initialization
    ###########################################################################

    def __init__(
        self,
        graph=None,
        cache=None,
        statistics=None,
        logger=None,
    ):
        """
        Initialize Graph Runtime.
        """

        self.graph = graph
        self.cache = cache
        self.statistics = statistics

        self.logger = logger

        self._initialize_runtime()
        self._initialize_timers()
        self._initialize_counters()
        self._initialize_configuration()

###############################################################################
# Initialization
###############################################################################

def __init__(
    self,
    graph=None,
    cache=None,
    statistics=None,
    storage=None,
    logger=None,
):
    """
    Initialize Graph Runtime.

    Parameters
    ----------
    graph : GraphEngine, optional
        Wallet DNA graph engine.

    cache : GraphCache, optional
        Graph cache manager.

    statistics : GraphStatistics, optional
        Statistics engine.

    storage : GraphStorage, optional
        Graph storage backend.

    logger : logging.Logger, optional
        Runtime logger.
    """

    ###########################################################################
    # Core Components
    ###########################################################################

    self.graph = graph

    self.cache = cache

    self.statistics = statistics

    self.storage = storage

    self.logger = logger

    ###########################################################################
    # Initialize Runtime
    ###########################################################################

    self._initialize_runtime()

    self._initialize_timers()

    self._initialize_counters()

    self._initialize_configuration()


###############################################################################


def _initialize_runtime(self) -> None:
    """
    Initialize runtime state.
    """

    self.running = False

    self.paused = False

    self.shutdown_requested = False

    self.started_at = None

    self.stopped_at = None

    self.paused_at = None

    self.resumed_at = None

    self.last_activity = None

    self.runtime_id = str(uuid.uuid4())

    self.runtime_version = "1.0.0"

    self.state = RuntimeState.STOPPED

    self.latest_snapshot = None


###############################################################################


def _initialize_timers(self) -> None:
    """
    Initialize runtime timers.
    """

    self.timers = {}

    self.active_timers = {}

    self.total_runtime = 0.0

    self.total_pause_time = 0.0

    self.graph_build_time = 0.0

    self.total_traversal_time = 0.0

    self.total_cache_time = 0.0

    self.last_timer_reset = time.time()


###############################################################################


def _initialize_counters(self) -> None:
    """
    Initialize runtime counters.
    """

    self.nodes_processed = 0

    self.edges_processed = 0

    self.traversals = 0

    self.cache_hits = 0

    self.cache_misses = 0

    self.errors = 0

    self.warnings = 0

    self.events_processed = 0

    self.snapshots_created = 0

    self.restores = 0


###############################################################################


def _initialize_configuration(self) -> None:
    """
    Initialize runtime configuration.
    """

    self.auto_snapshot = True

    self.snapshot_interval = 300

    self.enable_monitoring = True

    self.enable_events = True

    self.enable_diagnostics = True

    self.max_event_history = 1000

    self.max_timers = 100

    self.max_runtime_hours = 24

    self.health_check_interval = 30

    self.configuration = {

        "auto_snapshot": self.auto_snapshot,

        "snapshot_interval": self.snapshot_interval,

        "enable_monitoring": self.enable_monitoring,

        "enable_events": self.enable_events,

        "enable_diagnostics": self.enable_diagnostics,

        "health_check_interval": self.health_check_interval,

    }

###############################################################################
# Runtime Control
###############################################################################

def start(self) -> bool:
    """
    Start the Graph Runtime.

    Returns
    -------
    bool
        True if runtime started successfully.
    """

    try:

        if self.running:

            self.logger.warning(
                "Graph Runtime is already running."
            )

            return False

        self.running = True
        self.paused = False
        self.shutdown_requested = False

        self.started_at = time.time()
        self.last_activity = self.started_at

        self.state = RuntimeState.RUNNING

        self.logger.info(
            "Graph Runtime started."
        )

        return True

    except Exception as exc:

        self.errors += 1

        self.logger.exception(
            "Failed to start runtime: %s",
            exc,
        )

        return False


###############################################################################


def stop(self) -> bool:
    """
    Stop the Graph Runtime.

    Returns
    -------
    bool
    """

    try:

        if not self.running:

            return False

        self.running = False

        self.paused = False

        self.stopped_at = time.time()

        if self.started_at is not None:

            self.total_runtime += (
                self.stopped_at - self.started_at
            )

        self.state = RuntimeState.STOPPED

        self.logger.info(
            "Graph Runtime stopped."
        )

        return True

    except Exception as exc:

        self.errors += 1

        self.logger.exception(
            "Failed to stop runtime: %s",
            exc,
        )

        return False


###############################################################################


def pause(self) -> bool:
    """
    Pause the runtime.

    Returns
    -------
    bool
    """

    try:

        if not self.running:

            return False

        if self.paused:

            return False

        self.paused = True

        self.paused_at = time.time()

        self.state = RuntimeState.PAUSED

        self.logger.info(
            "Graph Runtime paused."
        )

        return True

    except Exception as exc:

        self.errors += 1

        self.logger.exception(
            "Pause failed: %s",
            exc,
        )

        return False


###############################################################################


def resume(self) -> bool:
    """
    Resume runtime execution.

    Returns
    -------
    bool
    """

    try:

        if not self.paused:

            return False

        self.paused = False

        self.resumed_at = time.time()

        if self.paused_at is not None:

            self.total_pause_time += (
                self.resumed_at - self.paused_at
            )

        self.last_activity = self.resumed_at

        self.state = RuntimeState.RUNNING

        self.logger.info(
            "Graph Runtime resumed."
        )

        return True

    except Exception as exc:

        self.errors += 1

        self.logger.exception(
            "Resume failed: %s",
            exc,
        )

        return False


###############################################################################


def restart(self) -> bool:
    """
    Restart the runtime.

    Returns
    -------
    bool
    """

    try:

        self.logger.info(
            "Restarting Graph Runtime..."
        )

        self.stop()

        self.reset()

        return self.start()

    except Exception as exc:

        self.errors += 1

        self.logger.exception(
            "Restart failed: %s",
            exc,
        )

        return False


###############################################################################


def shutdown(self) -> bool:
    """
    Shutdown Graph Runtime.

    Performs graceful shutdown of all runtime
    services.

    Returns
    -------
    bool
    """

    try:

        self.shutdown_requested = True

        self.stop()

        if self.cache:

            self.cache.cleanup_expired()

        self.state = RuntimeState.SHUTDOWN

        self.logger.info(
            "Graph Runtime shutdown complete."
        )

        return True

    except Exception as exc:

        self.errors += 1

        self.logger.exception(
            "Shutdown failed: %s",
            exc,
        )

        return False

###############################################################################
# Runtime Counters
###############################################################################

def increment_nodes_processed(
    self,
    count: int = 1,
) -> int:
    """
    Increment processed node counter.

    Parameters
    ----------
    count : int
        Number of nodes processed.

    Returns
    -------
    int
        Updated counter.
    """

    self.nodes_processed += count

    self.last_activity = time.time()

    return self.nodes_processed


###############################################################################


def increment_edges_processed(
    self,
    count: int = 1,
) -> int:
    """
    Increment processed edge counter.
    """

    self.edges_processed += count

    self.last_activity = time.time()

    return self.edges_processed


###############################################################################


def increment_traversals(
    self,
    count: int = 1,
) -> int:
    """
    Increment traversal counter.
    """

    self.traversals += count

    self.last_activity = time.time()

    return self.traversals


###############################################################################


def increment_cache_hits(
    self,
    count: int = 1,
) -> int:
    """
    Increment cache hit counter.
    """

    self.cache_hits += count

    self.last_activity = time.time()

    return self.cache_hits


###############################################################################


def increment_cache_misses(
    self,
    count: int = 1,
) -> int:
    """
    Increment cache miss counter.
    """

    self.cache_misses += count

    self.last_activity = time.time()

    return self.cache_misses


###############################################################################


def increment_errors(
    self,
    count: int = 1,
) -> int:
    """
    Increment runtime error counter.
    """

    self.errors += count

    self.last_activity = time.time()

    return self.errors


###############################################################################


def counter_statistics(self) -> Dict[str, Any]:
    """
    Return all runtime counters.

    Returns
    -------
    Dict[str, Any]
    """

    total_cache = self.cache_hits + self.cache_misses

    hit_rate = (
        self.cache_hits / total_cache
        if total_cache > 0
        else 0.0
    )

    return {

        "nodes_processed": self.nodes_processed,

        "edges_processed": self.edges_processed,

        "traversals": self.traversals,

        "cache_hits": self.cache_hits,

        "cache_misses": self.cache_misses,

        "cache_hit_rate": round(hit_rate, 4),

        "errors": self.errors,

        "warnings": self.warnings,

        "events_processed": self.events_processed,

        "snapshots_created": self.snapshots_created,

        "restores": self.restores,

        "runtime_seconds": self.total_runtime,

        "last_activity": self.last_activity,

    }

###############################################################################
# Performance Monitor
###############################################################################

import os
import time
import threading
import psutil


def cpu_usage(self) -> float:
    """
    Return current CPU usage (%).

    Returns
    -------
    float
    """

    try:

        usage = psutil.cpu_percent(interval=0.2)

        self.performance_statistics.cpu_usage = usage

        self.last_activity = time.time()

        return usage

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "CPU usage collection failed: %s",
            exc,
        )

        return 0.0


###############################################################################


def memory_usage(self) -> Dict[str, float]:
    """
    Return current process memory usage.

    Returns
    -------
    Dict[str, float]
    """

    try:

        process = psutil.Process(os.getpid())

        memory = process.memory_info()

        result = {

            "rss_mb": round(
                memory.rss / (1024 ** 2),
                2,
            ),

            "vms_mb": round(
                memory.vms / (1024 ** 2),
                2,
            ),

            "percent": round(
                process.memory_percent(),
                2,
            ),

        }

        self.performance_statistics.process_memory = result

        self.last_activity = time.time()

        return result

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Memory usage collection failed: %s",
            exc,
        )

        return {}


###############################################################################


def active_threads(self) -> int:
    """
    Return active thread count.

    Returns
    -------
    int
    """

    try:

        threads = threading.active_count()

        self.performance_statistics.active_threads = threads

        return threads

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Thread count failed: %s",
            exc,
        )

        return 0


###############################################################################


def uptime(self) -> float:
    """
    Return runtime uptime in seconds.

    Returns
    -------
    float
    """

    try:

        if self.started_at is None:

            return 0.0

        if self.running:

            value = time.time() - self.started_at

        else:

            value = self.total_runtime

        self.performance_statistics.uptime = value

        return round(value, 4)

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Uptime calculation failed: %s",
            exc,
        )

        return 0.0


###############################################################################


def throughput(self) -> Dict[str, float]:
    """
    Runtime throughput.

    Returns
    -------
    Dict[str, float]
    """

    try:

        runtime = self.uptime()

        if runtime <= 0:

            runtime = 1e-9

        metrics = {

            "nodes_per_second":
                self.nodes_processed / runtime,

            "edges_per_second":
                self.edges_processed / runtime,

            "traversals_per_second":
                self.traversals / runtime,

            "events_per_second":
                self.events_processed / runtime,

        }

        self.performance_statistics.runtime_throughput = metrics

        return metrics

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Throughput calculation failed: %s",
            exc,
        )

        return {}


###############################################################################


def health_status(self) -> Dict[str, Any]:
    """
    Runtime health monitor.

    Returns
    -------
    Dict[str, Any]
    """

    try:

        cpu = self.cpu_usage()

        memory = self.memory_usage()

        threads = self.active_threads()

        uptime = self.uptime()

        healthy = True

        issues = []

        #######################################################################
        # CPU
        #######################################################################

        if cpu > 90:

            healthy = False

            issues.append(
                "High CPU usage"
            )

        #######################################################################
        # Memory
        #######################################################################

        if memory.get("percent", 0) > 80:

            healthy = False

            issues.append(
                "High memory usage"
            )

        #######################################################################
        # Errors
        #######################################################################

        if self.errors > 100:

            healthy = False

            issues.append(
                "Excessive runtime errors"
            )

        #######################################################################
        # Result
        #######################################################################

        status = {

            "healthy": healthy,

            "state": self.state.name,

            "cpu_usage": cpu,

            "memory": memory,

            "threads": threads,

            "uptime": uptime,

            "errors": self.errors,

            "issues": issues,

        }

        self.performance_statistics.health = status

        return status

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Health check failed: %s",
            exc,
        )

        return {

            "healthy": False,

            "issues": [

                "Health monitor failure"

            ],



        }          

###############################################################################
# Events
###############################################################################

from collections import deque


def register_event(
    self,
    event_type: str,
    message: str,
    level: str = "INFO",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Register a runtime event.

    Parameters
    ----------
    event_type : str
        Event category.

    message : str
        Event message.

    level : str
        INFO | WARNING | ERROR | DEBUG

    metadata : dict
        Additional event data.

    Returns
    -------
    Dict[str, Any]
    """

    try:

        if not hasattr(self, "events"):

            self.events = deque(
                maxlen=self.max_event_history
            )

        event = {

            "id": str(uuid.uuid4()),

            "timestamp": time.time(),

            "datetime": datetime.utcnow().isoformat(),

            "type": event_type,

            "level": level,

            "message": message,

            "metadata": metadata or {},

        }

        self.events.append(event)

        self.events_processed += 1

        self.last_activity = time.time()

        if self.logger:

            getattr(
                self.logger,
                level.lower(),
                self.logger.info,
            )(message)

        return event

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Event registration failed: %s",
            exc,
        )

        return {}


###############################################################################


def event_history(
    self,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Return runtime event history.

    Parameters
    ----------
    limit : int

    Returns
    -------
    List[Dict]
    """

    try:

        if not hasattr(self, "events"):

            return []

        events = list(self.events)

        if limit:

            events = events[-limit:]

        return events

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Failed retrieving event history: %s",
            exc,
        )

        return []


###############################################################################


def clear_events(self) -> None:
    """
    Clear runtime event history.
    """

    try:

        if hasattr(self, "events"):

            self.events.clear()

        self.logger.info(
            "Runtime event history cleared."
        )

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Failed clearing events: %s",
            exc,
        )


###############################################################################


def latest_event(self) -> Optional[Dict[str, Any]]:
    """
    Return latest runtime event.

    Returns
    -------
    Dict | None
    """

    try:

        if not hasattr(self, "events"):

            return None

        if len(self.events) == 0:

            return None

        return self.events[-1]

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Failed retrieving latest event: %s",
            exc,
        )

        return None

###############################################################################
# Runtime Reports
###############################################################################

def runtime_summary(self) -> Dict[str, Any]:
    """
    Return a concise runtime summary.

    Returns
    -------
    Dict[str, Any]
    """

    try:

        return {

            "runtime_id": self.runtime_id,

            "state": self.state.name,

            "running": self.running,

            "paused": self.paused,

            "uptime_seconds": self.uptime(),

            "nodes_processed": self.nodes_processed,

            "edges_processed": self.edges_processed,

            "traversals": self.traversals,

            "cache_hits": self.cache_hits,

            "cache_misses": self.cache_misses,

            "errors": self.errors,

            "warnings": self.warnings,

            "events_processed": self.events_processed,

            "last_activity": self.last_activity,

        }

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Runtime summary failed: %s",
            exc,
        )

        return {}


###############################################################################


def performance_report(self) -> Dict[str, Any]:
    """
    Generate runtime performance report.

    Returns
    -------
    Dict[str, Any]
    """

    try:

        return {

            "cpu": self.cpu_usage(),

            "memory": self.memory_usage(),

            "threads": self.active_threads(),

            "uptime": self.uptime(),

            "throughput": self.throughput(),

            "cache_hit_rate": (

                self.cache_hits /

                max(

                    self.cache_hits +

                    self.cache_misses,

                    1,

                )

            ),

            "build_time": self.graph_build_time,

            "runtime": self.total_runtime,

        }

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Performance report failed: %s",
            exc,
        )

        return {}


###############################################################################


def health_report(self) -> Dict[str, Any]:
    """
    Generate runtime health report.

    Returns
    -------
    Dict[str, Any]
    """

    try:

        health = self.health_status()

        return {

            "runtime_id": self.runtime_id,

            "healthy": health["healthy"],

            "state": health["state"],

            "cpu_usage": health["cpu_usage"],

            "memory": health["memory"],

            "threads": health["threads"],

            "uptime": health["uptime"],

            "errors": self.errors,

            "warnings": self.warnings,

            "issues": health["issues"],

        }

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Health report failed: %s",
            exc,
        )

        return {}


###############################################################################


def export_runtime(
    self,
    file_path: Optional[str] = None,
    export_format: str = "json",
) -> Union[str, Dict[str, Any]]:
    """
    Export runtime information.

    Parameters
    ----------
    file_path
        Output file.

    export_format
        json | yaml | csv

    Returns
    -------
    str | Dict
    """

    try:

        runtime = {

            "summary":
                self.runtime_summary(),

            "performance":
                self.performance_report(),

            "health":
                self.health_report(),

            "events":
                self.event_history(),

        }

        #######################################################################

        if file_path is None:

            return runtime

        #######################################################################
        # JSON
        #######################################################################

        if export_format.lower() == "json":

            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(

                    runtime,

                    file,

                    indent=4,

                    default=str,

                )

        #######################################################################
        # YAML
        #######################################################################

        elif export_format.lower() == "yaml":

            import yaml

            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as file:

                yaml.safe_dump(

                    runtime,

                    file,

                    sort_keys=False,

                )

        #######################################################################
        # CSV
        #######################################################################

        elif export_format.lower() == "csv":

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8",
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    ["Metric", "Value"]
                )

                for key, value in self.runtime_summary().items():

                    writer.writerow(
                        [key, value]
                    )

        #######################################################################

        else:

            raise ValueError(

                f"Unsupported format: {export_format}"

            )

        #######################################################################

        self.logger.info(

            "Runtime exported to %s",

            file_path,

        )

        return file_path

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(

            "Runtime export failed: %s",

            exc,

        )

        raise

###############################################################################
# Snapshot
###############################################################################

def snapshot(self) -> Dict[str, Any]:
    """
    Create a runtime snapshot.

    Returns
    -------
    Dict[str, Any]
        Runtime snapshot.
    """

    try:

        snapshot = {

            "timestamp": time.time(),

            "runtime_id": self.runtime_id,

            "state": self.state.name,

            "running": self.running,

            "paused": self.paused,

            "started_at": self.started_at,

            "stopped_at": self.stopped_at,

            "last_activity": self.last_activity,

            ###################################################################
            # Counters
            ###################################################################

            "counters": {

                "nodes_processed": self.nodes_processed,

                "edges_processed": self.edges_processed,

                "traversals": self.traversals,

                "cache_hits": self.cache_hits,

                "cache_misses": self.cache_misses,

                "errors": self.errors,

                "warnings": self.warnings,

                "events_processed": self.events_processed,

                "snapshots_created": self.snapshots_created,

                "restores": self.restores,

            },

            ###################################################################
            # Timers
            ###################################################################

            "timers": {

                "total_runtime": self.total_runtime,

                "total_pause_time": self.total_pause_time,

                "graph_build_time": self.graph_build_time,

                "total_traversal_time": self.total_traversal_time,

                "total_cache_time": self.total_cache_time,

            },

            ###################################################################
            # Configuration
            ###################################################################

            "configuration": copy.deepcopy(
                self.configuration
            ),

        }

        self.latest_snapshot = copy.deepcopy(snapshot)

        self.snapshots_created += 1

        self.last_activity = time.time()

        self.logger.info(
            "Runtime snapshot created."
        )

        return snapshot

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Snapshot creation failed: %s",
            exc,
        )

        return {}


###############################################################################


def restore(
    self,
    snapshot: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Restore runtime from snapshot.

    Parameters
    ----------
    snapshot : dict

    Returns
    -------
    bool
    """

    try:

        if snapshot is None:

            snapshot = self.latest_snapshot

        if snapshot is None:

            self.logger.warning(
                "No runtime snapshot available."
            )

            return False

        #######################################################################
        # Runtime
        #######################################################################

        self.runtime_id = snapshot["runtime_id"]

        self.running = snapshot["running"]

        self.paused = snapshot["paused"]

        self.started_at = snapshot["started_at"]

        self.stopped_at = snapshot["stopped_at"]

        self.last_activity = snapshot["last_activity"]

        self.state = RuntimeState[
            snapshot["state"]
        ]

        #######################################################################
        # Counters
        #######################################################################

        counters = snapshot["counters"]

        self.nodes_processed = counters["nodes_processed"]

        self.edges_processed = counters["edges_processed"]

        self.traversals = counters["traversals"]

        self.cache_hits = counters["cache_hits"]

        self.cache_misses = counters["cache_misses"]

        self.errors = counters["errors"]

        self.warnings = counters["warnings"]

        self.events_processed = counters["events_processed"]

        self.snapshots_created = counters["snapshots_created"]

        self.restores = counters["restores"] + 1

        #######################################################################
        # Timers
        #######################################################################

        timers = snapshot["timers"]

        self.total_runtime = timers["total_runtime"]

        self.total_pause_time = timers["total_pause_time"]

        self.graph_build_time = timers["graph_build_time"]

        self.total_traversal_time = timers["total_traversal_time"]

        self.total_cache_time = timers["total_cache_time"]

        #######################################################################
        # Configuration
        #######################################################################

        self.configuration = copy.deepcopy(
            snapshot["configuration"]
        )

        self.logger.info(
            "Runtime restored successfully."
        )

        return True

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Runtime restore failed: %s",
            exc,
        )

        return False


###############################################################################


def reset(self) -> bool:
    """
    Reset runtime state.

    Returns
    -------
    bool
    """

    try:

        #######################################################################
        # Runtime
        #######################################################################

        self._initialize_runtime()

        self._initialize_timers()

        self._initialize_counters()

        #######################################################################
        # Events
        #######################################################################

        if hasattr(self, "events"):

            self.events.clear()

        #######################################################################
        # Snapshot
        #######################################################################

        self.latest_snapshot = None

        #######################################################################

        self.logger.info(
            "Runtime reset completed."
        )

        return True

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Runtime reset failed: %s",
            exc,
        )

        return False

###############################################################################
# Utilities
###############################################################################

def pretty_print(self) -> str:
    """
    Return a human-readable runtime report.

    Returns
    -------
    str
    """

    try:

        summary = self.runtime_summary()

        performance = self.performance_report()

        health = self.health_report()

        report = []

        separator = "=" * 80

        report.append(separator)
        report.append("               SENTINEL AI — GRAPH RUNTIME STATUS")
        report.append(separator)

        report.append(
            f"Runtime ID       : {summary['runtime_id']}"
        )

        report.append(
            f"State            : {summary['state']}"
        )

        report.append(
            f"Running          : {summary['running']}"
        )

        report.append(
            f"Paused           : {summary['paused']}"
        )

        report.append(
            f"Uptime           : {summary['uptime_seconds']:.2f}s"
        )

        report.append(separator)

        report.append("GRAPH")

        report.append(
            f"Nodes Processed  : {summary['nodes_processed']}"
        )

        report.append(
            f"Edges Processed  : {summary['edges_processed']}"
        )

        report.append(
            f"Traversals       : {summary['traversals']}"
        )

        report.append(separator)

        report.append("CACHE")

        report.append(
            f"Hits             : {summary['cache_hits']}"
        )

        report.append(
            f"Misses           : {summary['cache_misses']}"
        )

        report.append(
            f"Hit Rate         : {performance['cache_hit_rate']:.2%}"
        )

        report.append(separator)

        report.append("SYSTEM")

        report.append(
            f"CPU Usage        : {performance['cpu']:.2f}%"
        )

        report.append(
            f"Threads          : {performance['threads']}"
        )

        report.append(
            f"Memory           : {performance['memory']}"
        )

        report.append(separator)

        report.append("HEALTH")

        report.append(
            f"Healthy          : {health['healthy']}"
        )

        report.append(
            f"Issues           : {health['issues']}"
        )

        report.append(separator)

        return "\n".join(report)

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Pretty print failed: %s",
            exc,
        )

        return "Runtime unavailable."


###############################################################################


def validate_runtime(self) -> bool:
    """
    Validate runtime consistency.

    Returns
    -------
    bool
    """

    try:

        checks = [

            self.runtime_id is not None,

            self.configuration is not None,

            self.timers is not None,

            self.running in [True, False],

            self.paused in [True, False],

            self.nodes_processed >= 0,

            self.edges_processed >= 0,

            self.cache_hits >= 0,

            self.cache_misses >= 0,

            self.errors >= 0,

        ]

        valid = all(checks)

        if not valid:

            self.logger.warning(
                "Runtime validation failed."
            )

        return valid

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Runtime validation failed: %s",
            exc,
        )

        return False


###############################################################################


def diagnostics(self) -> Dict[str, Any]:
    """
    Generate runtime diagnostics.

    Returns
    -------
    Dict[str, Any]
    """

    try:

        diagnostics = {

            "runtime_valid":
                self.validate_runtime(),

            "health":
                self.health_report(),

            "performance":
                self.performance_report(),

            "summary":
                self.runtime_summary(),

            "counter_statistics":
                self.counter_statistics(),

            "latest_event":
                self.latest_event(),

            "active_timers":
                len(self.active_timers),

            "events":
                len(
                    self.event_history()
                ),

            "snapshot_exists":
                self.latest_snapshot is not None,

            "configuration":
                self.configuration,

        }

        return diagnostics

    except Exception as exc:

        self.increment_errors()

        self.logger.exception(
            "Diagnostics failed: %s",
            exc,
        )

        return {

            "runtime_valid": False,

            "error": str(exc),

        }        