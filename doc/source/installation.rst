.. _Installing-label:


.. highlight:: console
   :linenothreshold: 1000

================================================================================
Installing pysiriproxy
================================================================================

The following page contains step by step instructions for installing
pysiriproxy on an Ubuntu system. These instructions have been tested on the
following Ubuntu versions: 10.04, 11.10, and 12.04.

.. _dnsmasq-label:

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Installing and configuring dnsmasq
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

In order to intercept the commands being sent from the iPhone to Apple's server
you must install a program called *dnsmasq* onto a machine that will be
connected to the same network as the iPhone. The following provides instructions
on properly installing dnsmasq.

Run the following commands::

    $ sudo apt-get install dnsmasq

Now, open the file **/etc/dnsmasq.conf** with the editor of your choice.

Search for **#address=/double-click.net/127.0.0.1** (this should be roughly the
62nd line). Once the line is found, replace that line with the following two
lines::

    address=/guzzoni.apple.com/(your_machine's_ip_address).
    address=/kryten.apple.com/(your_machine's_ip_address).

Be sure to replace your machine’s IP address and then save the file. This will
allow the pysiriproxy server accept connections from devices using either
iOS 5 or iOS 6.

Finally, restart dnsmasq for the new IP address to take effect::

    $ sudo /etc/init.d/dnsmasq restart

.. note:: The above installation sequence was taken from
   `How to install Siri Proxy <http://www.iphonestuffs4u.com/how-to-install-siri-proxy/>`_.

.. note:: Once pysiriproxy has been installed and configured you can follow the
   instructions on :ref:`changing the dnsmasq IP address<changingDnsmasqIp-label>`
   to easily change the IP address used by dnsmasq.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Installing subversion and git
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Subversion and Git are needed to access the repositories for some of the
necessary modules to run pysiriproxy.

Run the following commands to install subversion::

    $ sudo apt-get install subversion

Run the following commands to install Git::

    $ sudo apt-get install -y aptitude
    $ sudo aptitude build-dep git-core
    $ cd ~
    $ wget http://git-core.googlecode.com/files/git-1.7.10.tar.gz
    $ tar xzvf git-1.7.10.tar.gz
    $ cd git-1.7.10
    $ ./configure
    $ make
    $ sudo make install

    $ git --version

    $ cd ../ && rm -rf git-1.7.10*

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Installing the CFPropertyList module
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The Python
:ref:`CFProperyList <https://github.com/bencochran/CFPropertyList>` module
is needed the run pysiriproxy. It can be installed by running the following
commands::

    $ cd /opt
    $ sudo git clone https://github.com/bencochran/CFPropertyList.git
    $ sudo chown -R $USERNAME:$USERNAME CFPropertyList
    $ cd CFPropertyList
    $ python setup.py build
    $ sudo python setup.py install

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Installing the biplist module
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The Python
:ref:`biplist <https://github.com/wooster/biplist>` module
is needed the run pysiriproxy. It can be installed by running the following
commands::

    $ sudo apt-get install python-setuptools
    $ sudo easy_install biplist

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Installing the twisted module
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The Python
:ref:`twisted <http://twistedmatrix.com/trac/>` module
is needed the run pysiriproxy. It can be installed by running the following
commands::

    $ sudo apt-get install python2.6-dev
    $ sudo easy_install twisted

**NOTE**: Replace "2.6" with the version of Python you will be using. You can
get the correct number by typing the following into a Python shell::

    import sys
    sys.version[0:3]


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Installing the pyamp module
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The Python :ref:`pyamp <http://code.google.com/p/pyamp/>` module is needed
to run pysiriproxy. It can be installed by running the following commands::

    $ cd /opt
    $ svn checkout http://pyamp.googlecode.com/svn/trunk/pyamp
    $ sudo chown -R $USERNAME:$USERNAME pyamp
    $ cd pyamp
    $ python setup.py build
    $ sudo python setup.py install

%%%%%%%%%%%%%%%%%%%%%%%
Installing pysiriproxy
%%%%%%%%%%%%%%%%%%%%%%%

Run the following commands::

    $ cd /opt
    $ svn checkout http://pysiriproxy.googlecode.com/svn/trunk/pysiriproxy
    $ sudo chown -R $USERNAME:$USERNAME pysiriproxy
    $ cd pysiriproxy
    $ python setup.py build
    $ python setup.py install
    $ sudo ./siriproxy

You can also install pysiriproxy using Python setuptools as follows::

    $ sudo apt-get install python-setuptools
    $ sudo easy_install pysiriproxy


.. highlight:: python
   :linenothreshold: 1000
