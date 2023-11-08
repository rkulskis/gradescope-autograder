# Gradescope Autograder Cluster API

This is an example Python autograder that uses the framework layout from the [gradescope example autograder](https://github.com/gradescope/autograder_samples/tree/master/python)
and exports the testing to a node on a cluster which has a compatible kernel with the test programs and packages you write for your class.

- **Problem:** Assignment test code breaks if there are incompatibilities between the packages they use and the gradescope kernel.
- **Solution:** Rather than building a whole new container with the gradescope framework (which may not even run if there are incompatibilities), simply use `ssh` to run the tests on
  the custom `container` or `VM` on which the tests work and send the results to the gradescope container for publishing.

  *Note: This solution is tailored to teachers who have a `course container` designed for their course which they run on some cloud. It's very easy to create such a container using
  Red Hat's [OPE framework](https://github.com/OPEFFORT/OPE-Testing/tree/container-base-ope) which is an open source tool for creating free online
  textbooks, containers, and presentations.* 

## Architecture
Note that the architecture diagram references the [NERC (New England Research Cloud)](https://nerc-project.github.io/nerc-docs/get-started/create-a-user-portal-account/), but you can set this up with any cloud you want.
<img width="1275" alt="Screenshot 2023-11-05 at 10 34 48 PM" src="https://github.com/rkulskis/gradescope-autograder/assets/91744036/27cc4214-3cb1-4d31-913a-827735ae3415">

## Configuration
1. `id_ed25519` (private key) and `config` files are for ssh configuration to connect to your VM on which the container runs. Configure these as needed.
2. Put the contents of your corresponding public key (i.e. `$( cat id_ed25519.pub)`) inside `~/.ssh/authorized_keys` on your VM.
3. `tests/` contains all your tests
4. `real_run_autograder` and `real_setup.sh` are called once the gradescope container uses ssh to log into your VM.
5. inside `real_run_autograder` a282 in the line `CONTAINER_ID=$(docker run -dv $(pwd):/home/autograder_${EMAIL} a282)` should be replaced with your docker image ID which we assume is already pulled onto the VM
6. `zip.sh` is a one line script to zip up your autograder and ignore any unecessary file (e.g. `.git` directory). We want to minimize the number of files we have to `scp` to our cluster for the sake of efficiency.
## Example run
This framwork is designed to handle concurrent requests from different students on gradescope
because upon copying state with scp to the VM, a new directory is created based on the student's unique email ID, `~/autograder_${student_ID}`, then subsequently deleted upon
pushing the results back to the gradescope container.

Due to the naming of submission directories on the NERC container `~/autograder_${student_ID}` rather than `/autograder`, gradescope_utils's `check_submitted_files` 
fails since it expects the latter path to locate the submission. This wasn't a big issue though and this test can be removed (it's `tests/test_files.py`). All other tests worked.
<img width="1496" alt="Screenshot 2023-11-05 at 10 36 35 PM" src="https://github.com/rkulskis/gradescope-autograder/assets/91744036/258f701a-f235-4075-8920-c5450bdf2dd2">
Here's a screenshot of the VM on NERC to which the gradescope VM `scp`s the state to and then starts a docker container to run the tests. At the end both the docker container and the directory are cleaned up (deleted) on the NERC VM.
<img width="912" alt="Screenshot 2023-11-08 at 2 09 16 PM" src="https://github.com/rkulskis/gradescope-autograder/assets/91744036/c2e38e2e-e6bb-4a31-a49c-49d2f5fb770b">





