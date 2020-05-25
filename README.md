# Besalu Notifier
A tool to watch the inventory of Cafe Besalu in Seattle, WA.

## Installation 
```
pip install besalu-notifier
```

## Running
To see the names of items as well as what's currently available as a one-off, run:
```
besalu list
```

and then to watch certain items (including push notifications when they're all there):
```
besalu watch "Lemon Blackberry Muffin, Almond Croissant, Bread Pudding"
```

To see what options are available for watch, run:
```
besalu watch --help
```