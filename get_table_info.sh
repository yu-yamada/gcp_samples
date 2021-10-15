#!/bin/bash

# データセット毎にテーブル数、レコード数

# プロジェクト一覧を取得して、プロジェクト数分ループ
gcloud projects list | cut -d' ' -f1 | while read project
do
  #プロジェクトの切り替え
  gcloud config set project $project

  # プロジェクト内のデータセット一覧の取得
  bq ls | grep -E -v "datasetId|---" > dataset.lst

  while read dataset
  do
    ## echo "select project_id, dataset_id, count(distinct table_id) table_cnt, sum(row_count) record_cnt, sum(size_bytes)/1024/1024/1024 size_gb from \`${project}.${dataset}.__TABLES__\` where type =1 group by project_id, dataset_id;"
    bq  query  --use_legacy_sql=false --format csv "select project_id, dataset_id, count(distinct table_id) table_cnt, sum(row_count) record_cnt, sum(size_bytes)/1024/1024/1024 size_gb from \`${project}.${dataset}.__TABLES__\` where type =1 group by project_id, dataset_id;"
  done < dataset.lst

done
