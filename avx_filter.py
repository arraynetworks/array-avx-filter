#!/usr/bin/env python
# -*-coding:utf-8 -*-

# Copyright (c) 2017 ArrayNetworks
#All Rights Reserved.
#FileName: avx_filter.py
#Author: litao@arraynetworks.com.cn
#Create date: 2017/9/22
#Description: This file is created to help create VM in the AVX host

from oslo_log import log as logging
from oslo_config import cfg
import nova.conf
from nova.i18n import _LI
from nova.scheduler import filters

LOG = logging.getLogger(__name__)

class AVXFilter(filters.BaseHostFilter):
    """this filter makes the request of creating avx instance with avx.* flavor build and run in the AVX hosts """
    def host_passes(self, host_state, spec_obj):
        avx_opts = [
            cfg.StrOpt('group_hosts',
                        default='',
                        help='this is hosts value for AVX'),
            cfg.StrOpt('reserve',
                        default='nothing',
                        help=' reserve')
        ]
        avx_group = cfg.OptGroup(name = 'AVX',title = "array AVX")
        CONF=cfg.CONF
        CONF.register_group(avx_group)
        CONF.register_opts(avx_opts,avx_group)
        cfg.CONF(project='nova')

        hosts = CONF.AVX.group_hosts.split(';')
        cur_host_ip = host_state.host_ip.format()
        request_flavor_name = spec_obj.flavor.name
        if request_flavor_name[:3].lower() == "avx":
            if cur_host_ip in hosts:
                LOG.debug("the flavor is belong to AVX, and the host %(cur_host_ip)s is in the avx allowed list %(hosts)s",{'cur_host_ip':cur_host_ip,'hosts':hosts})
                return True
            else:
                LOG.debug("the flavor is belong to AVX, but the host %(cur_host_ip)s is not in the avx allowed list %(hosts)s",{'cur_host_ip':cur_host_ip,'hosts':hosts})
                return False
        else:
            LOG.debug("the request flavor is not belong to AVX")
            return True
