#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time

def update_all_jobs(progress_callback=None, log_callback=None):
    
    STREAM_JAR = "/home/hadoopthanhtruc/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar"
    base_hdfs = "/user/hadoopthanhtruc"
    base_local = "/home/hadoopthanhtruc/mapreduce"

    # Đồng bộ dữ liệu Hasaki từ PostgreSQL
    if log_callback:
        log_callback("🔹 Đang đồng bộ dữ liệu Hasaki từ PostgreSQL sang HDFS...")
    result = subprocess.run([
        "sqoop", "import", "--connect", "jdbc:postgresql://localhost:5432/bigdata",
        "--username", "sqoopdb", "--password", "13062005", "--table", "hasaki",
        "--target-dir", f"{base_hdfs}/hasaki_input_pg", "--delete-target-dir", "-m", "1"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        if log_callback:
            log_callback("✅ Hoàn tất đồng bộ dữ liệu Hasaki.")
    else:
        if log_callback:
            log_callback(f"Lỗi đồng bộ dữ liệu Hasaki: {result.stderr}")
        print(f"Lỗi đồng bộ dữ liệu Hasaki: {result.stderr}")
        return

    # Danh sách các job (chỉ Hasaki)
    jobs = [
        ("Hasaki - Job 1", f"{base_local}/job1_hasaki/top_reviews_mapper.py", f"{base_local}/job1_hasaki/top_reviews_reducer.py",
         f"{base_hdfs}/hasaki_input_pg", f"{base_hdfs}/hasaki_output_job1"),
        ("Hasaki - Job 2", f"{base_local}/job2_hasaki/avg_rating_brand_mapper.py", f"{base_local}/job2_hasaki/avg_rating_brand_reducer.py",
         f"{base_hdfs}/hasaki_input_pg", f"{base_hdfs}/hasaki_output_job2"),
        ("Hasaki - Job 3", f"{base_local}/job3_hasaki/price_range_mapper.py", f"{base_local}/job3_hasaki/price_range_reducer.py",
         f"{base_hdfs}/hasaki_input_pg", f"{base_hdfs}/hasaki_output_job3"),
    ]

    log_output = ""
    total = len(jobs)

    for i, (job_name, mapper, reducer, hdfs_in, hdfs_out) in enumerate(jobs, start=1):
        step = f"[{i}/{total}] {job_name}"
        print(f"\nĐang chạy {step}")
        if log_callback:
            log_callback(f"🔹 Đang chạy {step}")

        subprocess.run(["hdfs", "dfs", "-rm", "-r", "-f", hdfs_out], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        cmd = [
            "hadoop", "jar", STREAM_JAR,
            "-files", f"{mapper},{reducer}",
            "-mapper", f"python3 {mapper}",
            "-reducer", f"python3 {reducer}",
            "-input", hdfs_in,
            "-output", hdfs_out
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log_output += f"\n\n=== {job_name} ===\n" + result.stdout[-800:] + "\n" + result.stderr

        if result.returncode != 0:
            if log_callback:
                log_callback(f"Lỗi khi chạy {job_name}: {result.stderr}")
            print(f"Lỗi khi chạy {job_name}: {result.stderr}")
        else:
            if log_callback:
                log_callback(f"Hoàn tất {job_name}")

        if progress_callback:
            progress_callback(i / total)

        time.sleep(1)

    print("\nHoàn tất 3 Job Hasaki!")
    if log_callback:
        log_callback("Hoàn tất 3 Job Hasaki!")

    return log_output

if __name__ == "__main__":
    update_all_jobs()