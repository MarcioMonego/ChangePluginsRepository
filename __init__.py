from modules.core.props import Property
from modules import cbpi
from flask import g, request, url_for, redirect

import json
import sys

from flask import Blueprint, request, send_from_directory
from importlib import import_module
from modules import socketio, cbpi

#from git import Repo
import os
import requests
import yaml
#import shutil

blueprint = Blueprint('ChangePluginsRepositorory', __name__)

modules = {}

def merge(source, destination):
    """
    Helper method to merge two dicts
    :param source:
    :param destination:
    :return:
    """
    for key, value in source.items():
        if isinstance(value, dict):
               # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination

@blueprint.route('/list', methods=['GET'])
def plugins():
    """
    Read the central plugin yaml to get a list of all official plugins
    :return:
    """
    
    mergedPlugins = ""

    #response = requests.get("https://raw.githubusercontent.com/Manuel83/craftbeerpi-plugins/master/plugins.yaml")
    
    parameterName = "Plugins_Repository"
    pluginsFileOnRepository = cbpi.get_config_parameter(parameterName, None)

    parameterName = "Plugins_Repository_MergeWithOriginal"
    parameterToVerify = cbpi.get_config_parameter(parameterName, None)

    # Make request to plugins file on repository
    response = requests.get(pluginsFileOnRepository)
    mergedPlugins = yaml.load(response.text)

    if parameterToVerify is not None and parameterToVerify == "Yes":
        # Make request to plugins file on repository
        if pluginsFileOnRepository != "https://raw.githubusercontent.com/Manuel83/craftbeerpi-plugins/master/plugins.yaml" :
            responseToOriginal = requests.get("https://raw.githubusercontent.com/Manuel83/craftbeerpi-plugins/master/plugins.yaml")
            mergedPlugins = merge(yaml.load(responseToOriginal.text), mergedPlugins)

    cbpi.cache["plugins"] = merge(mergedPlugins, cbpi.cache["plugins"])
    for key, value in  cbpi.cache["plugins"].iteritems():
        value["installed"] = os.path.isdir("./modules/plugins/%s/" % (key))

    return json.dumps(cbpi.cache["plugins"])

@cbpi.initalizer(order=9998)
def init(cbpi):

    cbpi.app.register_blueprint(blueprint, url_prefix='/api/ChangePluginsRepositorory/editor')

class ConnectionInterceptorToChangePluginsRepository:

    @cbpi.app.before_request
    def before_request():
        # check if route is the ones envoled in recipe import
        if request.url_rule is not None and request.url_rule.rule == "/api/editor/list":
            parameterToVerify = cbpi.get_config_parameter("Plugins_Repository", None)
            if parameterToVerify is not None:
                return redirect('api/ChangePluginsRepositorory/editor/list')

@cbpi.initalizer(order=9999)
def init(cbpi):
    """
    Initializer for ChangePluginsRepository
    :param app: the flask app
    :return: None
    """

    # Verifies if parameter was definied previously
    # Creates the missing parameter

    parameterName = "Plugins_Repository"
    parameterToVerify = cbpi.cache.get("config").get(parameterName)
    if parameterToVerify is None:
        cbpi.add_config_parameter(parameterName, "https://raw.githubusercontent.com/Manuel83/craftbeerpi-plugins/master/plugins.yaml", "text", "Plugins file on repository")

    parameterName = "Plugins_Repository_MergeWithOriginal"
    parameterToVerify = cbpi.get_config_parameter(parameterName,None)
    if parameterToVerify is None:
        cbpi.add_config_parameter(parameterName, "No", "select", "Plugins file on repository",['Yes','No'])