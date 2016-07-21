### What: Builds a Rancher OS virtual machine template

#### How?
Using docker we run Hashicorp Packer within a CentOS-based container that has qemu-kvm installed.

#### Why?
The goal is to create a very small template in a automated and repeatable for RancherOS.

#### Requirements
- Linux w/KVM
- Docker and Docker Compose

#### Configuration
The only modification that should be required is adding your public ssh key to `cloud-config.yml`.

#### Run and build
One simple command...

```
docker-compose up
```
#### Issues

If your SSH key does not work add
```
rancher.password=your-password-here
```
to the end of the `linux` line in grub
