import subprocess
import concurrent.futures
import json

# request with correct solution
def make_request1():
    try:
        response = subprocess.run(["curl", "--user", "${USERNAME}:${PASSWORD}", "-X", "POST", "-F", "submission.zip=@submission.zip", "https://autograder-rkulskis-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com"], capture_output=True, text=True)

        response_json = json.loads(response.stdout)
        score = response_json.get('score')
        return score
    except subprocess.CalledProcessError as e:
        return str(e)
    except json.JSONDecodeError:
        return "mult"


# bogus request
def make_request2():
    try:
        response = subprocess.run(["curl", "--user", "${USERNAME}:${PASSWORD}", "-X", "POST", "-F", "submission.zip=@./autograder/submission.zip", "https://autograder-rkulskis-dev.apps.sandbox-m2.ll9k.p1.openshiftapps.com"], capture_output=True, text=True)

        response_json = json.loads(response.stdout)
        score = response_json.get('score')
        return score
    except subprocess.CalledProcessError as e:
        return str(e)
    except json.JSONDecodeError:
        return "mult"

def main():
    number_of_requests = 100

    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_requests) as executor:
        # Create a list of futures
        futures = []
        for i in range(number_of_requests):
            if i % 2 == 0:  # Even step
                futures.append(executor.submit(make_request2))
            else:  # Odd step
                futures.append(executor.submit(make_request1))        
        # Wait for the futures to complete and get the results
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Print results
        for result in results:
            print(result)

if __name__ == "__main__":
    main()
