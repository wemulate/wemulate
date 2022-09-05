.. incoming-outgoing-explanation:

Incoming - Outgoing Explanation
###################################
WEmulate uses tc in the background. Because tc can not be set on bridge interfaces, the developer decided to set the appropriate disturbance parameters on the first interface used in the bridge. The developers have introduced two keywords: incoming and outgoing, to influence the traffic in different directions.
If there are the interfaces LAN-A and LAN-B in the current connection, incoming influences the traffic from LAN-A to LAN-B, whereas outgoing influences the traffic in the other direction from LAN-B to LAN-A.
The following drawings should clarify the handling:

.. code-block:: bash 

                            +-----------------Linux Bridge-----------------+
                            |                                              |
                            |    +-----------+           +-----------+     |
                            |    |           |           |           |     |
                            |    |   LAN-A   |           |   LAN-B   |     |
                            |    |           |           |           |     |
                            |    |           |           |           |     |
                            |    |           |           |           |     |
                            +----+---^----+--------------+--^----+---+-----+
                     incoming       +-+  +-+ outgoing       |    |
                     will influence  |    | will influence  |    |
                     traffic here    |    | traffic here    |    |
                                     |    |                 |    |
                            request  |    |                 |    |
       +----------------+------------+    |                 |    |            +---------------+
       |                |                 |                 |    |  request   |               |
       |  Source        |    reply        |                 |    +------------>  Destination  |
       |                <-----------------+                 |                 |               |
       |                |                                   |      reply      |               |
       |                |                                   +-----------------+               |
       |                |                                                     |               |
       |                |                                                     |               |
       |                |                                                     |               |
       |                |                                                     |               |
       +----------------+                                                     +---------------+