#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2015  Matthias Kolja Miehl
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
DESCRIPTION: Python script for generating email signatures from
             a single (HTML) template for all employees at once
UPDATES    : https://github.com/makomi/email-signature-generator
"""


# -----------------------------------------------------------------------------

# include libraries and set defaults
import os, shutil, errno
from configparser import ConfigParser, ExtendedInterpolation
from string import Template

outputFolder    = "output"
releaseFolder   = "" # e.g. "in use"
fileData        = "data.cfg"
fileTemplateSig = "signature.template.html"

# -----------------------------------------------------------------------------
# helper functions

# access configuration
def ConfigSectionMap(section):
    dict1={}
    options = cfg.options(section)
    for option in options:
        try:
            dict1[option] = cfg[section][option]
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            # not part of the template
            print("exception on '%s!'" % option)
            dict1[option] = None
    return dict1

# create a directory
def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

# -----------------------------------------------------------------------------

# set up output folder
if not os.path.isdir(outputFolder):
    mkdir(outputFolder)
else:
    # else: delete all files (old signatures) in output directory
    for content in os.listdir(outputFolder):
        path = os.path.join(outputFolder, content)
        try:
            if os.path.isfile(path):
                os.unlink(path)
            #elif os.path.isdir(path): shutil.rmtree(path)
        except:
            print("exception on '%s'!" % path)


# create folder for the files that are in use
if releaseFolder != "" and not os.path.isdir(releaseFolder):
    mkdir(releaseFolder)

# -----------------------------------------------------------------------------

# read in template file and data file
fpTemplate = open(fileTemplateSig)
src = Template(fpTemplate.read())

cfg = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)
cfg.read(fileData)


# for every person in the data file
for person in cfg.sections():
    if ConfigSectionMap(person)["type"] == "person":
        # read its data
        first_name   = ConfigSectionMap(person)["first_name"]
        last_name    = ConfigSectionMap(person)['last_name']
        department   = ConfigSectionMap(person)['department']
        tel_base     = ConfigSectionMap(person)['tel_base']
        tel_generic  = ConfigSectionMap(person)['tel_generic']
        tel          = ConfigSectionMap(person)['tel']
        mobile       = ConfigSectionMap(person)['mobile']
        fax          = ConfigSectionMap(person)['fax']
        email        = ConfigSectionMap(person)['email']
        url          = ConfigSectionMap(person)['url']
        company_full = ConfigSectionMap(person)['company_full']
        street       = ConfigSectionMap(person)['street']
        zip_code     = ConfigSectionMap(person)['zip_code']
        city         = ConfigSectionMap(person)['city']
        state        = ConfigSectionMap(person)['state']
        managers     = ConfigSectionMap(person)['managers']
        local_court  = ConfigSectionMap(person)['local_court']
        # FIXME: dirty hack
        # this field is optional
        try:
            more_text    = ConfigSectionMap(person)['more_text']
        except:
            pass

        # assemble dataset for signature
        d = {
                'first_name':first_name,
                'last_name':last_name,
                'department':department,
                'tel_base':tel_base,
                'tel_generic':tel_generic,
                'tel':tel,
                'mobile':mobile,
                'fax':fax,
                'email':email,
                'url':url,
                'company_full':company_full,
                'street':street,
                'zip_code':zip_code,
                'city':city,
                'state':state,
                'managers':managers,
                'local_court':local_court,
                'more_text':more_text
            }

        # substitute variables in template, save as result
        result = src.substitute(d)

        # write result to a file named like the current section 
        fpResult = open(outputFolder + "/" + person +".html", 'w')
        fpResult.write(result)
        fpResult.close()


# let user read the script's output
#input("Everything done!\n\nPlease, check the files for errors ... ")
