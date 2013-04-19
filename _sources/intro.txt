================================================================================
Introduction
================================================================================

pysiriproxy is a porting of the
`SiriProxy <https://github.com/plamoni/SiriProxy>`_ project from Ruby to
Python. Siri Proxy was created by Pete Lamonica.

Siri Proxy is a proxy server for Apple's Siri "assistant." The idea is to allow
for the creation of custom handlers for different actions. This can allow
developers to easily add functionality to Siri. 

.. note:: You may also be interested in the
   :ref:`siriviewer <https://code.google.com/p/siriviewer/>` project which
   provides a graphical interface for easily testing pysiriproxy plugins.

----------------------------------------
About
----------------------------------------

pysiriproxy is a port of `Siri Proxy <https://github.com/plamoni/SiriProxy>`_
from Ruby to Python.

From the About description of Siri Proxy:

    "Siri Proxy is a proxy server for Apple's Siri "assistant." The idea is to
    allow for the creation of custom handlers for different actions. This can
    allow developers to easily add functionality to Siri."

pysiriproxy is very much in its early stages and is a work in progress. Users
will likely encounter many issues during use and are advised to submit their
issues so that siriproxy can be improved.

----------------------------------------
Acknowledgements
----------------------------------------

`Siri Proxy <https://github.com/plamoni/SiriProxy>`_ is the foundation of
pysiriproxy and as such this project would not exist without the work by
Pete Lamonica and all the developers working to create and improve Siri Proxy.

I'd also like to thank the following people for their work in debugging and
improving the project:

- Aaron (meluvalli): has discovered and reported countless issues with
  all aspects of the project and also deduced how to configure the server
  to work with the new server for iOS 6.

- Matt Parmett: sole investigator of how to get the pysiriproxy server
  running on a jailbroken iPhone and through this process helped find and
  test many speed/implementation improvements to the system.

All of the help improving pysiriproxy is much appreciated!


----------------------------------------
Licensing
----------------------------------------

Just as `Siri Proxy <https://github.com/plamoni/SiriProxy>`_ is covered by
the `GNU General Public License v3.0 <https://www.gnu.org/licenses/>`, so is
pysiriproxy. Below is the license:

    pysiriproxy. Copyright 2012 Brett Ponsler, Pete Lamonica

    pysiriproxy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pysiriproxy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pysiriproxy.  If not, see <http://www.gnu.org/licenses/>.


----------------------------------------
Disclaimer
----------------------------------------

I am in no way affiliated with Apple. This program is by no means
endorsed by Apple.

Please refrain from using this software for anything malicious.
