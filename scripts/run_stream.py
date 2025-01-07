import subprocess
import time
import os

def run_producer():
    print("Initializing Kafka producer...")
    current_dir = os.path.abspath(os.path.dirname(__file__))  
    scripts_dir = os.path.join(current_dir)  
    producer_script_path = os.path.join(scripts_dir, "producer_script.py")

    producer_process = subprocess.Popen(
        ["python", producer_script_path],
        cwd=scripts_dir, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return producer_process

def run_consumer():
    print("Initializing Kafka consumer...")
    current_dir = os.path.abspath(os.path.dirname(__file__))  
    scripts_dir = os.path.join(current_dir)  
    consumer_script_path = os.path.join(scripts_dir, "consumer_script.py")

    consumer_process = subprocess.Popen(
        ["python", consumer_script_path],
        cwd=scripts_dir, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return consumer_process

def run_stream_processor():
    print("Initializing Kafka stream processor...")
    current_dir = os.path.abspath(os.path.dirname(__file__))
    scripts_dir = os.path.join(current_dir)  
    stream_processor_script_path = os.path.join(scripts_dir, "start_reddit_kafka_stream_processor.py")

    stream_processor_process = subprocess.Popen(
        ["python", stream_processor_script_path],
        cwd=scripts_dir, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return stream_processor_process

def main():
    producer_process = run_producer()
    consumer_process = run_consumer()
    stream_process = run_stream_processor()

    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        producer_process.terminate()
        consumer_process.terminate()
        stream_process.terminate()
    finally:
        producer_process.wait()
        consumer_process.wait()
        stream_process.wait()

if __name__ == "__main__":
    """
    TODO: I'm not sure whether this is working correctly.
    I would strongly recommend running all of these 
    scripts separately.
    """
    main()