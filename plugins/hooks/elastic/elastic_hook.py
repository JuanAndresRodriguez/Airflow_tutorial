from airflow.plugins_manager import AirflowPlugin
from airflow.hooks.base import BaseHook

from elasticsearch import Elasticsearch

class ElasticHook(BaseHook):
    def __init__(self, conn_id='elastic_default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = self.get_connection(conn_id)

        conn_config = {}
        hosts = []

        if conn.host:
            hosts = conn.host.split(',')
        if conn.port:
            conn_config['port'] = int(conn.port)
        if conn.login:
            conn_config['http_auth'] = (conn.login, conn.password)

        self.es = Elasticsearch(hosts, **conn_config)
        self.index = conn.schema

    def info(self):
        """
        returns information about the elastic search instance
        """
        return self.es.info()
    
    def set_index(self, index):
        """
        define the index we want to use
        """
        self.index = index

    def add_doc(self, index, doc_type, doc):
        """
        add a document to a specific index
        """
        self.set_index(index)
        res= self.es.index(
            index=index,
            doc_type=doc_type,
            doc=doc
        )
        return res
    
# airflow plugins inside materials-airflow-scheduler-1 (to see loaded plugins)
# Elastic Hook has to be registered to the airflow plugin manager.

class AirflowElasticPlugin(AirflowPlugin):
    name = 'elastic'
    hooks = [ElasticHook]