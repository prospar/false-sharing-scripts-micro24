# README file for MICRO Artifact for Paper 506

V. Patel, S. Biswas, and M. Chaudhuri. Leveraging Cache Coherence to Detect and Repair False Sharing On-the-fly.

## Prerequisite

The following setup is required for the simulation to run. We use an Ubuntu distribution for our setup, and our instructions are tailored to Ubuntu.

### Docker Installation

- [Install Docker Enginer on Ubuntu](https://docs.docker.com/engine/install/ubuntu)
- [Install Docker Desktop on Mac](https://docs.docker.com/docker-for-mac/install)
- [Install Docker Desktop on Windows](https://docs.docker.com/docker-for-windows/install)

We include the installation steps required for an Ubuntu system from the first link for convenience.

```shell
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Perf Event Paranoid

We need to set the `perf_event_paranoid` flag to -1 for Ubuntu distribution only. Execute the following command with `sudo` privileges to set the flag: `sudo sysctl kernel.perf_event_paranoid=-1`

### KVM Installation

[How to Install KVM on Ubuntu](https://phoenixnap.com/kb/ubuntu-install-kvm)

We include the installation steps required for an Ubuntu system from the link for convenience.

```shell
sudo apt update
# A non-zero value is expected for virtualization to work
egrep -c '(vmx|svm)' /proc/cpuinfo
sudo apt install cpu-checker
sudo kvm-ok
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils -y
```

### Post-installation Steps for Docker and KVM

After installing `docker` and `kvm`, add your user to the `docker` and `kvm` user groups.

```shell
# Docker
sudo groupadd docker
sudo usermod -aG docker $USER # Your user ID

# KVM
sudo adduser $USER libvirt # Your user ID
sudo adduser $USER kvm
```

### Hardware Requirement

1. Please check whether the host system supports virtualization.
2. Please check whether the root partition has at least 150 GB of free storage if `docker` is installed with the default setting. At least an 8-core system with 32GB RAM.

### Suggestions

The fully functional container may consume around 150GB of disk space. We recommend changing the mount point for the `docker` image to a partition with around 250GB of free disk space.


## Downloading the docker image

The docker image `micro-false-sharing-artifact.tar` is located at path `/data/vipinpat/` on the Nilgiri server. The image is approximately 13GB in size. Use `scp` to copy the image to your local folder.

`scp $USER@nilgiri.cse.iitk.ac.in:/data/vipinpat/micro-false-sharing-artifact.tar  /data/$USER/`

TODO: Update with the download link. Test that the link is working.

## Steps to create Docker container

```shell
# This step may take around five minutes
docker import micro-false-sharing-artifact.tar
# Get the newly created image id <image_id>
docker image ls
# Create the container (only once)
docker run -it --privileged <image_id> /bin/bash
```

Use `sudo` if the username is not added to the `docker` user group.

Try the following command if you get "permission denied while trying to connect to the Docker daemon socket at unix": `newgrp docker`.

After successfully initializing the container, you will need to log into the container as `root`. It should happen automatically after following the earlier steps.

Run the following commands in another terminal.

```shell
docker ps -a # note the container_id for the image
# Rename the container to something that you can easily remember and identify. For example, micro24-fs.
docker container rename <container_id> micro24-fs
```

Close the terminal.

Use the following commands to connect to and manage an existing container. Please refer to the `docker` [documentation](https://docs.docker.com/) for more details.

- Start a container: `docker start <container_name>`
- Stop a running container: `docker stop <container_name>`
- Connect to a running container: `docker attach <container_name>`
- Detach the user from the container: `Ctrl+P` and then `Ctrl+q`
- Stop the container, the user exits, and control is transferred to the host machine: `exit`

## Source Code

The `/root/.bashrc` file defines a few environment variables for convenience, and it should already be added in `docker` container. Please add the following snippet to `/root/.bashrc` if not already present.

```bash
export FS_FRAMEWORK="/home/prospar/false-sharing-scripts-micro24"
export MICRO_VIR_ENV="/home/prospar/micro-virtualenv"
export MICRO_GEM5="/home/prospar/micro-virtualenv/false-sharing-micro24/gem5-false-sharing"
export MICRO_RESOURCE="/home/prospar/micro-virtualenv/false-sharing-micro24/false-sharing-resources"
export MICRO_BENCH="/home/prospar/micro-virtualenv/false-sharing-micro24/false-sharing-benchmarks"
export MICRO_OUT="/home/prospar/prospar-micro-output"
export MICRO_RES="/home/prospar/prospar-micro-result"
export MICRO_SCRIPT="/home/prospar/false-sharing-scripts-micro24"
```

Navigate to the `prospar` directory in the docker container: `cd /home/prospar`. The directory structure in `/home/prospar` is as follows.
```
- /home/prospar
  |___ cmake-3.18.4
  |___ micro-virtualenv(contains the source code and resources)
  |    |___ false-sharing-micro24
  |            |__ gem5-false-sharing : contains gem5 source code
  |            |__ false-sharing-resources : contains the execution script and disk image
  |            |__ false-sharing-benchmarks: contains the benchmarks used in our study
  |___ false-sharing-scripts-micro24(scripts to launch experiment)

```
<!-- - Dir `micro-virtualenv/false-sharing-micro24` contains the following folders:
  |__ gem5-false-sharing : contains gem5 source code
  |__ false-sharing-resources : contains the execution script and disk image
  |__ false-sharing-benchmarks: contains the benchmarks used in our study -->

## Building Gem5 Source

The docker image should contain all necessary source and input files. Please use the AE discussion to report an issue in case of any problems.

Artifact committee can communicate through AE website discussion forum. Later we can modify the instruction, saying `Drop an email to one of the authors`

```shell
cd false-sharing-scripts-micro24
# Make sure all scripts and framework code are up-to-date
git pull

# Validate the setup by running the following script one time
bash validation-script.sh

# Build the necessary directories and protocols in Gem5, extract the tar image
bash setup-script.sh

# The setup script will take up to 6 hours to complete. Building each protocol for the first time might take an hour, and extracting images might take up to 2 hours.
```

The container will consume around 80GB of space after building the source: 10 GB for each protocol, 30 GB for 3 protocols, and 50GB for the extracted images.

We are now ready to run experiments and reproduce results.

## Running Experiments

Each script takes the number of iterations as an input argument. We suggest using the number of iterations as 1 for the initial validation. A single iteration takes a minimum of 5-6 weeks to generate all results if launched on a single docker instance.

`bash <script_name> <number_of_trial>`

Please note that the results reported in the paper are an average of 3 iterations. A single iteration may result in a variation of 5% for each experiment.

Our scripts will parse the output results and plot the graphs automatically.

For a quick validation of result, reproducing `Fig 2` (motivation), `Fig 14` (applications with false sharing), and `Fig 15` (applications without false sharing) is advised.

### Expected runtime for different applications with MESI Baseline protocol

| Applications  |Runtime(in hr)| False Sharing |
|---------------|:------------:|--------------:|
| Blackscholes  |  4    |  No  |
| Bodytrack     |  12   |  No  |
| Canneal       |  5    |  No  |
| Facesim       |  24   |  No  |
| Fluidanimate  |  12   |  No  |
| Swaptions     |  26   |  No  |
| Streamcluster |  30   |  Yes |
| Linear-reg    |  10   |  Yes |
| String-match  |  6    |  Yes |
| Locked-toy    |  18   |  Yes |
| Ref-count     |  14   |  Yes |
| ESTM-sftree   |  18   |  Yes |
| Boost-spinlock|  12   |  Yes |
| Lockless-toy  |  34   |  Yes |
| Total time    | 215   |      |


> The total runtime for single iteration of all listed applications for MESI baseline protocol will take around **9 days**<br>
> The runtime for *FSDetect* protocol is similar to MESI Baseline protocol<br>
> The runtime for *FSLite* protocol will be lesser compared to MESI Baseline and depend on the amount of false sharing, e.g., PARSEC applications will have similar runtime to MESI baseline due to no and negligible amount of false sharing. <br>

### Important Figure

 > The *figure 2, 14, and 15* are the primary result of our paper.<br>
 > The artifact also includes script for figure 13, 17 and various optimization exploration discussed in the evaluation section(**VIII-B**) of the paper. 
 > The figures used in the paper are provided in the **`/home/prospar/false-sharing-micro24-scripts/src/reference_plots`** folder
 > The directory **`/home/prospar/false-sharing-micro24-scripts`** will contain all the generated plots 

### Reproducing Figure 2 (motivation)

- `bash introduction-result.sh <number_of_iteration>`
- The script will take around **9 days** to complete for a  single iteration 
- The file `figure2-runtime.pdf` should be generated in the **`/home/prospar/false-sharing-micro24-scripts`** folder.

TODO: SB: Give exact names wherever possible, e.g., `figure1.sh`. Same for the output PDF files.

### Reproducing Figure 13 (Classification of L1 misses into false sharing and non-false-sharing misses)
- `bash false-sharing-classification.sh <number_of_iteration>`
- The experiments of `Figure 13` will generate around **66GB** of log files for a single iteration, Therefore it is advised to run the experiment with sufficient space in the device root partition.
- The script will take around **6-7 days** to complete 
- The plot `figure-13.pdf` will be generated in the **`/home/prospar/false-sharing-micro24-scripts`** folder.

### Reproducing Figure 14 (applications with false sharing)

- `bash primary-result.sh <number_of_iteration>`
- The script will take around **13 days** to complete
- The files `figure-14-runtime.pdf` and `figure-14-energy.pdf` will be generated in the **`/home/prospar/false-sharing-micro24-scripts`** folder.

### Reproducing Figure 15 (applications without false sharing)

- `bash parsec-result.sh 1`
- The script will take around **10 days** to complete
- The plot `figure-15-runtime-energy.pdf` will be generated in the **`/home/prospar/false-sharing-micro24-scripts`** folder.

 <!-- In progress -->
### Reproducing the Figure 16 (FC-IC exploration)
- `bash fc-ic-result.sh <number_of_iteration>`
- A single iteration will take around **12 days** to complete
- The plot `figure-16-runtime.pdf` will be generated in the **`/home/prospar/false-sharing-micro24-scripts`** folder

### Verifying the claim for granularity
 - `bash granularity-result.sh <number_of_iteration>`
 - A single iteration will take around **12 days** to complete 
 - The plot `figure-granularity-runtime.pdf` will be generated in the **`/home/prospar/false-sharing-micro24-scripts`** folder

### Verifying the claim for SAM256
 - `bash sam-result.sh <number_of_iteration>`
 - A single iteration will take around **9 days** to complete
 - The plot `figure-sam-run-time.pdf` will be generated in the **`/home/prospar/false-sharing-micro24-scripts`** folder

### Verifying the claim for Optimized reader
 - `bash opt-reader-result.sh <number_of_iteration>`
 - A single iteration will take around **9 days** to complete
 - The plot `figure-opt-reader-run-time.pdf` will be generated in the **`/home/prospar/false-sharing-micro24-scripts`** folder

### Verifying the claim for 40KB baseline
 - `bash micro baseline-40KB-script.sh <num_of_iteration>`
 - A single iteration will take around **18 days** to complete
 - The graph `figure-baseline-40KB-runtime.pdf` will be generated in the  **`/home/prospar/false-sharing-micro24-scripts`**


### Verifying the claim for Out-of-order core
- Build the false-sharing benchmarks
```shell
cd ${MICRO_VIR_ENV}/false-sharing-micro24/false-sharing-benchmarks
mkdir -p build && cd build
cmake -DSE_MODE=true ..
cmake --build .
```

