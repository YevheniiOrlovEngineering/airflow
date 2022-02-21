from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),

    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

with DAG(
    'first_dag',
    default_args=default_args,
    description='start OpenRGB',
    schedule_interval=timedelta(hours=4),
    start_date=datetime(2022, 2, 21),
    catchup=False,
    tags=['first']
) as dag:

    t1 = BashOperator(
        task_id='openRGB_profiles_list',
        bash_command='ls ~/.config/OpenRGB/*.orp',
    )

    t1.doc_md = dedent(
        """\
        #### T1 Documentation
        Printing openRGB profiles list
        """
    )

    templated_command = dedent(
        """ \
        cd ~/.config/OpenRGB/
        openrgb -p {{ params.profile }}
        """
    )

    t2 = BashOperator(
        task_id='openRGB_enabling',
        depends_on_past=False,
        bash_command=templated_command,
        params={'profile': 'red.orp'},
        retries=2
    )

    t2.doc_md = dedent(
        """\
        #### T2 Documentation
        Enabling openRGB with passed in profile
        """
    )

    dag.doc_md = """
    Dag for testing Airflow features within openRGB functionality
    """

    t1 >> t2
