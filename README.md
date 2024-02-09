# Gradescope Autograder Cluster API

This is an example Python autograder that uses the framework layout
from the [gradescope example
autograder](https://github.com/gradescope/autograder_samples/tree/master/python)
and exports the testing to a node on a cluster which has a compatible
kernel with the test programs and packages you write for your class.

- **Problem:** Assignment test code breaks if there are
 incompatibilities between the packages they use and the gradescope
 kernel.  - **Solution:** Rather than building a whole new container
 with the gradescope framework (which may not even run if there are
 incompatibilities), simply use `ssh` to run the tests on the custom
 `container` or `VM` on which the tests work and send the results to
 the gradescope container for publishing.

  *Note: This solution is tailored to teachers who have a `course
  container` designed for their course which they run on some
  cloud. It's very easy to create such a container using Red Hat's
  [OPE
  framework](https://github.com/OPEFFORT/OPE-Testing/tree/container-base-ope)
  which is an open source tool for creating free online textbooks,
  containers, and presentations.*

## Architecture

Note that the architecture diagram references the
[NERC (New England Research
Cloud)](https://nerc-project.github.io/nerc-docs/get-started/create-a-user-portal-account/),
but you can set this up with any cloud you want.

![Architecture diagram](images/architecture.png)

## Configuration

1. `id_ed25519` (private key) and `config` files are for ssh configuration to
   connect to your VM on which the container runs. Configure these as needed.

2. Put the contents of your corresponding public key (i.e. `$( cat
   id_ed25519.pub)`) inside `~/.ssh/authorized_keys` on your VM.

3. `tests/` contains all your tests

4. `real_run_autograder` and `real_setup.sh` are called once the gradescope
   container uses ssh to log into your VM.

5. inside `real_run_autograder` a282 in the line `CONTAINER_ID=$(docker run -dv
   $(pwd):/home/autograder_${EMAIL} a282)` should be replaced with your docker
   image ID which we assume is already pulled onto the VM

6. `zip.sh` is a one line script to zip up your autograder and ignore any
   unecessary file (e.g. `.git` directory). We want to minimize the number of
   files we have to `scp` to our cluster for the sake of efficiency.  ##
   Example run This framwork is designed to handle concurrent requests from
   different students on gradescope because upon copying state with scp to the
   VM, a new directory is created based on the student's unique email ID,
   `~/autograder_${student_ID}`, then subsequently deleted upon pushing the
   results back to the gradescope container.

Due to the naming of submission directories on the NERC container
`~/autograder_${student_ID}` rather than `/autograder`,
gradescope_utils's `check_submitted_files` fails since it expects the
latter path to locate the submission. This wasn't a big issue though
and this test can be removed (it's `tests/test_files.py`). All other
tests worked.

![Screenshot showing passing tests](images/test_results.png)

Here's a screenshot of the VM on NERC to which the gradescope VM
`scp`s the state to and then starts a docker container to run the
tests. At the end both the docker container and the directory are
cleaned up (deleted) on the NERC VM. 

![Screenshot showing the result of running docker ps](images/docker_ps.png)

## V2: OpenShift Serverless Service

This version of the service uses curl to send the student submission to a
Knative service route on an openshift cluster. Using a TLS connection verified
by a manually configured username and password, the API only accepts incoming
requests from the professor's gradescope containers which are configured in the
directory `gradescope_autograder`.  The service uses Flask to run the set of
tests calling `run_tests.py` and sends a JSON response `results.json` back to
the gradescope container which made the request.

### Scaling

This version of the service can scale because it uses Knative to scale in
proportion to the requests in a severless manner.

### Security

The gradescope container only sends and receives a file using `curl`, so no
student code is ran on the container. This guarantees safety since the student
can only submit files and cannot `ssh` into the `gradescope_autograder`
container.

The `autograder container` which is run on the OpenShift cluster currently
executes the student code with full permissions; however, the next iteration
will include running student code in a temporary directory with lower
privilages such that it can't access outside of that directory. Then when you
configure the service, you can hard code the USERNAME and PASSWORD used for
curl authentication so that these values are no longer stored in envirnomental
variables (which a student may have access to).

### Testing Concurrency

Run `python3 test_concurrent.py` which successfully tests 100 concurrent
requests.
