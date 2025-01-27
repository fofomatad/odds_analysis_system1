import logging
import psutil
import time
from datetime import datetime
import threading
from queue import Queue
import pandas as pd
import os
from config import DATA_DIR, LOG_LEVEL

logger = logging.getLogger(__name__)

class SystemMonitor:
    def __init__(self):
        self.stats_file = os.path.join(DATA_DIR, 'system_stats.csv')
        self.is_running = False
        self.monitor_thread = None
        self.stats_queue = Queue()
        self.alert_thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 80.0,
            'disk_percent': 80.0
        }
        
    def start(self):
        """Inicia o monitoramento do sistema"""
        if not self.is_running:
            self.is_running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            logger.info("Sistema de monitoramento iniciado")
    
    def stop(self):
        """Para o monitoramento do sistema"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join()
            logger.info("Sistema de monitoramento parado")
    
    def _monitor_loop(self):
        """Loop principal de monitoramento"""
        while self.is_running:
            try:
                stats = self._collect_stats()
                self._save_stats(stats)
                self._check_thresholds(stats)
                time.sleep(60)  # Coleta estatísticas a cada minuto
            except Exception as e:
                logger.error(f"Erro no loop de monitoramento: {e}")
                time.sleep(5)
    
    def _collect_stats(self):
        """Coleta estatísticas do sistema"""
        try:
            stats = {
                'timestamp': datetime.now(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'network_bytes_sent': psutil.net_io_counters().bytes_sent,
                'network_bytes_recv': psutil.net_io_counters().bytes_recv,
                'thread_count': threading.active_count()
            }
            return stats
        except Exception as e:
            logger.error(f"Erro ao coletar estatísticas: {e}")
            return None
    
    def _save_stats(self, stats):
        """Salva estatísticas em arquivo CSV"""
        if not stats:
            return
            
        try:
            df = pd.DataFrame([stats])
            mode = 'a' if os.path.exists(self.stats_file) else 'w'
            header = not os.path.exists(self.stats_file)
            df.to_csv(self.stats_file, mode=mode, header=header, index=False)
        except Exception as e:
            logger.error(f"Erro ao salvar estatísticas: {e}")
    
    def _check_thresholds(self, stats):
        """Verifica se algum threshold foi ultrapassado"""
        if not stats:
            return
            
        try:
            for metric, threshold in self.alert_thresholds.items():
                if metric in stats and stats[metric] > threshold:
                    logger.warning(
                        f"Alerta: {metric} está em {stats[metric]}% "
                        f"(threshold: {threshold}%)"
                    )
        except Exception as e:
            logger.error(f"Erro ao verificar thresholds: {e}")
    
    def get_system_health(self):
        """Retorna status atual do sistema"""
        try:
            stats = self._collect_stats()
            if not stats:
                return {'status': 'error', 'message': 'Não foi possível coletar estatísticas'}
            
            health_status = 'healthy'
            if any(stats.get(metric, 0) > threshold 
                  for metric, threshold in self.alert_thresholds.items()):
                health_status = 'warning'
            
            return {
                'status': health_status,
                'stats': stats,
                'thresholds': self.alert_thresholds
            }
        except Exception as e:
            logger.error(f"Erro ao obter status do sistema: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_historical_stats(self, hours=24):
        """Retorna estatísticas históricas do sistema"""
        try:
            if not os.path.exists(self.stats_file):
                return pd.DataFrame()
            
            df = pd.read_csv(self.stats_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filtra últimas X horas
            cutoff_time = datetime.now() - pd.Timedelta(hours=hours)
            df = df[df['timestamp'] > cutoff_time]
            
            return df
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas históricas: {e}")
            return pd.DataFrame() 