import json
import random
import argparse
from datetime import datetime, timedelta
import os
import sys

 
USER_IDS=[f"u{str(i).zfill(5)}" for i in range(1, 1001)]  # 1000 users
COURSE_IDS=[f"c{str(i).zfill(3)}" for i in range(1, 201)] # 200 courses
EVENTS= ["login","logout","course_view","ressource_view","quiz_start","quiz_submit","forum_post","forum_read","assignment_upload"]

IP_PREFIXES = ["192.168.1.", "10.0.0.", "172.16.0."]  # 3 IP prefixes


def random_date(start_date, end_date):
    """Generate a random datetime between `start_date` and `end_date`."""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days=random.randrange(days_between)
    random_time=random.randrange(24*3600)  # seconds in a day
    return start_date + timedelta(days=random_days, seconds=random_time)

def generate_logs(timestamp):
    user=random.choice(USER_IDS)
    event=random.choice(EVENTS)
    log={
        "ts": timestamp.isoformat() +"Z",
        "user_id": user,
        "event": event,
        "ip_hash":f"hash_{random.randint(1, 9999)}",       #pseudonymized IP hash
        "session_id": f"sess_{random.randint(10000, 99999)}",   #pseudonymized session ID
    }

    if event in ["course_view", "ressource_view","quiz_start","quiz_submit"]:
        log["course_id"]=random.choice(COURSE_IDS)
    if event in ["quiz_submit"]:
        log["score"]=round(random.uniform(0, 100), 1)  # random score between 0 and 100
    if event in ["forum_post","assignment_upload"]:
        log["details"]= {"size_kb": random.randint(1, 500)}  # size of the post/upload in KB
    
    return log

def write_logs(output_file,total_lines):
    """Ecrit les logs ligne par ligne dans un fichier JSONL"""
    end_date=datetime.now()
    start_date=end_date - timedelta(days=30)  # logs from the last 30 days

    print(f"Generating {total_lines} logs in {output_file}...")

    with open(output_file, "w", encoding="utf-8") as f:
        for i in range(total_lines):
            timestamp = random_date(start_date, end_date)
            log = generate_logs(timestamp)
            f.write(json.dumps(log) + "\n")

            # Progression simple
            if (i+1) % (total_lines//10) == 0:
                progress= (i+1) / total_lines * 100
                print(f"Progression: {progress:.0f}%({i+1:,} logs)")
    
    print(f"Terminé. Fichier généré: {output_file}")
    size= os.path.getsize(output_file) / (1024 * 1024)  # taille en MB
    print(f"Taille du fichier: {size:.2f} MB")

def main():
    parser = argparse.ArgumentParser(description="Génère un fichier de logs JSONL pour les tests.")
    parser.add_argument("--output", type=str, default="logs.jsonl", help="chemin du fichier de sortie")
    parser.add_argument("--nombre", type=int, default=100000, help="Nombre de logs à générer")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)  # Crée le dossier de sortie si nécessaire

    write_logs(args.output, args.nombre)


if __name__ == "__main__":    main()