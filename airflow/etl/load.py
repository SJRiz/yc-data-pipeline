from airflow.providers.postgres.hooks.postgres import PostgresHook

def load_to_postgres():
    hook = PostgresHook(postgres_conn_id='postgres_docker')
    sql = """
    COPY startups(
      name, slug, ceo_name, ceo_linkedin, company_linkedin,
      eng, remote, job_website, description, stage,
      tags, industries, all_locations, team_size, batch, funding
    )
    FROM STDIN WITH CSV HEADER NULL '\\N';
    """
    file_path = './data/processed/yc_clean.csv'

    with hook.get_conn() as conn:
        with conn.cursor() as cur, open(file_path, 'r', encoding='utf-8') as f:
            cur.copy_expert(sql, f)
        conn.commit()
