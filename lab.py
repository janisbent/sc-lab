"""
network_dataclient_py23.py 

An HTTP network client for side-channel data captures.

To use, instantiate a DataClient object using the server address.
	client = network_captures.DataClient("ADDRESS:PORT")
	
This is intended to connect to a network server (network_captures.py) that returns side-channel 
traces via live capture or a pre-captured file.

This module also provides a helper function (plot_sm) to plot the returned data.
"""

# Copyright 2019 The MITRE Corporation
# Approved for Public Release; Distribution Unlimited. Case Number 18-2369
# Modified for Python 2-3 compatibility 6/2019
# Modified proxy configuration 2/2020
# Modified for seed param 2/2021
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import json
import requests
import numpy as np
import binascii
import matplotlib.pyplot as plt


# Listening port for our data capture server
SERVER_ADDR = 'woodbad.pythonanywhere.com'
SERVER_PORT = 80


def plot_trace(data,
              smooth=1,
              crop=None,
              decimate=1,
              tracedata_label='tracedata',
              value_label='data',
              label_decode=True,
              result_label='result',
              **kwargs):
    """
    Helper function for plotting data returned by client.

    Assumes the structure for the data as:
    data[tracedata_label]: Numpy array to plot
    data[value_label]: [Hex-encoded] value used to request the data
    data['result']: Feedback from target, currently hardcoded to look for 'Password correct'
    """
    

    # Grab the data value associated with the capture data
    label = data[value_label]

    # Hex-decode if requested
    if label_decode:
        label = binascii.unhexlify(label).decode('utf-8') # Python 2-3

    # convolve the data with a box-car if requested - crude low-pass filter
    if smooth > 1:
        # Create a normalized boxcar
        boxcar = np.ones(smooth)/smooth
        
        # Convolve with data
        smoothed = np.convolve(boxcar, data[tracedata_label])

        # Create a pad to keep traces with different smooth factors aligned in time
        nan_pad = np.ones(int(smooth/2)) * np.nan

        # Concat the pad with the data, after trimming the beginning and end of the convolution output
        data_to_plot = np.concatenate((nan_pad, smoothed[smooth:-smooth]))
        label += ' (sm%d)' % smooth
    else:
        # Nothing to do, just grab the data
        data_to_plot = data[tracedata_label]

    if decimate > 1:
        data_to_plot = data_to_plot[::decimate]

    if crop:
        s, e = crop
        data_to_plot = data_to_plot[s: e]
        rng = range(s, e)
    else:
        rng = range(len(data_to_plot))

    # Check if the device indicated success
    if data.get(result_label, None) == 'Password correct':
        label += ' CORRECT!!!!' 
    else:
        label += ' (incorrect)'

    # Plot the data, passing along any additional arguments
    plt.plot(rng, data_to_plot, label=label, **kwargs)
    plt.xlabel('Time')
    plt.ylabel('Power consumption')

    # Show the legend
    plt.legend()
    plt.draw()
    plt.show(block=False)


class DataClient(object):
    """
    HTTP data client to request side-channel captures from the server.
    
    Client provides data which the client uses when performing the pre-determined operation

    Example:
    dc = network_captures.DataClient()
    data = dc.fetch('33333333')
    network_captures.plot_helper(data, 6)
    """
    BASIC_PATH = 'passwordtrigger'
    MED_PATH = 'password'
    ADV_PATH = 'passworddiversify'
                
    def __init__(self, address='%s:%d' % (SERVER_ADDR, SERVER_PORT), path=BASIC_PATH, labels=['value'], seed = None):
        """
        address: 'HOST:PORT' address of server
        path: URI path on server
        label: parameter label for data to pass
        """
        self.base_url = 'http://%s/' % address
        self.path = path
        self.labels = labels
        self.seed = seed

    def _gen_url(self, path, parameters=None):
        """
        Generate a URL to a provided path, formatting parameters as necessary.  
        
        path: URL path
        parameters: dictionary of parameters

        Note: List parameters currently not supported
        """
        if parameters is None:
            parameters = {}

        url = list(self.base_url)
        url.append(path)
        url.append('?')

        formatted_params = []
        for (param, value) in parameters.items(): # slower, but Python 2-3 compatible
            formatted_params.append('%s=%s' % (param, value))

        url.append('&'.join(formatted_params))
        return ''.join(url)

    def fetch(self, values):
        """
        Request side-channel data corresponding to the provided <value>.  
        Note the value should be provided raw as the hex encoding will be performed before 
        generating the URL.
        """
        if isinstance(values, str):
            values = [values.encode('utf-8')]
        if len(values) != len(self.labels):
            print("Error: length of function 'values' parameter must match class 'labels' parameter")
            return {}

        params = {}
        for l, v in zip(self.labels, values):
            params[l] = binascii.hexlify(v).decode('utf-8') # Python 2-3 compatible

        if self.seed:
            params['seed'] = binascii.hexlify(self.seed.encode('utf-8')).decode('utf-8')
            
        resp = requests.get(self._gen_url(self.path, params))
        if (resp.status_code != 200):
            print("Fetch failed with code %d: %s" % (resp.status_code, str(resp.content, 'utf8')))
            return None

        try:
            result = json.loads(resp.content)
        except ValueError:
            return None
        
        if 'tracedata' in result:
            # overwrite hex-encoded tracedata value with a numpy object
            result['tracedata'] = np.frombuffer(binascii.unhexlify(result['tracedata'])) # Python 2-3

        return result

    def fetch_and_plot(self, values, *args, **kwargs):
        result = self.fetch(values)
        plot_trace(result, *args, **kwargs)
