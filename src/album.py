#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractproperty

class Album(object):
    """Interface for saving an album"""

    __metaclass__ = ABCMeta

    @abstractproperty
    def links(self):
        """Yank list of audio track links"""
        pass

    @abstractproperty
    def artist(self):
        """Yank artist name"""
        pass

    @abstractproperty
    def album_name(self):
        """Yank album name"""
        pass

