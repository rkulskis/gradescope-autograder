import subprocess
import time
import os
import concurrent.futures
import json
import sys

LINK = "https://autograder-service-ece440spring2024-619f12.apps.shift.nerc.mghpcc.org/"

# request with correct solution
def make_request1(uname_pwd):
    for http_retries in range(5):
        try:
            response = subprocess.run(["curl", "--user", uname_pwd, "-X", "POST", "-F", "submission.zip=@submission.zip", LINK], capture_output=True, text=True)

            response_json = json.loads(response.stdout)
            score = response_json.get('score')
            return score
        except subprocess.CalledProcessError as e:
            print("retry")
            time.sleep(5)
        except json.JSONDecodeError:
            print("retry")
            time.sleep(5)
    return 'bruh'

# bogus request
def make_request2(uname_pwd):

    for http_retries in range(5):
        try:
            response = subprocess.run(["curl", "--user", uname_pwd, "-X", "POST", "-F", "submission.zip=@./autograder/submission.zip", LINK], capture_output=True, text=True)

            response_json = json.loads(response.stdout)
            score = response_json.get('score')
            return score
        except subprocess.CalledProcessError as e:
            print("retry")
            time.sleep(5)
        except json.JSONDecodeError:
            print("retry")
            time.sleep(5)
    return 'bruh'

def main(uname_pwd):
    number_of_requests = 100 

    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_requests) as executor:
        # Create a list of futures
        futures = []
        for i in range(number_of_requests):
            if i % 2 == 0:  # Even step
                futures.append(executor.submit(make_request2, uname_pwd))
            else:  # Odd step
                futures.append(executor.submit(make_request1, uname_pwd))        
        # Wait for the futures to complete and get the results
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Print results
        for result in results:
            print(result)

if __name__ == "__main__":
    uname_pwd = sys.argv[1]
    main(uname_pwd)
