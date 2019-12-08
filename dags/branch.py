# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Example DAG demonstrating the usage of the BashOperator."""

from datetime import timedelta

import airflow
from airflow.models import DAG
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id='branch',
    default_args=args,
    start_date=airflow.utils.dates.days_ago(2),
    #schedule_interval='0 0 * * *',
    #dagrun_timeout=timedelta(minutes=60),
)

def _get_weekday(execution_date, **context):
    return execution_date.strftime("%a")

branching = BranchPythonOperator(
    task_id="branching",
    python_callable=_get_weekday,
    provide_context=True,
    dag=dag)

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

join = DummyOperator(
    task_id="join",
    trigger_rule="none_failed"
)

for day in days:
    branching >> DummyOperator(task_id=day, dag=dag) >> join