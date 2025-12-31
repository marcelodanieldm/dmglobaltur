import time
import threading
from typing import Callable, Optional


from data_ingestion.china_sources import XHS_Scraper, Ctrip_API, Baidu_Mirror
from data_ingestion.notifiers import send_slack_alert, log_system_health

class DataIngestor:
    def __init__(self, user_id: str, slack_notify: Callable, log_health: Callable):
        self.source_objs = [XHS_Scraper(), Ctrip_API(), Baidu_Mirror()]
        self.sources = ["XHS_Scraper", "Ctrip_API", "Baidu_Mirror"]
        self.current_idx = 0
        self.failures = 0
        self.last_failure_times = []
        self.lock = threading.Lock()
        self.user_id = user_id
        self.slack_notify = slack_notify
        self.log_health = log_health
        self.last_rotation_time = None
        self.recovery_thread = None

    def ingest(self, *args, **kwargs):
        source_obj = self.source_objs[self.current_idx]
        try:
            result = source_obj.fetch(*args, **kwargs)
            self._reset_failures()
            return result
        except Exception as e:
            self._register_failure(str(e))
            raise

    def _register_failure(self, error_msg: str):
        now = time.time()
        self.last_failure_times.append(now)
        self.failures += 1
        # Remove failures older than 1 minute
        self.last_failure_times = [t for t in self.last_failure_times if now - t < 60]
        self.failures = len(self.last_failure_times)
        if self.failures > 3:
            self._circuit_break(error_msg)

    def _circuit_break(self, error_msg: str):
        with self.lock:
            if self.current_idx == 0:
                # Log to system_health_logs
                self.log_health(
                    user_id=self.user_id,
                    source=self.sources[self.current_idx],
                    event="circuit_break",
                    message=error_msg
                )
                # Switch to next source
                self.current_idx = 1
                self.last_rotation_time = time.time()
                # Notify Daniel (QA) via Slack
                self.slack_notify(
                    channel="#qa-alerts",
                    message=f"[HIGH PRIORITY] Data source XHS_Scraper failed >3 times in 1 min. Switched to Ctrip_API."
                )
                # Start recovery timer
                self._start_recovery_timer()

    def _start_recovery_timer(self):
        if self.recovery_thread and self.recovery_thread.is_alive():
            return
        self.recovery_thread = threading.Thread(target=self._recovery_loop, daemon=True)
        self.recovery_thread.start()

    def _recovery_loop(self):
        while True:
            time.sleep(4 * 60 * 60)  # 4 hours
            with self.lock:
                if self.current_idx != 0:
                    self.current_idx = 0
                    self.failures = 0
                    self.last_failure_times = []
                    self.slack_notify(
                        channel="#qa-alerts",
                        message="[INFO] Attempting to restore XHS_Scraper as primary data source."
                    )
                    break

    def _reset_failures(self):
        self.failures = 0
        self.last_failure_times = []



# Example usage:


if __name__ == "__main__":
    ingestor = DataIngestor(user_id="daniel", slack_notify=send_slack_alert, log_health=log_system_health)
    for i in range(20):
        try:
            data = ingestor.ingest()
            print(f"[{i}] Fuente: {data['source']} | Data: {data['data']}")
        except Exception as e:
            print(f"[{i}] Error: {e}")
        time.sleep(5)
