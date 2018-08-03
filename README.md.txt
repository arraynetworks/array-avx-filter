The following 4 steps are how to use AVX Filter:
1. Creating AVX Flavors
    To create the AVX flavors in the OpenStack, execute the following precedure:
    1.1 Configure AVX flavor parameters using the following command:
        openstack flavor create --id auto --ram <memory_size> --disk <disk_size> --vcpus <cpu_number> avx.<flavor_class>.<flavor_name>
        Note: In the above command, “flavor_class” parameter is used for extension with the default value being 1, and the “flavor_name” parameter is used to define VA instance type.
        For example, execute the following command to create a small-size AVX flavor:
        [root@localhost]# openstack flavor create --id auto --ram 4096 --disk 40 --vcpus 2 avx.1.small

    1.2 Check the created flavors using the following command:
        [root@localhost]# nova flavor-list

2. Adding AVX Nova Scheduler Filter
    In OpenStack controller node, when more than one compute node host exists, nova scheduler is responsible to decide which compute node host should launch a VM (VA Instance in terms of AVX) among other responsibilities.
    To ensure that the nova scheduler will pick AVX node to run a given VM, execute the following procedure:
    2.1 Open the “nova.conf” configuration file.
        [root@localhost]# vi /etc/nova/nova.conf
    2.2 Add AVX nova scheduler filter into the “nova.conf” configuration file.
        scheduler_default_filters=RetryFilter,AvailabilityZoneFilter,RamFilter,DiskFilter,ComputeFilter,ComputeCapabilitiesFilter,ImagePropertiesFilter,ServerGroupAntiAffinityFilter,ServerGroupAffinityFilter,CoreFilter,AVXFilter
    2.3 Add AVX configuration group IP address to the end of the “nova.conf” configuration file.
        [AVX]
        group_hosts = <ip_address1>;<ip_address2>…;<ip_addressN>

3. Downloading the AVX Filter
    Obtain the “avx_filter.py” file published together with the AVX and OpenStack Integration Guide and then store the file to the following directory:
        /usr/lib/python2.7/site-packages/nova/scheduler/filters/
4. Restarting OpenStack Services
    Restart the following services to make the changes take effect:
        [root@localhost filters]#systemctl restart openstack-nova-api
        [root@localhost filters]#systemctl restart openstack-nova-scheduler